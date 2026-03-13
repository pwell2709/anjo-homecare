import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

KEY = "bc6804864a4843a69ad0db3720f2c215"
HOST = "anjo-cleaning.com"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def fetch_sitemap(url: str) -> list[str]:
    with urllib.request.urlopen(url, timeout=30) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls = []
    for loc in root.findall("sm:url/sm:loc", ns):
        value = (loc.text or "").strip()
        if value:
            urls.append(value)

    # Duplikate entfernen, Reihenfolge behalten
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    return unique_urls


def send_indexnow(urls: list[str]) -> tuple[int, str]:
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8", errors="replace")
        return status_code, body


def main() -> int:
    try:
        urls = fetch_sitemap(SITEMAP_URL)
    except Exception as exc:
        print(f"FEHLER beim Laden der Sitemap: {exc}")
        return 1

    if not urls:
        print("Keine URLs in der Sitemap gefunden.")
        return 1

    print(f"{len(urls)} URLs aus der Sitemap geladen.")
    print("Erste 5 URLs:")
    for u in urls[:5]:
        print(f" - {u}")

    try:
        status_code, body = send_indexnow(urls)
    except Exception as exc:
        print(f"FEHLER beim Senden an IndexNow: {exc}")
        return 1

    print(f"\nIndexNow Antwortcode: {status_code}")
    if body.strip():
        print("Antwort:")
        print(body)
    else:
        print("Keine Response-Body-Inhalte zurückgegeben.")

    return 0


if __name__ == "__main__":
    sys.exit(main())