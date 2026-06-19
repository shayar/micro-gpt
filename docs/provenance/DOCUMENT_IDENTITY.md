# Document Identity and Deleted File Context

This Phase 2 starter includes a provenance foundation for future RAG.

## Why

When MicroGPT answers from files, it should know exactly which document was used. A filename alone is weak because files can be renamed, moved, overwritten, or deleted.

## Current identity fields

- `document_id`
- original path
- canonical path
- filename
- extension
- file size
- modified timestamp
- MD5
- SHA-256
- exists/missing status

MD5 is included for quick debugging and compatibility with simple file-management workflows. SHA-256 is the stronger content identity.

## CLI

Register files:

```bash
python scripts/check_documents.py README.md docs/architecture/MicroGPT_Local_Cognitive_Engine_Architecture_v0.6.md
```

Check whether registered files were deleted or moved:

```bash
python scripts/check_documents.py --reconcile
```

## API

- `POST /documents/register`
- `GET /documents`
- `POST /documents/reconcile`
- `GET /documents/{document_id}/context`

The context endpoint currently searches old MicroLake conversation events for document identifiers, paths, hashes, or filenames. Phase 4 will replace this with indexed local RAG.
