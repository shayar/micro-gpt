# llama-cli Runtime Adapter

The `llama_cli` runtime lets MicroGPT call a standalone `llama-cli` binary from llama.cpp.

This is useful when `llama-cpp-python` fails on Windows but the standalone llama.cpp binary works.

## Runtime shape

```text
MicroGPT FastAPI
  -> llama_cli adapter
  -> subprocess.Popen(... llama-cli ...)
  -> local GGUF model
```

The adapter is optional. MicroGPT still supports `no_model`, `llama_cpp`, and future runtime adapters.

## Required local files

```text
models/
  local/
    Qwen_Qwen3-0.6B-Q4_K_M.gguf
  model_registry.local.json
```

The model file should never be committed to Git.

## Recommended `.env`

```env
MICROGPT_RUNTIME_MODE=llama_cli
MICROGPT_RUNTIME_FALLBACK_ENABLED=true
MICROGPT_MODEL_DIR=./models
MICROGPT_MODEL_REGISTRY_PATH=./models/model_registry.local.json
MICROGPT_ACTIVE_MODEL_ID=qwen3-0.6b-q4-k-m-local
MICROGPT_LLAMA_CLI_PATH=llama-cli
MICROGPT_LLAMA_N_CTX=2048
MICROGPT_LLAMA_N_THREADS=4
MICROGPT_LLAMA_N_GPU_LAYERS=0
MICROGPT_LLAMA_MAX_TOKENS=128
MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS=300
```

## Phase 2.2 streaming fix

The first `llama_cli` adapter used `subprocess.run(...)`, so `/chat/stream` waited for the full model response before sending anything. If generation took longer than 120 seconds, the API could raise an ASGI exception.

Phase 2.2 changes the adapter to use `subprocess.Popen(...)` and incremental stdout reading. This gives safer streaming behavior and lets the API fall back cleanly if a timeout or subprocess error occurs.

## If generation times out

Try one or more of these:

1. Use fewer output tokens:

```json
{
  "message": "Explain AI to a kid.",
  "max_tokens": 64
}
```

2. Increase timeout:

```env
MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS=600
```

3. Lower context for weak laptops:

```env
MICROGPT_LLAMA_N_CTX=1024
```

4. Test the model directly:

```powershell
llama-cli -m models\local\Qwen_Qwen3-0.6B-Q4_K_M.gguf -p "Explain AI to a kid." -n 64 -c 1024 -t 4 -ngl 0
```

## Future improvement

For a production desktop/web app, MicroGPT should eventually support a persistent `llama-server` adapter. That avoids starting a new llama process for every request and should reduce latency.

## Phase 2.3 one-shot CLI fix

Recent llama-cli builds can automatically enter conversation mode when the model has a chat template. In subprocess mode this can make llama-cli wait for another user turn instead of exiting after the first answer.

MicroGPT now adds one-shot API flags by default:

```text
--single-turn
--no-display-prompt
--no-show-timings
--simple-io
--log-disable
--reasoning off
```

Why these defaults exist:

- `--single-turn` makes llama-cli exit after one model response.
- `--no-display-prompt` avoids echoing the prompt into API responses.
- `--no-show-timings` removes performance footers from user-facing output.
- `--simple-io` improves subprocess/console compatibility.
- `--log-disable` reduces banner/log noise.
- `--reasoning off` keeps the first CPU smoke test fast for Qwen3-style reasoning models.

For reasoning experiments later, set:

```env
MICROGPT_LLAMA_REASONING=auto
```

or:

```env
MICROGPT_LLAMA_REASONING=on
```
