from pathlib import Path
import sys

TARGET = Path("src/_includes/components/header.njk")

REPLACEMENTS = {
    'href="{{ langLinks.en or \'/en/\' }}"': 'href="{{ langLinks.en }}"',
    'data-href="{{ langLinks.en or \'/en/\' }}"': 'data-href="{{ langLinks.en }}"',

    'href="{{ langLinks.de or \'/de/\' }}"': 'href="{{ langLinks.de }}"',
    'data-href="{{ langLinks.de or \'/de/\' }}"': 'data-href="{{ langLinks.de }}"',

    'href="{{ langLinks.fr or \'/fr/\' }}"': 'href="{{ langLinks.fr }}"',
    'data-href="{{ langLinks.fr or \'/fr/\' }}"': 'data-href="{{ langLinks.fr }}"',

    'href="{{ langLinks.pt or \'/pt/\' }}"': 'href="{{ langLinks.pt }}"',
    'data-href="{{ langLinks.pt or \'/pt/\' }}"': 'data-href="{{ langLinks.pt }}"',
}


def main():
    if not TARGET.exists():
        raise FileNotFoundError("header.njk nicht gefunden")

    text = TARGET.read_text(encoding="utf-8")

    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    TARGET.write_text(text, encoding="utf-8", newline="\n")

    print("OK: Language switcher fallbacks entfernt")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FEHLER:", e)
        sys.exit(1)