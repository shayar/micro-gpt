from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
from typing import BinaryIO


def _utc_from_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def _hash_file(file_obj: BinaryIO) -> tuple[str, str]:
    md5 = hashlib.md5(usedforsecurity=False)
    sha256 = hashlib.sha256()
    for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
        md5.update(chunk)
        sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


@dataclass(frozen=True)
class DocumentIdentity:
    document_id: str
    path: str
    canonical_path: str
    file_name: str
    extension: str
    size_bytes: int
    modified_time_utc: str
    md5: str
    sha256: str
    exists: bool = True

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def fingerprint_file(path: str | Path) -> DocumentIdentity:
    original = Path(path).expanduser()
    if not original.exists() or not original.is_file():
        raise FileNotFoundError(f"File not found: {original}")

    canonical = original.resolve()
    stat = canonical.stat()
    with canonical.open("rb") as f:
        md5, sha256 = _hash_file(f)

    # The content hash is the strongest identity. Size and filename make debugging easier.
    document_id = hashlib.sha256(
        f"{sha256}:{stat.st_size}:{canonical.name}".encode("utf-8")
    ).hexdigest()[:32]

    return DocumentIdentity(
        document_id=document_id,
        path=str(original),
        canonical_path=str(canonical),
        file_name=canonical.name,
        extension=canonical.suffix.lower(),
        size_bytes=stat.st_size,
        modified_time_utc=_utc_from_timestamp(stat.st_mtime),
        md5=md5,
        sha256=sha256,
        exists=True,
    )
