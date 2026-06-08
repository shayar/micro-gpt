# ADR 0002: Secure Login and Maturity Gate

## Status

Accepted

## Context

MicroGPT is an early-stage generative AI project. It must not be publicly accessible before the system reaches maturity and passes safety review.

Leadership requested secure login and safeguards to prevent violent or sexual content from being generated.

## Decision

MicroGPT will require authenticated access before use.

The system will include a maturity gate with these stages:

- `research`
- `internal`
- `alpha`
- `beta`
- `public`

Public access will remain disabled until maintainers approve safety, security, evaluation, and licensing readiness.

The starter includes a basic safety policy that blocks violent and sexual content requests before model inference.

## Consequences

Benefits:

- Reduces unsafe early access
- Makes project maturity explicit
- Gives maintainers release control
- Aligns product development with safety requirements

Tradeoffs:

- Adds setup complexity
- Early contributors need login credentials
- MVP safety policy is only a starting point and must be improved before public release

## Follow-up work

- Add audit logging
- Add rate limiting
- Add output safety checks
- Add red-team test set
- Add stronger open-source safety classifier
- Add release approval checklist
