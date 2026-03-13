# scripts/find_live_broken_pt_strings.py
from pathlib import Path

ROOTS = [Path("src"), Path("_site")]
EXTENSIONS = {".njk", ".html", ".md", ".txt", ".xml", ".json"}

BROKEN_STRINGS = [
    "Nã­vel",
    "corresponde ã",
    "tambã",
    "irrepreensã",
    "superfã",
    "Isto vai alã",
    "ãé",
    "visã",
    "perã",
    "mantã",
    "higiã",
    "resã",
    "transiçã",
    "famã",
    "nãºmero",
    "previsã",
    "–\"",
]

for root in ROOTS:
    if not root.exists():
        continue

    print(f"\n===== SCAN {root.as_posix()} =====\n")
    found_any = False

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in EXTENSIONS:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = [s for s in BROKEN_STRINGS if s in text]

        if hits:
            found_any = True
            print(path.as_posix())
            for hit in hits:
                print(f"  -> {hit}")

    if not found_any:
        print("Keine Treffer.")