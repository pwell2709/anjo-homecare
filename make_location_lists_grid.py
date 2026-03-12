from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = [
    ROOT / "src/de/orte/index.njk",
    ROOT / "src/en/locations/index.njk",
    ROOT / "src/fr/lieux/index.njk",
    ROOT / "src/pt/locais/index.njk",
]

CSS_FILE = ROOT / "src/assets/css/components.css"

OLD = '<ul class="sectionList">'
NEW = '<ul class="sectionList sectionList--locationsGrid">'

CSS_PATCH = """

/* === LOCATION OVERVIEW GRID === */
.prose-page ul.sectionList.sectionList--locationsGrid{
  list-style: none;
  padding-left: 0;
  margin: 1.2rem 0 1.4rem 0;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px 18px;
}

.prose-page ul.sectionList.sectionList--locationsGrid li{
  margin: 0;
}

.prose-page ul.sectionList.sectionList--locationsGrid li + li{
  margin-top: 0;
}

.prose-page ul.sectionList.sectionList--locationsGrid a.cta-link{
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 54px;
  width: 100%;
  text-align: center;
  padding: 12px 14px;
  box-sizing: border-box;
}

@media (max-width: 980px){
  .prose-page ul.sectionList.sectionList--locationsGrid{
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 720px){
  .prose-page ul.sectionList.sectionList--locationsGrid{
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
}

@media (max-width: 480px){
  .prose-page ul.sectionList.sectionList--locationsGrid{
    grid-template-columns: 1fr;
  }
}
""".strip() + "\n"


def patch_templates():
    changed = 0
    for file_path in FILES:
        text = file_path.read_text(encoding="utf-8")
        if NEW in text:
            print(f"SKIP template already patched: {file_path}")
            continue
        if OLD not in text:
            print(f"MISS target not found: {file_path}")
            continue
        text = text.replace(OLD, NEW, 1)
        file_path.write_text(text, encoding="utf-8", newline="\n")
        print(f"OK   template patched: {file_path}")
        changed += 1
    return changed


def patch_css():
    text = CSS_FILE.read_text(encoding="utf-8")
    marker = "/* === LOCATION OVERVIEW GRID === */"
    if marker in text:
        print("SKIP CSS already patched")
        return False
    text = text.rstrip() + "\n\n" + CSS_PATCH
    CSS_FILE.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK   CSS patched: {CSS_FILE}")
    return True


def main():
    tpl_changed = patch_templates()
    css_changed = patch_css()
    print(f"\nDone. Templates changed: {tpl_changed}, CSS changed: {1 if css_changed else 0}")


if __name__ == "__main__":
    main()