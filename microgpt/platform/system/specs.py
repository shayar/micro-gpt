from __future__ import annotations

import os
import platform
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SystemSpecs:
    os: str
    python: str
    cpu_brand: str
    cpu_threads: int
    cpu_flags: list[str]
    avx: bool
    avx2: bool
    fma: bool
    f16c: bool
    total_ram_gb: float | None
    free_disk_gb: float | None


def _cpu_info() -> tuple[str, list[str]]:
    try:
        import cpuinfo  # type: ignore

        info = cpuinfo.get_cpu_info()
        return info.get("brand_raw") or platform.processor() or "unknown", list(info.get("flags") or [])
    except Exception:
        return platform.processor() or "unknown", []


def _ram_gb() -> float | None:
    try:
        import psutil  # type: ignore

        return round(psutil.virtual_memory().total / (1024**3), 2)
    except Exception:
        return None


def collect_system_specs(path: str | Path = ".") -> dict:
    brand, flags = _cpu_info()
    flags_set = {flag.lower() for flag in flags}
    try:
        free_disk_gb = round(shutil.disk_usage(path).free / (1024**3), 2)
    except Exception:
        free_disk_gb = None
    specs = SystemSpecs(
        os=f"{platform.system()} {platform.release()}",
        python=platform.python_version(),
        cpu_brand=brand,
        cpu_threads=os.cpu_count() or 1,
        cpu_flags=sorted(flags_set),
        avx="avx" in flags_set,
        avx2="avx2" in flags_set,
        fma="fma" in flags_set,
        f16c="f16c" in flags_set,
        total_ram_gb=_ram_gb(),
        free_disk_gb=free_disk_gb,
    )
    return asdict(specs)


def recommend_model_tier(specs: dict) -> dict:
    ram = specs.get("total_ram_gb")
    threads = int(specs.get("cpu_threads") or 1)
    avx2 = bool(specs.get("avx2"))
    free_disk = specs.get("free_disk_gb")

    safe_default = {
        "model_id": "qwen3-0.6b-q4-k-m-local",
        "name": "Qwen3 0.6B Q4_K_M GGUF",
        "why": "Smallest recommended CPU smoke-test model for Phase 2.",
    }

    options = [safe_default]
    if ram is None or ram >= 8:
        options.append(
            {
                "model_id": "qwen3-1.7b-q4-k-m-local",
                "name": "Qwen3 1.7B Q4_K_M GGUF",
                "why": "Better quality if the machine has enough RAM and acceptable latency.",
            }
        )
    if ram is not None and ram >= 16 and threads >= 6:
        options.append(
            {
                "model_id": "smollm3-3b-q4-k-m-local",
                "name": "SmolLM3 3B Q4_K_M GGUF",
                "why": "Stronger local model candidate for better laptops.",
            }
        )

    warning = None
    if not avx2:
        warning = "CPU does not report AVX2; prefer the smallest model or a no-AVX llama.cpp build."
    elif free_disk is not None and free_disk < 2:
        warning = "Low free disk space; keep only one tiny GGUF model locally."

    return {
        "recommended": safe_default,
        "options": options,
        "warning": warning,
        "notes": [
            "If llama-cpp-python fails with Windows 0xc000001d, try a CPU-safe rebuild or standalone llama.cpp.",
            "Do not commit .gguf files to GitHub.",
        ],
    }
