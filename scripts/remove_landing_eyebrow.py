from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

FILES = [
    ROOT / "src/de/landing/alto/index.njk",
    ROOT / "src/fr/landing/alto/index.njk",
    ROOT / "src/pt/landing/alto/index.njk",
]

PATTERN = re.compile(r'^[ \t]*<p class="eyebrow">Alojamento Local</p>\s*\n?', re.MULTILINE)

def main():
    changed = 0

    for path in FILES:
        if not path.exists():
            print(f"FEHLT: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        new_text, count = PATTERN.subn("", text, count=1)

        if count:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            print(f"OK   entfernt: {path}")
            changed += 1
        else:
            print(f"SKIP nicht gefunden: {path}")

    print(f"\nFertig. Geänderte Dateien: {changed}")

if __name__ == "__main__":
    main()