from pathlib import Path
import re
import sys

REQUIRED = ("de", "en", "fr", "pt")


def find_njk_files(root: Path):
    for path in root.rglob("*.njk"):
        if any(part in {"_site", "node_modules"} for part in path.parts):
            continue
        yield path


def parse_langlinks_block(text: str):
    m = re.search(r'langLinks:\s*\n(?P<block>(?:[ \t]+[a-z]{2}:\s*[^\n]+\n)+)', text)
    if not m:
        return None
    block = m.group("block")
    found = {}
    for code, value in re.findall(r'[ \t]+([a-z]{2}):\s*([^\n]+)', block):
        found[code] = value.strip()
    return found


def main():
    root = Path("src")
    if not root.exists():
        raise FileNotFoundError("src nicht gefunden")

    missing = []

    for path in find_njk_files(root):
        text = path.read_text(encoding="utf-8")
        data = parse_langlinks_block(text)
        if data is None:
            continue

        missing_codes = [code for code in REQUIRED if code not in data]
        if missing_codes:
            missing.append((path, missing_codes))

    if not missing:
        print("OK: Alle gefundenen langLinks-Blöcke sind vollständig (de/en/fr/pt).")
        return

    print("FEHLENDE langLinks:")
    for path, codes in missing:
        print(f"{path}: {', '.join(codes)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)