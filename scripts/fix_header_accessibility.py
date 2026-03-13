from pathlib import Path
import sys

FILE = Path("src/_includes/components/header.njk")

def main():
    if not FILE.exists():
        raise FileNotFoundError("header.njk nicht gefunden")

    text = FILE.read_text(encoding="utf-8")

    # div -> nav für Language Switch
    text = text.replace(
        '<div class="lang-switch" aria-label="Language switch">',
        '<nav class="lang-switch" aria-label="Language switch">'
    )

    text = text.replace(
        '</div>\n    <a class="brand"',
        '</nav>\n    <a class="brand"'
    )

    # Brand aria-label präzisieren
    text = text.replace(
        'aria-label="Home"',
        'aria-label="Anjo Property Care home"'
    )

    # Logo alt leeren (weil Link bereits benannt ist)
    text = text.replace(
        'alt="Anjo Property Care"',
        'alt=""'
    )

    FILE.write_text(text, encoding="utf-8", newline="\n")

    print("OK: Header Accessibility verbessert")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FEHLER:", e)
        sys.exit(1)