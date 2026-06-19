# Dependency Approval Workflow

Before adding a dependency:

1. Check official repository.
2. Check exact license file.
3. Check transitive dependencies where practical.
4. Record dependency in `LICENSES.md`.
5. Add reason for adoption.
6. Prefer permissive OSI-approved licenses for core.
7. Keep AGPL/copyleft services optional and isolated unless reviewed.

For models:

1. Check model card.
2. Check license.
3. Check use restrictions.
4. Record exact revision in `MODEL_REGISTRY.md`.
5. Do not commit weights.
