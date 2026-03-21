from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE_JS = ROOT / "src" / "_data" / "site.js"

ENTRIES = {
    "de": [
        '{ label: "AGB", url: "/de/terms/" },',
        '{ label: "Widerruf", url: "/de/withdrawal/" },',
    ],
    "en": [
        '{ label: "Terms", url: "/en/terms/" },',
        '{ label: "Withdrawal", url: "/en/withdrawal/" },',
    ],
    "fr": [
        '{ label: "Conditions", url: "/fr/terms/" },',
        '{ label: "Rétractation", url: "/fr/withdrawal/" },',
    ],
    "pt": [
        '{ label: "Termos", url: "/pt/terms/" },',
        '{ label: "Livre resolução", url: "/pt/withdrawal/" },',
    ],
}

PRIVACY_URLS = {
    "de": '/de/privacy/',
    "en": '/en/privacy/',
    "fr": '/fr/privacy/',
    "pt": '/pt/privacy/',
}


def backup_file(path: Path) -> None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak_{stamp}")
    shutil.copy2(path, backup)
    print(f"Backup erstellt: {backup.relative_to(ROOT)}")


def find_block_bounds(content: str, lang: str) -> tuple[int, int]:
    marker = f"{lang}: {{"
    start = content.find(marker)
    if start == -1:
        raise ValueError(f"Sprachblock nicht gefunden: {lang}")

    next_markers = []
    for other in ["de", "en", "fr", "pt"]:
        if other == lang:
            continue
        pos = content.find(f"{other}: {{", start + 1)
        if pos != -1:
            next_markers.append(pos)

    end = min(next_markers) if next_markers else content.find("  }", start)
    if end == -1:
        end = len(content)

    return start, end


def insert_before_privacy(block: str, lang: str) -> str:
    terms_url = f"/{lang}/terms/"
    withdrawal_url = f"/{lang}/withdrawal/"
    privacy_url = PRIVACY_URLS[lang]

    if terms_url in block and withdrawal_url in block:
        print(f"{lang}: AGB + Widerruf bereits vorhanden")
        return block

    lines = block.splitlines(keepends=True)
    new_lines = []
    inserted = False

    for line in lines:
        if (privacy_url in line) and not inserted:
            indent = line[: len(line) - len(line.lstrip())]
            for entry in ENTRIES[lang]:
                new_lines.append(f"{indent}{entry}\n")
            inserted = True
            print(f"{lang}: AGB + Widerruf vor Datenschutz eingefügt")
        new_lines.append(line)

    if not inserted:
        raise ValueError(f"{lang}: Datenschutz-Eintrag nicht gefunden")

    return "".join(new_lines)


def main() -> None:
    if not SITE_JS.exists():
        raise SystemExit("FEHLER: src/_data/site.js nicht gefunden.")

    backup_file(SITE_JS)
    content = SITE_JS.read_text(encoding="utf-8")

    # Reihenfolge absichtlich stabil: en, de, fr, pt
    for lang in ["en", "de", "fr", "pt"]:
        start, end = find_block_bounds(content, lang)
        block = content[start:end]
        updated_block = insert_before_privacy(block, lang)
        content = content[:start] + updated_block + content[end:]

    SITE_JS.write_text(content, encoding="utf-8")
    print("FERTIG: site.js aktualisiert, AGB und Widerruf in allen Sprachen vor Datenschutz eingefügt.")


if __name__ == "__main__":
    main()