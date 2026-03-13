from pathlib import Path

CHECK_DIRS = ["src", "_site"]
EXTENSIONS = {".html", ".njk", ".md", ".xml", ".txt", ".json"}

BAD_SNIPPETS = [
    "Nã",
    "ã©",
    "ã­",
    "ãº",
    "ã ",
    "ãµ",
    "ã‰",
    "ã¨",
    "ã§",
    "ãª",
    "ã´",
    "ã³",
    "ã¢",
    "–\"",
    "â€“",
    "â€”",
    "â€œ",
    "â€\x9d",
    "â€™",
    "â€˜",
    "â€¦",
    " ",
]

results = []

for root_name in CHECK_DIRS:
    root = Path(root_name)
    if not root.exists():
        continue

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in EXTENSIONS:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        hits = [snippet for snippet in BAD_SNIPPETS if snippet in text]
        if hits:
            results.append((str(path).replace("\\", "/"), sorted(set(hits))))

results.sort()

print("\nKONKRETE ENCODING-FEHLER:\n")

if not results:
    print("Keine konkreten Encoding-Fehler gefunden.")
else:
    for file_path, hits in results:
        print(f"{file_path}  ->  Treffer: {', '.join(repr(h) for h in hits)}")

print(f"\nAnzahl Dateien: {len(results)}")