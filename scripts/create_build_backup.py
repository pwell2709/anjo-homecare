from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def should_exclude(path: Path) -> bool:
    excluded_parts = {
        ".vs",
        ".vscode",
        "node_modules",
        "_site",
        "dist",
        "backups",
        "__pycache__",
    }

    excluded_suffixes = {
        ".pyc",
        ".pyo",
        ".log",
        ".tmp",
    }

    return any(part in excluded_parts for part in path.parts) or path.suffix.lower() in excluded_suffixes


def create_backup(project_root: Path) -> Path:
    if not project_root.exists() or not project_root.is_dir():
        raise FileNotFoundError(f"Projektordner nicht gefunden: {project_root}")

    backups_dir = project_root / "backups"
    backups_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = f"{project_root.name}_full_backup_{timestamp}.zip"
    zip_path = backups_dir / zip_name

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as zip_file:
        for item in project_root.rglob("*"):
            if item == zip_path:
                continue
            if should_exclude(item):
                continue
            if item.is_file():
                arcname = item.relative_to(project_root)
                zip_file.write(item, arcname)

    return zip_path


def main() -> int:
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1]).resolve()
    else:
        project_root = Path.cwd().resolve()

    try:
        zip_path = create_backup(project_root)
        print(f"Voll-Backup erstellt: {zip_path}")
        return 0
    except Exception as exc:
        print(f"Fehler: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())