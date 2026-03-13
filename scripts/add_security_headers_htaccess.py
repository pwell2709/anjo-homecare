from pathlib import Path

SECURITY_BLOCK = """

# Security Headers

<IfModule mod_headers.c>

Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"

Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"

Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

Header always set Content-Security-Policy "
default-src 'self';
img-src 'self' data:;
script-src 'self';
style-src 'self';
font-src 'self';
connect-src 'self';
frame-ancestors 'self';
base-uri 'self';
form-action 'self';
"

</IfModule>

"""


def main():
    path = Path("src/.htaccess")

    if not path.exists():
        raise FileNotFoundError("src/.htaccess nicht gefunden")

    text = path.read_text(encoding="utf-8")

    if "Content-Security-Policy" in text:
        print("Security Headers bereits vorhanden.")
        return

    new_text = text.rstrip() + "\n" + SECURITY_BLOCK

    path.write_text(new_text, encoding="utf-8")

    print("OK: Security Headers zu .htaccess hinzugefügt")


if __name__ == "__main__":
    main()