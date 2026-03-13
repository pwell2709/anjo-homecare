# scripts/show_pt_broken_lines.py
from pathlib import Path

FILES = [
    "src/pt/about/index.njk",
    "src/pt/faq/index.njk",
    "src/pt/home/index.njk",
    "src/pt/landing/alto/index.njk",
    "src/pt/locais/porto-moniz/index.njk",
    "src/pt/locais/ribeira-brava/index.njk",
    "src/pt/locais/santana/index.njk",
    "src/pt/locais/sao-jorge/index.njk",
    "src/pt/services/index.njk",
]

MARKERS = ["NÒ", "Ò ", "Ò\xad", "ÒÁ", "Ò║", 'û"']

for file_path in FILES:
    path = Path(file_path)
    if not path.exists():
        continue

    print(f"\n===== {file_path} =====\n")
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    found = False
    for i, line in enumerate(lines, start=1):
        if any(marker in line for marker in MARKERS):
            found = True
            print(f"{i}: {line}")

    if not found:
        print("Keine Marker in Datei gefunden.")