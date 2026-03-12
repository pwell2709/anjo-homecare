from pathlib import Path
import re

ROOT = Path("src")
VALID_LANGS = {"de", "en", "fr", "pt"}

SECTION_MAP = {
    "de": {
        "orte": "orte",
        "locations": "orte",
        "lieux": "orte",
        "locais": "orte",
        "landing": "landing",
    },
    "en": {
        "orte": "locations",
        "locations": "locations",
        "lieux": "locations",
        "locais": "locations",
        "landing": "landing",
    },
    "fr": {
        "orte": "lieux",
        "locations": "lieux",
        "lieux": "lieux",
        "locais": "lieux",
        "landing": "landing",
    },
    "pt": {
        "orte": "locais",
        "locations": "locais",
        "lieux": "locais",
        "locais": "locais",
        "landing": "landing",
    },
}

def build_target_path(parts_after_lang, target_lang):
    if not parts_after_lang:
        return f"/{target_lang}/"

    mapped = []
    for part in parts_after_lang:
        mapped.append(SECTION_MAP.get(target_lang, {}).get(part, part))

    return f"/{target_lang}/" + "/".join(mapped) + "/"

def compute_langlinks(path: Path):
    rel = path.relative_to(ROOT)
    parts = list(rel.parts)

    if len(parts) < 2:
        return None

    lang = parts[0]
    if lang not in VALID_LANGS:
        return None

    if parts[-1] != "index.njk":
        return None

    parts_after_lang = parts[1:-1]

    return {
        "de": build_target_path(parts_after_lang, "de"),
        "en": build_target_path(parts_after_lang, "en"),
        "fr": build_target_path(parts_after_lang, "fr"),
        "pt": build_target_path(parts_after_lang, "pt"),
    }

def strip_existing_langlinks(frontmatter: str) -> str:
    lines = frontmatter.splitlines()
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if re.match(r"^langLinks:\s*$", line):
            i += 1
            while i < len(lines) and re.match(r"^[ \t]+(?:de|en|fr|pt):", lines[i]):
                i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"

def inject_langlinks(frontmatter: str, langlinks: dict) -> str:
    block = (
        "langLinks:\n"
        f"  de: {langlinks['de']}\n"
        f"  en: {langlinks['en']}\n"
        f"  fr: {langlinks['fr']}\n"
        f"  pt: {langlinks['pt']}\n"
    )

    lines = frontmatter.splitlines()
    out = []
    inserted = False

    for line in lines:
        out.append(line)
        if re.match(r"^permalink:\s*", line) and not inserted:
            out.append("")
            out.extend(block.rstrip().splitlines())
            inserted = True

    if not inserted:
        out.append("")
        out.extend(block.rstrip().splitlines())

    return "\n".join(out).rstrip() + "\n"

changed = []

for path in ROOT.rglob("index.njk"):
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        continue

    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
    if not match:
        continue

    frontmatter = match.group(1)
    body = match.group(2)

    langlinks = compute_langlinks(path)
    if not langlinks:
        continue

    cleaned = strip_existing_langlinks(frontmatter)
    rebuilt = inject_langlinks(cleaned, langlinks)

    new_text = f"---\n{rebuilt}---\n{body}"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="")
        changed.append(str(path))

print("\n=== REWRITTEN LANGLINKS ===\n")
if changed:
    for item in changed:
        print(item)
else:
    print("Keine Änderungen notwendig.")