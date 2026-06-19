# ADR-0007: Document Identity and Provenance Foundation

## Status
Accepted for Phase 2 starter.

## Context
MicroGPT will eventually answer questions over local files. The system must know exactly which file was used and whether that file later changed, moved, or disappeared.

## Decision
Add a document identity registry before full RAG. Every registered file records:

- Original path
- Canonical path
- File name and extension
- Size
- Modified timestamp
- MD5 for quick/debug identity
- SHA-256 for stronger content identity
- Stable `document_id`
- Exists/missing status

The registry writes document events to MicroLake and can do a best-effort search through old conversation events if the original file is deleted.

## Consequences
Phase 4 RAG can build on real provenance rather than treating files as anonymous chunks. Deleted or moved files can still be connected to prior chat context when enough metadata was captured earlier.
