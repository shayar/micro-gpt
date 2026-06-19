from pathlib import Path

from microgpt.api.auth.security import ensure_dev_user_file
from microgpt.api.config import get_settings


def main() -> None:
    settings = get_settings()
    for path in [
        settings.data_dir / "events",
        settings.data_dir / "auth",
        settings.data_dir / "tables",
        settings.data_dir / "snapshots",
        settings.data_dir / "indexes",
        settings.data_dir / "manifests",
        Path("models"),
        Path("vault"),
    ]:
        path.mkdir(parents=True, exist_ok=True)
    ensure_dev_user_file()
    print("MicroGPT local dev initialized.")
    print(f"Data dir: {settings.data_dir.resolve()}")
    print(f"Default admin username: {settings.admin_username}")
    print("Default admin password comes from MICROGPT_ADMIN_PASSWORD or .env.example.")


if __name__ == "__main__":
    main()
