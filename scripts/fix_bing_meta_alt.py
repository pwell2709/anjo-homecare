from pathlib import Path
import re

ROOT = Path("src")

# 1) Neue, kürzere Home-Descriptions für alle 4 Sprachen
HOME_DESCRIPTIONS = {
    "src/en/index.njk": "Luxury Property Care in Madeira for international owners: discreet supervision of villas and high-end apartments with reliable inspections, preparation and premium services.",
    "src/de/index.njk": "Luxury Property Care auf Madeira für internationale Eigentümer: diskrete Betreuung von Villen und hochwertigen Apartments mit verlässlichen Kontrollen, Vorbereitung und Premium-Services.",
    "src/fr/index.njk": "Luxury Property Care à Madère pour propriétaires internationaux : supervision discrète de villas et d’appartements haut de gamme avec contrôles, préparation et services premium.",
    "src/pt/index.njk": "Luxury Property Care na Madeira para proprietários internacionais: acompanhamento discreto de moradias e apartamentos de alto padrão com controlo, preparação e serviços premium.",
}

def replace_frontmatter_description(path: Path, new_description: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(
        r'(?m)^description:\s*"[^"]*"$',
        f'description: "{new_description}"',
        text,
        count=1,
    )
    if count:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False

changed = []

# 1) Home-Descriptions in DE/EN/FR/PT kürzen
for file_path, new_desc in HOME_DESCRIPTIONS.items():
    path = Path(file_path)
    if path.exists() and replace_frontmatter_description(path, new_desc):
        changed.append(f"UPDATED description: {file_path}")

# 2) Leeres Alt im Header-Logo projektweit bereinigen
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix.lower() not in {".njk", ".html", ".md"}:
        continue

    text = path.read_text(encoding="utf-8")

    new_text = text

    # Leeres Logo-Alt -> Markenname
    new_text = new_text.replace(
        '<img src="/assets/images/logo.svg" alt="" class="site-logo">',
        '<img src="/assets/images/logo.svg" alt="Anjo Property Care Madeira" class="site-logo">'
    )

    # Vorhandene alte Logo-Alts vereinheitlichen
    new_text = new_text.replace(
        'alt="Anjo Cleaning Logo"',
        'alt="Anjo Property Care Madeira"'
    )

    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        changed.append(f"UPDATED alt: {path.as_posix()}")

print("\n".join(changed) if changed else "No changes made.")
print("\nDone.")