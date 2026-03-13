from pathlib import Path
import sys


PRELOAD_BLOCK = """  <link rel="preload" as="image" href="/assets/images/background.webp" media="(min-width: 821px)">
  <link rel="preload" as="image" href="/assets/images/backgroundm.webp" media="(max-width: 820px)">
"""


def main() -> None:
    path = Path("src/layouts/base.njk")
    if not path.exists():
        raise FileNotFoundError("src/layouts/base.njk nicht gefunden")

    text = path.read_text(encoding="utf-8")

    if '/assets/images/background.webp" media="(min-width: 821px)"' in text:
        print("Preload bereits vorhanden.")
        return

    marker = '  <link rel="stylesheet" href="/assets/css/base.css">'
    if marker not in text:
        raise RuntimeError("Einfügepunkt für Preload nicht gefunden")

    text = text.replace(marker, PRELOAD_BLOCK + marker, 1)

    path.write_text(text, encoding="utf-8", newline="\n")
    print("OK: Background-Preload eingefügt")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)