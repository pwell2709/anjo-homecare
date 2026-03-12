from pathlib import Path

ROOT = Path(__file__).resolve().parent

BASE_FILE = ROOT / "src" / "layouts" / "base.njk"
STYLE_FILE = ROOT / "src" / "assets" / "css" / "style.css"

NEW_CTA_BLOCK = """  {% include "components/cta.njk" %}
"""

CTA_WIDTH_PATCH = """
/* === GLOBAL CTA UNIFICATION === */
.ctaInner{
  gap: 16px;
}

.ctaInner .ctaBtn{
  width: clamp(190px, 22vw, 250px);
  min-height: 52px;
  justify-content: center;
  text-align: center;
  white-space: nowrap;
}

@media (max-width: 820px){
  .ctaInner .ctaBtn{
    width: min(44vw, 220px);
    min-height: 50px;
    font-size: 17px;
  }
}

@media (max-width: 520px){
  .ctaInner{
    gap: 10px;
  }

  .ctaInner .ctaBtn{
    width: min(44vw, 200px);
    min-height: 48px;
    font-size: 16px;
    padding: 10px 10px;
  }

  .ctaBtn--wa .ctaBtnIcon{
    width: 20px;
    height: 20px;
  }

  .ctaBtn--wa svg{
    width: 20px;
    height: 20px;
  }
}
""".strip() + "\n"


def patch_base():
    text = BASE_FILE.read_text(encoding="utf-8")

    old_block = """  {% set showCta = false %}
  {% if page.url %}
    {% set isMainIndex = page.url == ("/" + pageLang + "/") %}
    {% set isContact = page.url.indexOf("/" + pageLang + "/contact/") == 0 %}
    {% set localizedAlRoot = {"de":"/de/landing/alto/","en":"/en/landing/alto/","fr":"/fr/landing/alto/","pt":"/pt/landing/alto/"} %}
    {% set isAl = false %}
    {% set isCheck = page.url.indexOf("/" + pageLang + "/check/") == 0 %}
    {% set localizedAreaRoots = {"de":"/de/orte/","en":"/en/locations/","fr":"/fr/lieux/","pt":"/pt/locais/"} %}
    {% set isAreas = page.url.indexOf(localizedAreaRoots[pageLang]) == 0 %}
    {% if isMainIndex or isContact or isAl or isCheck or isAreas %}{% set showCta = true %}{% endif %}
  {% endif %}
  {% if showCta %}
    {% include "components/cta.njk" %}
  {% endif %}
"""

    if old_block in text:
        text = text.replace(old_block, NEW_CTA_BLOCK, 1)
    elif '{% include "components/cta.njk" %}' not in text:
        anchor = '  {% include "components/cookie.njk" %}\n'
        if anchor not in text:
            raise RuntimeError("CTA-Anker in base.njk nicht gefunden.")
        text = text.replace(anchor, anchor + "\n" + NEW_CTA_BLOCK, 1)

    BASE_FILE.write_text(text, encoding="utf-8", newline="\n")
    print("OK  base.njk aktualisiert")


def patch_style():
    text = STYLE_FILE.read_text(encoding="utf-8")

    marker = "/* === GLOBAL CTA UNIFICATION === */"
    if marker in text:
        print("SKIP style.css bereits gepatcht")
        return

    text = text.rstrip() + "\n\n" + CTA_WIDTH_PATCH
    STYLE_FILE.write_text(text, encoding="utf-8", newline="\n")
    print("OK  style.css aktualisiert")


def main():
    patch_base()
    patch_style()
    print("\nFertig.")


if __name__ == "__main__":
    main()