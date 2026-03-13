from pathlib import Path
import re
import ftfy

ROOT = Path("src")
EXTS = {".njk", ".html", ".md", ".css", ".js", ".json", ".yml", ".yaml", ".txt"}

SUSPECT_RE = re.compile(
    r"(Ã[^\s<>{}\[\]()\"']|â(?:€™|€ž|€œ|€|€¦|€“|€”|°)|Â(?:«|»|°|\s))"
)

changed = []
still_suspicious = []

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in EXTS:
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    fixed = text
    for _ in range(3):
        new_fixed = ftfy.fix_text(fixed)
        if new_fixed == fixed:
            break
        fixed = new_fixed

    if fixed != text:
        path.write_text(fixed, encoding="utf-8", newline="")
        changed.append(str(path))

    try:
        final_text = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        final_text = path.read_text(encoding="utf-8", errors="replace")

    hits = SUSPECT_RE.findall(final_text)
    if hits:
        still_suspicious.append((str(path), sorted(set(hits))[:10]))

print("\n=== GEÄNDERTE DATEIEN ===")
if changed:
    for p in changed:
        print(p)
else:
    print("Keine Änderungen notwendig.")

print("\n=== DATEIEN MIT VERDÄCHTIGEN RESTEN ===")
if still_suspicious:
    for p, hits in still_suspicious:
        print(f"{p} -> {', '.join(hits)}")
else:
    print("Keine verdächtigen Reste gefunden.")