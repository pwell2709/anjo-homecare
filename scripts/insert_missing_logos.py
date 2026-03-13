from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

FILES = [
    "src/de/about/index.njk",
    "src/de/faq/index.njk",
    "src/de/legal/index.njk",
    "src/de/privacy/index.njk",
    "src/de/landing/alto/index.njk",
    "src/en/about/index.njk",
    "src/en/faq/index.njk",
    "src/en/legal/index.njk",
    "src/en/privacy/index.njk",
    "src/fr/about/index.njk",
    "src/fr/faq/index.njk",
    "src/fr/legal/index.njk",
    "src/fr/privacy/index.njk",
    "src/fr/landing/alto/index.njk",
    "src/pt/about/index.njk",
    "src/pt/faq/index.njk",
    "src/pt/legal/index.njk",
    "src/pt/privacy/index.njk",
    "src/pt/landing/alto/index.njk",
]

LOGO_SMALL = """
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
"""

LOGO_LANDING = """
  <div class="hero-logo hero-logo--landing">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
"""

SECTION_OPEN_RE = re.compile(r"(<section\b[^>]*>)", re.IGNORECASE)


def insert_logo_into_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    if "hero-logo" in text:
        print(f"SKIP  already has logo: {path}")
        return False

    logo_block = LOGO_LANDING if "landing/alto" in path.as_posix() else LOGO_SMALL

    match = SECTION_OPEN_RE.search(text)
    if not match:
        print(f"ERROR no <section> found: {path}")
        return False

    insert_at = match.end()
    new_text = text[:insert_at] + "\n" + logo_block + text[insert_at:]

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"OK    inserted logo: {path}")
    return True


def main():
    changed = 0

    for rel in FILES:
        file_path = ROOT / rel
        if not file_path.exists():
            print(f"MISS  file not found: {file_path}")
            continue

        if insert_logo_into_file(file_path):
            changed += 1

    print(f"\nDone. Changed files: {changed}")


if __name__ == "__main__":
    main()