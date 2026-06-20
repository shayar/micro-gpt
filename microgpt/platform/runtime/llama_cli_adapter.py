from __future__ import annotations

import queue
import re
import subprocess
import threading
import time
from functools import lru_cache
from typing import Iterator

from microgpt.api.config import get_settings
from microgpt.platform.runtime.base import GenerationResult, RuntimeAdapter
from microgpt.platform.runtime.errors import RuntimeUnavailableError
from microgpt.platform.runtime.model_registry import ModelRegistry, ModelSpec


class LlamaCliRuntime(RuntimeAdapter):
    """Standalone llama.cpp CLI adapter.

    This runtime calls the standalone `llama-cli` binary behind the MicroGPT
    runtime interface. Phase 2.3 focuses on stable one-shot behavior and clean
    user-facing output. It intentionally keeps the adapter optional and
    replaceable; MicroGPT core should never become tied to one model runtime.
    """

    NOISE_PREFIXES = (
        "loading model",
        "exiting",
        "available commands",
        "build",
        "model",
        "modalities",
        "llama_perf_",
        "main:",
        "system_info:",
        "sampler seed:",
        "sampling:",
        "generate:",
    )

    def __init__(self, model: ModelSpec) -> None:
        settings = get_settings()
        self.model = model
        self.model_path = model.resolved_path(settings.model_dir)
        if not self.model_path.exists():
            raise RuntimeUnavailableError(
                f"Model file not found: {self.model_path}. Add a GGUF model locally or update the registry."
            )
        self.cli_path = settings.llama_cli_path

        # Lightweight binary check. Do not load the model here; runtime/status should stay fast.
        try:
            probe = subprocess.run(
                [self.cli_path, "--version"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                check=False,
            )
        except FileNotFoundError as exc:
            raise RuntimeUnavailableError(
                f"llama-cli was not found at '{self.cli_path}'. Install llama.cpp or set "
                "MICROGPT_LLAMA_CLI_PATH to the full llama-cli.exe path."
            ) from exc
        except Exception as exc:  # pragma: no cover - environment-specific
            raise RuntimeUnavailableError(
                f"Could not execute llama-cli at '{self.cli_path}': {exc.__class__.__name__}: {exc}"
            ) from exc

        self.version_output = (probe.stdout or probe.stderr or "").strip()

    @property
    def runtime_name(self) -> str:
        return "llama_cli"

    @staticmethod
    def _format_prompt(user_prompt: str) -> str:
        """Wrap raw user text in a concise instruction prompt.

        Tiny instruct models are much more stable when given a small role and
        output contract. This also discourages visible reasoning text.
        """
        clean_user_prompt = user_prompt.strip()
        return (
            "You are MicroGPT, a helpful local AI assistant.\n"
            "Answer clearly and directly.\n"
            "Do not show internal reasoning, hidden thinking, tool logs, or startup messages.\n"
            "Keep the answer concise unless the user asks for detail.\n\n"
            f"User: {clean_user_prompt}\n"
            "Assistant:"
        )

    def _build_command(self, prompt: str, max_tokens: int | None = None) -> list[str]:
        settings = get_settings()
        token_limit = max_tokens or settings.llama_max_tokens
        wrapped_prompt = self._format_prompt(prompt)
        cmd = [
            self.cli_path,
            "-m",
            str(self.model_path),
            "-p",
            wrapped_prompt,
            "-n",
            str(token_limit),
            "-c",
            str(settings.llama_n_ctx),
            "-t",
            str(settings.llama_n_threads),
            "--temp",
            str(settings.llama_temperature),
            "--top-p",
            str(settings.llama_top_p),
            "-ngl",
            str(settings.llama_n_gpu_layers),
        ]

        # Make llama-cli behave like a one-shot API call instead of an interactive shell.
        if settings.llama_cli_log_disable:
            cmd.append("--log-disable")
        if settings.llama_cli_single_turn:
            cmd.append("--single-turn")
        if settings.llama_cli_suppress_prompt:
            cmd.append("--no-display-prompt")
        if not settings.llama_cli_show_timings:
            cmd.append("--no-show-timings")
        if settings.llama_cli_simple_io:
            cmd.append("--simple-io")
        if settings.llama_reasoning in {"on", "off", "auto"}:
            cmd.extend(["--reasoning", settings.llama_reasoning])

        cmd.extend(settings.llama_cli_extra_args)
        return cmd

    @classmethod
    def _is_banner_art(cls, stripped: str) -> bool:
        if not stripped:
            return False
        banner_chars = set("▄█▀ ▌▐▝▘▖▗▚▞▙▛▜▟|_/\\-+=")
        return len(stripped) > 4 and set(stripped) <= banner_chars

    @classmethod
    def _clean_output(cls, raw: str, prompt: str) -> str:
        """Remove llama-cli UI/logging noise and visible thinking blocks.

        The adapter may receive stdout from several llama.cpp builds. Some emit
        clean text, while others leak banner, loading, prompt echo, timings, or
        shutdown lines. This function makes API output user-facing and stable.
        """
        text = raw.replace("\r\n", "\n").replace("\r", "\n")

        # Remove common inline status fragments even when they are concatenated
        # with the first generated token by stdout buffering.
        text = re.sub(r"(?is)loading\s+model\s*\.\.\.\s*", "", text)
        text = re.sub(r"(?im)^\s*exiting\s*\.*\s*$", "", text)
        text = re.sub(r"(?im)^\s*\[\s*prompt:.*generation:.*\]\s*$", "", text)
        text = re.sub(r"(?im)^\s*llama_perf_.*$", "", text)

        wrapped_prompt = cls._format_prompt(prompt)
        markers = [
            f"> {prompt}",
            prompt,
            wrapped_prompt,
            "Assistant:",
        ]
        for marker in markers:
            idx = text.rfind(marker)
            if idx >= 0:
                text = text[idx + len(marker) :]
                break

        lines = text.splitlines()
        cleaned_lines: list[str] = []
        skip_thinking = False
        skip_command_menu = False

        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            if not stripped:
                if cleaned_lines and cleaned_lines[-1].strip():
                    cleaned_lines.append("")
                continue

            if lower.startswith("available commands"):
                skip_command_menu = True
                continue
            if skip_command_menu:
                if stripped.startswith(">") or stripped.lower().startswith("assistant"):
                    skip_command_menu = False
                else:
                    continue

            if stripped.startswith(">"):
                # Prompt echo or interactive shell marker.
                continue

            if cls._is_banner_art(stripped):
                continue

            # Remove metadata/log lines while keeping normal prose like "Model compression...".
            if lower.startswith(("build", "model", "modalities")) and ":" in stripped:
                continue
            if lower.startswith(cls.NOISE_PREFIXES) and (":" in stripped or lower.startswith(("loading", "exiting", "llama_perf_"))):
                continue
            if stripped.startswith(("/exit", "/regen", "/clear", "/read", "/glob")):
                continue

            # Suppress visible thinking sections.
            if stripped in {"[Start thinking]", "<think>", "<thinking>"}:
                skip_thinking = True
                continue
            if stripped in {"[End thinking]", "</think>", "</thinking>"}:
                skip_thinking = False
                continue
            if skip_thinking:
                continue
            if "[Start thinking]" in stripped or "<think>" in stripped:
                before = stripped.split("[Start thinking]", 1)[0].split("<think>", 1)[0].strip()
                if before:
                    cleaned_lines.append(before)
                skip_thinking = True
                continue

            cleaned_lines.append(line.rstrip())

        cleaned = "\n".join(cleaned_lines).strip()
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        cleaned = re.sub(r"(?is)^assistant:\s*", "", cleaned).strip()
        return cleaned

    @staticmethod
    def _reader_thread(stream, out_queue: "queue.Queue[str | None]") -> None:
        try:
            while True:
                chunk = stream.read(1)
                if chunk == "":
                    break
                out_queue.put(chunk)
        finally:
            out_queue.put(None)

    def _run_process_stream(self, prompt: str, max_tokens: int | None = None) -> Iterator[str]:
        """Run llama-cli and yield stdout incrementally.

        This still uses a short-lived CLI process per request. Phase 2.3 prefers
        clean API responses over pretending to be a perfect model server. A later
        `llama_server` adapter should keep the model loaded persistently.
        """
        settings = get_settings()
        cmd = self._build_command(prompt, max_tokens=max_tokens)
        timeout = settings.llama_cli_timeout_seconds
        start = time.monotonic()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
        except FileNotFoundError as exc:
            raise RuntimeUnavailableError(
                f"llama-cli was not found at '{self.cli_path}'. Install llama.cpp or set MICROGPT_LLAMA_CLI_PATH."
            ) from exc
        except Exception as exc:  # pragma: no cover - environment-specific
            raise RuntimeUnavailableError(f"llama-cli failed to start: {exc.__class__.__name__}: {exc}") from exc

        assert process.stdout is not None
        assert process.stderr is not None
        stdout_queue: "queue.Queue[str | None]" = queue.Queue()
        stderr_queue: "queue.Queue[str | None]" = queue.Queue()
        stderr_parts: list[str] = []

        threading.Thread(target=self._reader_thread, args=(process.stdout, stdout_queue), daemon=True).start()
        threading.Thread(target=self._reader_thread, args=(process.stderr, stderr_queue), daemon=True).start()

        stdout_done = False
        try:
            while not stdout_done:
                if time.monotonic() - start > timeout:
                    process.kill()
                    raise RuntimeUnavailableError(
                        f"llama-cli timed out after {timeout} seconds. Try fewer max_tokens, lower context, "
                        "increase MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS, or use llama-server later for long-running streaming."
                    )

                while True:
                    try:
                        err_chunk = stderr_queue.get_nowait()
                    except queue.Empty:
                        break
                    if err_chunk is not None:
                        stderr_parts.append(err_chunk)

                try:
                    item = stdout_queue.get(timeout=0.1)
                except queue.Empty:
                    if process.poll() is not None and stdout_queue.empty():
                        break
                    continue

                if item is None:
                    stdout_done = True
                    break
                yield item

            return_code = process.wait(timeout=5)
            while True:
                try:
                    err_chunk = stderr_queue.get_nowait()
                except queue.Empty:
                    break
                if err_chunk is not None:
                    stderr_parts.append(err_chunk)

            if return_code != 0:
                details = "".join(stderr_parts).strip() or f"return code {return_code}"
                raise RuntimeUnavailableError(f"llama-cli returned an error: {details}")
        finally:
            if process.poll() is None:
                process.kill()

    def generate(self, prompt: str, max_tokens: int | None = None) -> GenerationResult:
        raw_parts: list[str] = []
        for chunk in self._run_process_stream(prompt, max_tokens=max_tokens):
            raw_parts.append(chunk)
        raw = "".join(raw_parts)
        text = self._clean_output(raw, prompt)
        if not text:
            text = "The local model ran, but MicroGPT could not extract a clean answer from llama-cli output."
        return GenerationResult(
            text=text,
            model_id=self.model.model_id,
            tokens_generated=len(text.split()),
            prompt_tokens=len(prompt.split()),
            runtime=self.runtime_name,
            metadata={
                "model_name": self.model.name,
                "quantization": self.model.quantization,
                "context_length": self.model.context_length,
                "license": self.model.license,
                "model_path": str(self.model_path),
                "cli_path": self.cli_path,
                "cli_version": self.version_output,
                "prompt_wrapper": "microgpt_phase2_3_default",
                "cleaned_output": True,
            },
        )

    def stream_generate(self, prompt: str, max_tokens: int | None = None) -> Iterator[str]:
        """Return clean text through the streaming endpoint.

        For the short-lived `llama-cli` process, truly incremental streaming can
        leak startup/shutdown noise before the cleaner has enough context. Phase
        2.3 therefore buffers the CLI output, cleans it, then yields the answer
        in small chunks. This is stable for Swagger/local testing. A future
        `llama_server` adapter should provide real token streaming.
        """
        result = self.generate(prompt, max_tokens=max_tokens)
        chunk_size = 24
        for start in range(0, len(result.text), chunk_size):
            yield result.text[start : start + chunk_size]


@lru_cache(maxsize=1)
def cached_llama_cli_runtime() -> LlamaCliRuntime:
    settings = get_settings()
    model = ModelRegistry(settings.model_registry_path).get(settings.active_model_id or None)
    if model is None:
        raise RuntimeUnavailableError(
            f"No active model found. Set MICROGPT_ACTIVE_MODEL_ID or add one model to {settings.model_registry_path}."
        )
    if model.runtime != "llama_cli":
        raise RuntimeUnavailableError(f"Active model runtime is {model.runtime}, not llama_cli.")
    if model.status not in {"approved", "local_only", "candidate"}:
        raise RuntimeUnavailableError(f"Model {model.model_id} is not allowed: status={model.status}.")
    return LlamaCliRuntime(model)
