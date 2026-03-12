from pathlib import Path

ROOT = Path("src")

# Nur echte Inhaltsdateien prüfen
EXTS = {".njk", ".html", ".md", ".txt", ".yml", ".yaml", ".json"}

# Diese Marker sind in deinen Dateien fast nie legitim und deuten sehr stark auf Mojibake hin
BAD_MARKERS = [
    "Ã¡", "Ã£", "Ã¢", "Ã¤", "Ã§", "Ã¨", "Ã©", "Ãª", "Ã­", "Ã³", "Ã´", "Ãµ", "Ãº", "Ã¼",
    "Ã„", "Ã–", "Ãœ", "ÃŸ", "Ã€", "Ã‰", "Ã®", "Ã¹",
    "â€“", "â€”", "â€ž", "â€œ", "â€", "â€™", "â€¦", "â€¢", "â€",
    "Â«", "Â»", "Â°", "Â ",
    "\uFFFD",  # echtes Replacement Character
]

def should_check(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in EXTS:
        return False
    parts = {p.lower() for p in path.parts}
    if "_site" in parts or "node_modules" in parts or ".git" in parts:
        return False
    return True

def main():
    findings = []

    for path in ROOT.rglob("*"):
        if not should_check(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError as e:
            findings.append({
                "file": str(path),
                "kind": "UTF-8 decode error",
                "line": None,
                "match": str(e),
                "snippet": ""
            })
            continue

        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            for marker in BAD_MARKERS:
                if marker in line:
                    findings.append({
                        "file": str(path),
                        "kind": "suspicious marker",
                        "line": i,
                        "match": marker,
                        "snippet": line.strip()
                    })

    print("\n=== ENCODING AUDIT ===\n")

    if not findings:
        print("Keine echten Encoding-Verdachtsfälle in src gefunden.")
        return

    current_file = None
    for item in findings:
        if item["file"] != current_file:
            current_file = item["file"]
            print(current_file)

        if item["line"] is None:
            print(f"  [DECODE ERROR] {item['match']}")
        else:
            print(f"  [Zeile {item['line']}] {item['match']}")
            print(f"    {item['snippet']}")
        print()

    print("=== ENDE ===")

if __name__ == "__main__":
    main()