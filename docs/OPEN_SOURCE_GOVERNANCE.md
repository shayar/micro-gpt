# Open-Source Governance

## Repository model

MicroGPT uses a monorepo so shared platform services can support multiple future product modules.

## Maintainer areas

| Area | Path | Owner |
|---|---|---|
| API / orchestration | `api/` | TBD |
| Runtime / inference | `api/app/runtime/`, `cpp/` | TBD |
| Safety / maturity | `api/app/safety/`, `docs/SAFETY_AND_MATURITY.md` | TBD |
| Retrieval / search | future `api/app/retrieval/` | TBD |
| Docs / release | `docs/`, root docs | TBD |
| CI / templates | `.github/` | TBD |

## Review rules

- Safety-sensitive PRs require maintainer review.
- Model or dataset changes require license review.
- No public release without evaluation and safety notes.
- No model weights should be committed to Git.

## Release rule

No metric report, no release.

## Good first issues

Good first issues should be small, testable, and safe:

- improve README clarity
- add tests for maturity gate
- add Docker troubleshooting notes
- improve error messages
- add request/response examples

Avoid assigning new contributors to authentication bypass-sensitive code or public-facing safety gates without review.
