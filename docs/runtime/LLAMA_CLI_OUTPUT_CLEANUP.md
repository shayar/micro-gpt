# Phase 2.3 llama-cli output cleanup

Phase 2.3 makes the standalone `llama-cli` runtime safer for API use.

## Problem

`llama-cli` is a terminal-first program. Depending on build/version/model, it can emit console text that is useful in a terminal but noisy in an API response:

- startup text such as `Loading model...`
- shutdown text such as `Exiting...`
- banner/menu text from interactive mode
- timing footer lines
- visible thinking markers from reasoning models
- echoed prompts

## Decision

The `llama_cli` adapter now:

1. wraps raw user prompts in a small MicroGPT instruction prompt;
2. runs `llama-cli` in one-shot mode;
3. removes common console noise from stdout;
4. suppresses visible thinking blocks by default;
5. makes `/chat/stream` stable by yielding cleaned text chunks after the CLI process completes.

## Important limitation

`llama_cli` still starts a new process and loads the model per request. This is acceptable for Phase 2 CPU validation, but it is not the final performance design.

Future runtime work should add a persistent `llama_server` adapter:

```text
MicroGPT API -> llama-server HTTP endpoint -> warm local GGUF model
```

That will be better for web/desktop UI latency and true token streaming.
