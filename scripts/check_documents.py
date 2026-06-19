from __future__ import annotations

import argparse
import json

from microgpt.platform.documents.registry import default_document_registry


def main() -> None:
    parser = argparse.ArgumentParser(description="Register and reconcile document fingerprints.")
    parser.add_argument("paths", nargs="*", help="Files to fingerprint/register")
    parser.add_argument("--reconcile", action="store_true", help="Mark deleted/moved files as missing")
    args = parser.parse_args()

    registry = default_document_registry()
    for path in args.paths:
        identity = registry.register_file(path)
        print(json.dumps(identity.to_dict(), indent=2))

    if args.reconcile:
        changed = registry.reconcile_missing_files()
        print(json.dumps({"changed_count": len(changed), "changed": changed}, indent=2))


if __name__ == "__main__":
    main()
