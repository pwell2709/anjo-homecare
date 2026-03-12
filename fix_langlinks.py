from pathlib import Path
import re

ROOT = Path("src")

LANG_PREFIXES = {
    "de": "de",
    "en": "en",
    "fr": "fr",
    "pt": "pt",
}

SECTION_MAP = {
    "de": {
        "orte": "orte",
        "landing": "landing",
    },
    "en": {
        "orte": "locations",
        "locations": "locations",
        "landing": "landing",
    },
    "fr": {
        "orte": "lieux",
        "lieux": "lieux",
        "landing": "landing",
    },
    "pt": {
        "orte": "locais",
        "locais": "locais",
        "landing": "landing",
    },
}

VALID_LANGS = {"de", "en", "fr", "pt"}

def build_target_path(parts_after_lang, target_lang):
    mapped = []
    for part in parts_after_lang:
        mapped.append(SECTION_MAP.get(target_lang, {}).get(part, part))
    return f"/{target_lang}/" + "/".join(mapped) + "/"

def get_langlinks_for_file(path: Path):
    rel = path.relative_to(ROOT)
    parts = list(rel.parts)

    if len(parts) < 2:
        return None

    lang = parts[0]
    if lang not in VALID_LANGS:
        return None

    # nur index.njk bearbeiten
    if parts[-1] != "index.njk":
        return None

    # Pfadteile nach Sprache, ohne index.njk
    parts_after_lang = parts[1:-1]

    # Startseiten: src/de/index.njk etc.
    if not parts_after_lang:
        return {
            "de": "/de/",
            "en": "/en/",
            "fr": "/fr/",
            "pt": "/pt/",
        }

    return {
        "de": build_target_path(parts_after_lang, "de"),
        "en": build_target_path(parts_after_lang, "en"),
        "fr": build_target_path(parts_after_lang, "fr"),
        "pt": build_target_path(parts_after_lang, "pt"),
    }

def replace_langlinks_block(text, langlinks):
    new_block = (
        "langLinks:\n"
        f"  de: {langlinks['de']}\n"
        f"  en: {langlinks['en']}\n"
        f"  fr: {langlinks['fr']}\n"
        f"  pt: {langlinks['pt']}"
    )

    pattern = re.compile(
        r"langLinks:\n(?:[ \t]+de:.*\n)?(?:[ \t]+en:.*\n)?(?:[ \t]+fr:.*\n)?(?:[ \t]+pt:.*\n?)?",
        re.MULTILINE
    )

    if pattern.search(text):
        return pattern.sub(new_block + "\n", text, count=1)

    # Falls kein langLinks-Block existiert: direkt nach permalink einfügen
    permalink_pattern = re.compile(r"(permalink:\s*.*\n)", re.MULTILINE)
    if permalink_pattern.search(text):
        return permalink_pattern.sub(r"\1\n" + new_block + "\n", text, count=1)

    return text

def main():
    changed = []

    for path in ROOT.rglob("index.njk"):
        langlinks = get_langlinks_for_file(path)
        if not langlinks:
            continue

        original = path.read_text(encoding="utf-8")
        updated = replace_langlinks_block(original, langlinks)

        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="")
            changed.append(str(path))

    print("\n=== FIXED LANGLINKS ===\n")
    if changed:
        for item in changed:
            print(item)
    else:
        print("Keine Änderungen notwendig.")

if __name__ == "__main__":
    main()