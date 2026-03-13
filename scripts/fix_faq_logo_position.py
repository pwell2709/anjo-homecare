from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

FAQ_FILES = [
    "src/de/faq/index.njk",
    "src/en/faq/index.njk",
    "src/fr/faq/index.njk",
    "src/pt/faq/index.njk",
]

LOGO_BLOCK = """
<div class="hero-logo hero-logo--small">
  <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
</div>
""".strip()

# entfernt jeden hero-logo-Block vollständig, egal wo er aktuell sitzt
HERO_LOGO_RE = re.compile(
    r'\s*<div class="hero-logo hero-logo--(?:small|landing)">\s*'
    r'<img[^>]*src="/assets/images/logo\.svg"[^>]*>\s*'
    r'</div>\s*',
    re.IGNORECASE | re.DOTALL
)

def fix_file(rel_path: str) -> None:
    path = ROOT / rel_path
    if not path.exists():
        print(f"FEHLT : {rel_path}")
        return

    text = path.read_text(encoding="utf-8")

    # 1) alte/falsch platzierte Logos entfernen
    text = HERO_LOGO_RE.sub("\n", text)

    # 2) exakter Insert-Punkt: direkt nach </style>, vor faq-wrap
    anchor = "</style>\n\n<div class=\"faq-wrap\">"
    if anchor in text:
        text = text.replace(
            anchor,
            f"</style>\n\n{LOGO_BLOCK}\n\n<div class=\"faq-wrap\">",
            1
        )
    else:
        # Fallback, falls Zeilenumbrüche anders sind
        m = re.search(r"(</style>\s*)(<div class=\"faq-wrap\">)", text, re.IGNORECASE)
        if not m:
            print(f"KEIN ANKER: {rel_path}")
            return
        text = text[:m.start()] + m.group(1) + LOGO_BLOCK + "\n\n" + m.group(2) + text[m.end():]

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK    : {rel_path}")

def main():
    for rel_path in FAQ_FILES:
        fix_file(rel_path)

if __name__ == "__main__":
    main()