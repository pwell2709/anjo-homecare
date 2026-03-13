from pathlib import Path
import re
import sys


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "src").exists() and (candidate / "src" / "layouts" / "base.njk").exists():
            return candidate
    raise FileNotFoundError("Projektwurzel nicht gefunden.")


def check_base_njk(base_path: Path) -> list[str]:
    text = read_text(base_path)
    results: list[str] = []

    if "Content-Security-Policy" in text:
        results.append("base.njk: CSP-Meta gefunden")
    else:
        results.append("base.njk: keine CSP-Meta gefunden")

    preload_hits = re.findall(r'<link\s+rel="preload"[^>]*>', text, flags=re.IGNORECASE)
    if preload_hits:
        results.append(f"base.njk: {len(preload_hits)} preload-Link(s) gefunden")
        for hit in preload_hits:
            results.append(f"  {hit.strip()}")
    else:
        results.append("base.njk: keine preload-Links gefunden")

    return results


def check_htaccess(htaccess_path: Path) -> list[str]:
    if not htaccess_path.exists():
        return ["src/.htaccess: Datei fehlt"]

    text = read_text(htaccess_path)
    results: list[str] = []

    header_checks = {
        "Content-Security-Policy": r"Header\s+(?:always\s+)?set\s+Content-Security-Policy\b",
        "X-Frame-Options": r"Header\s+(?:always\s+)?set\s+X-Frame-Options\b",
        "X-Content-Type-Options": r"Header\s+(?:always\s+)?set\s+X-Content-Type-Options\b",
        "Referrer-Policy": r"Header\s+(?:always\s+)?set\s+Referrer-Policy\b",
        "Strict-Transport-Security": r"Header\s+(?:always\s+)?set\s+Strict-Transport-Security\b",
        "Permissions-Policy": r"Header\s+(?:always\s+)?set\s+Permissions-Policy\b",
    }

    for name, pattern in header_checks.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            results.append(f"src/.htaccess: {name} gefunden")
        else:
            results.append(f"src/.htaccess: {name} fehlt")

    return results


def main() -> None:
    root = find_project_root(Path.cwd())
    base_path = root / "src" / "layouts" / "base.njk"
    htaccess_path = root / "src" / ".htaccess"

    print("=== CSP / Security Headers / Preload Check ===")
    print(f"Projekt: {root}")
    print()

    for line in check_base_njk(base_path):
        print(line)

    print()

    for line in check_htaccess(htaccess_path):
        print(line)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)