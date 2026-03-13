from pathlib import Path
import re
import sys


NEW_CSP = '''Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self' https://www.googletagmanager.com; frame-src https://www.googletagmanager.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self';"'''


def main() -> None:
    path = Path("src/.htaccess")
    if not path.exists():
        raise FileNotFoundError("src/.htaccess nicht gefunden")

    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r'Header always set Content-Security-Policy\s+"(?:[^"\\]|\\.|[\r\n])*?"',
        re.MULTILINE,
    )

    if not pattern.search(text):
        raise RuntimeError("Content-Security-Policy Eintrag nicht gefunden")

    updated = pattern.sub(NEW_CSP, text, count=1)

    path.write_text(updated, encoding="utf-8", newline="\n")
    print("OK: CSP für aktuellen Header aktualisiert")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)