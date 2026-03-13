from pathlib import Path
import re
import sys

NEW_BLOCK = """  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/theme.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/style.css">
  <link rel="stylesheet" href="/assets/css/cta-icons.css">"""


def main() -> None:
    path = Path("src/layouts/base.njk")
    if not path.exists():
        raise FileNotFoundError("src/layouts/base.njk nicht gefunden")

    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r'  <link rel="stylesheet" href="/assets/css/base\.css">\n'
        r'  <link rel="stylesheet" href="/assets/css/components\.css">\n'
        r'  <link rel="stylesheet" href="/assets/css/cta-icons\.css">\n'
        r'  <link rel="stylesheet" href="/assets/css/style\.css">\n'
        r'  <link rel="stylesheet" href="/assets/css/theme\.css">'
    )

    if not pattern.search(text):
        raise RuntimeError("Erwarteter CSS-Block nicht gefunden")

    text = pattern.sub(NEW_BLOCK, text, count=1)

    path.write_text(text, encoding="utf-8", newline="\n")
    print("OK: CSS-Reihenfolge angepasst")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)