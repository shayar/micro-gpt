# ADR-0003: Secure login and maturity gates before generation

## Status

Accepted

## Context

The project requires secure access before maturity and safety readiness.

## Decision

Generation endpoints require authentication. Public access remains disabled unless the maturity level is explicitly `public`.

## Consequences

- Safer development process
- Easier auditability
- More setup required for contributors
