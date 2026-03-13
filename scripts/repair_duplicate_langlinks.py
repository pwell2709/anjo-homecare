from pathlib import Path
import re

ROOT = Path("src")

# findet komplette langLinks-Blöcke
BLOCK_RE = re.compile(
    r"langLinks:\n"
    r"(?:[ \t]+de:\s*.*\n)?"
    r"(?:[ \t]+en:\s*.*\n)?"
    r"(?:[ \t]+fr:\s*.*\n)?"
    r"(?:[ \t]+pt:\s*.*\n?)*",
    re.MULTILINE,
)

def clean_block(text: str) -> str:
    matches = list(BLOCK_RE.finditer(text))
    if not matches:
        return text

    # nur den ersten Block behalten und darin doppelte Keys bereinigen
    first = matches[0]
    block = first.group(0).splitlines()

    seen = set()
    cleaned = []
    for line in block:
        m = re.match(r"[ \t]+(de|en|fr|pt):", line)
        if m:
            key = m.group(1)
            if key in seen:
                continue
            seen.add(key)
        cleaned.append(line)

    new_block = "\n".join(cleaned).rstrip() + "\n"

    # alles von erstem bis letztem gefundenen langLinks-Block durch bereinigten ersten ersetzen
    start = matches[0].start()
    end = matches[-1].end()
    return text[:start] + new_block + text[end:]

changed = []

for path in ROOT.rglob("index.njk"):
    original = path.read_text(encoding="utf-8")
    updated = clean_block(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="")
        changed.append(str(path))

print("\n=== REPAIRED DUPLICATE LANGLINKS ===\n")
if changed:
    for p in changed:
        print(p)
else:
    print("Keine Änderungen notwendig.")