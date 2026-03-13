from pathlib import Path
import sys


TARGETS = [
    Path("src/de/legal/index.njk"),
    Path("src/en/legal/index.njk"),
    Path("src/fr/legal/index.njk"),
    Path("src/pt/legal/index.njk"),
    Path("src/de/privacy/index.njk"),
    Path("src/en/privacy/index.njk"),
    Path("src/fr/privacy/index.njk"),
    Path("src/pt/privacy/index.njk"),
]


def add_sitemap_false(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")

    text = path.read_text(encoding="utf-8")

    if "sitemap: false" in text:
        print(f"Schon ok: {path}")
        return

    if not text.startswith("---"):
        raise RuntimeError(f"Kein Frontmatter gefunden: {path}")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise RuntimeError(f"Frontmatter konnte nicht sauber gelesen werden: {path}")

    frontmatter = parts[1]
    body = parts[2]

    frontmatter = frontmatter.rstrip() + "\nsitemap: false\n"
    new_text = f"---{frontmatter}---{body}"

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"Aktualisiert: {path}")


def main() -> None:
    for target in TARGETS:
        add_sitemap_false(target)
    print("OK: legal/privacy aus Sitemap ausgeschlossen.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)