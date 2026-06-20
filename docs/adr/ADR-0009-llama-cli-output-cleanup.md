# ADR-0009: Clean llama-cli output before returning API responses

## Status

Accepted for Phase 2.3.

## Context

The standalone `llama-cli` binary is reliable on Windows machines where `llama-cpp-python` may fail, but it is a command-line program. Its stdout can include startup logs, prompt echoes, timing footer lines, interactive menu text, and model reasoning markers.

Returning that raw stdout directly from `/chat` or `/chat/stream` makes MicroGPT feel unstable and exposes implementation details to users.

## Decision

MicroGPT will treat `llama-cli` as an optional runtime adapter and clean its output before returning responses.

The adapter will:

- use a MicroGPT prompt wrapper around raw user messages;
- keep `llama-cli` in one-shot mode;
- remove console noise such as `Loading model...`, `Exiting...`, timing lines, banner text, and prompt echoes;
- suppress visible thinking blocks by default;
- provide stable, cleaned chunks for `/chat/stream`.

## Consequences

Positive:

- Cleaner responses in Swagger, web, and future desktop/mobile clients.
- Safer separation between model runtime logs and user-facing content.
- Better Windows-first local testing.

Tradeoff:

- `llama_cli` streaming is not true token streaming in Phase 2.3. It buffers and cleans the CLI output first. A future `llama_server` adapter should provide warm-model token streaming.
