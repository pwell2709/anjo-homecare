from pathlib import Path
import re
import sys


def main():
    path = Path("src/layouts/base.njk")

    if not path.exists():
        print("base.njk nicht gefunden")
        return

    text = path.read_text(encoding="utf-8")

    print("\nCSS Dateien:")
    css = re.findall(r'<link rel="stylesheet" href="([^"]+)"', text)
    for c in css:
        print(" ", c)

    print("\nBackground Bilder:")
    bg = re.findall(r'background-image:\s*url\("([^"]+)"\)', text)
    for b in bg:
        print(" ", b)

    print("\nBereits vorhandene Preloads:")
    pre = re.findall(r'<link rel="preload"[^>]+href="([^"]+)"', text)
    for p in pre:
        print(" ", p)

    if not pre:
        print("  keine")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fehler:", e)
        sys.exit(1)