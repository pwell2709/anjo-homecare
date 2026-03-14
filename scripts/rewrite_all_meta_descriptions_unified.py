#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT_404 = "404.njk"

LOCATION_NAMES = OrderedDict([
    ("boaventura", {"de": "Boaventura", "en": "Boaventura", "fr": "Boaventura", "pt": "Boaventura"}),
    ("calheta", {"de": "Calheta", "en": "Calheta", "fr": "Calheta", "pt": "Calheta"}),
    ("camara-de-lobos", {"de": "Câmara de Lobos", "en": "Câmara de Lobos", "fr": "Câmara de Lobos", "pt": "Câmara de Lobos"}),
    ("campanario", {"de": "Campanário", "en": "Campanário", "fr": "Campanário", "pt": "Campanário"}),
    ("canico", {"de": "Caniço", "en": "Caniço", "fr": "Caniço", "pt": "Caniço"}),
    ("curral-das-freiras", {"de": "Curral das Freiras", "en": "Curral das Freiras", "fr": "Curral das Freiras", "pt": "Curral das Freiras"}),
    ("funchal", {"de": "Funchal", "en": "Funchal", "fr": "Funchal", "pt": "Funchal"}),
    ("jardim-do-mar", {"de": "Jardim do Mar", "en": "Jardim do Mar", "fr": "Jardim do Mar", "pt": "Jardim do Mar"}),
    ("paul-do-mar", {"de": "Paul do Mar", "en": "Paul do Mar", "fr": "Paul do Mar", "pt": "Paul do Mar"}),
    ("ponta-do-pargo", {"de": "Ponta do Pargo", "en": "Ponta do Pargo", "fr": "Ponta do Pargo", "pt": "Ponta do Pargo"}),
    ("ponta-do-sol", {"de": "Ponta do Sol", "en": "Ponta do Sol", "fr": "Ponta do Sol", "pt": "Ponta do Sol"}),
    ("porto-moniz", {"de": "Porto Moniz", "en": "Porto Moniz", "fr": "Porto Moniz", "pt": "Porto Moniz"}),
    ("ribeira-brava", {"de": "Ribeira Brava", "en": "Ribeira Brava", "fr": "Ribeira Brava", "pt": "Ribeira Brava"}),
    ("santa-cruz", {"de": "Santa Cruz", "en": "Santa Cruz", "fr": "Santa Cruz", "pt": "Santa Cruz"}),
    ("santana", {"de": "Santana", "en": "Santana", "fr": "Santana", "pt": "Santana"}),
    ("sao-jorge", {"de": "São Jorge", "en": "São Jorge", "fr": "São Jorge", "pt": "São Jorge"}),
    ("sao-vicente", {"de": "São Vicente", "en": "São Vicente", "fr": "São Vicente", "pt": "São Vicente"}),
])

BASE_DESCRIPTIONS = {
    ROOT_404: "The requested page could not be found.",
    "de/404/index.njk": "Die angeforderte Seite konnte nicht gefunden werden.",
    "de/about/index.njk": "Über Anjo Property Care Madeira, unsere Standards und die Betreuung hochwertiger Immobilien für internationale Eigentümer.",
    "de/check/index.njk": "Storm Check auf Madeira für Villen und Zweitwohnsitze nach Sturm, Starkregen und Wind mit klarer Rückmeldung.",
    "de/contact/index.njk": "Kontakt für Property Care, Reinigungen und Objektbetreuung auf Madeira mit klaren Abläufen und verlässlicher Antwort.",
    "de/faq/index.njk": "Fragen zu Property Care auf Madeira, Services, Storm Check und ausgewählter Betreuung für Eigentümer und Residenzen.",
    "de/home/index.njk": "Property Care auf Madeira für Villen und hochwertige Wohnungen mit diskreten Kontrollen und verlässlicher Betreuung.",
    "de/index.njk": "Luxury Property Care auf Madeira für Villen und hochwertige Wohnungen mit diskreter Kontrolle und Vorbereitung.",
    "de/landing/alto/index.njk": "Reinigung für Alojamento Local auf Madeira mit strukturierter Vorbereitung und verlässlicher Umsetzung zwischen Buchungen.",
    "de/legal/index.njk": "Impressum von Anjo Property Care Madeira mit Anbieterangaben, Kontaktdaten und rechtlichen Informationen.",
    "de/orte/index.njk": "Property Care auf Madeira, abgestimmt auf Regionen, Mikroklima und die Anforderungen hochwertiger Immobilien.",
    "de/privacy/index.njk": "Datenschutzerklärung von Anjo Property Care Madeira zu Datenverarbeitung, Kontaktanfragen und Nutzerrechten.",
    "de/services/index.njk": "Exklusive Services auf Madeira mit Reinigung, Pflege und diskreter Ausführung als Ergänzung zu Property Care.",
    "en/404/index.njk": "The requested page could not be found.",
    "en/about/index.njk": "About Anjo Property Care Madeira, our standards and how we protect high-end properties for international owners.",
    "en/check/index.njk": "Storm Check in Madeira for villas and second homes after storms, heavy rain and wind with clear owner feedback.",
    "en/contact/index.njk": "Contact for Property Care, cleaning and property support in Madeira with clear processes and reliable response.",
    "en/faq/index.njk": "Questions about Property Care in Madeira, additional services, storm checks and selected support for owners.",
    "en/home/index.njk": "Property Care in Madeira for villas and premium apartments with discreet checks and reliable supervision.",
    "en/index.njk": "Luxury Property Care in Madeira for villas and premium apartments with discreet supervision and preparation.",
    "en/landing/alto/index.njk": "Cleaning for Alojamento Local in Madeira with structured preparation and reliable changeovers between guest stays.",
    "en/legal/index.njk": "Legal notice for Anjo Property Care Madeira with provider details, contact data and legal information.",
    "en/locations/index.njk": "Property Care across Madeira, adapted to each region, microclimate and high-end property profile.",
    "en/privacy/index.njk": "Privacy policy of Anjo Property Care Madeira covering data processing, contact requests and user rights.",
    "en/services/index.njk": "Exclusive services in Madeira with premium cleaning, careful upkeep and discreet execution beside Property Care.",
    "fr/404/index.njk": "La page demandée est introuvable.",
    "fr/about/index.njk": "Présentation d’Anjo Property Care Madère, de nos standards et de notre suivi des propriétés haut de gamme.",
    "fr/check/index.njk": "Storm Check à Madère pour villas et résidences secondaires après tempête, fortes pluies et vent.",
    "fr/contact/index.njk": "Contact pour Property Care, nettoyage et suivi de propriété à Madère avec processus clairs et réponse fiable.",
    "fr/faq/index.njk": "Questions sur le Property Care à Madère, les services, le Storm Check et l’accompagnement des propriétaires.",
    "fr/home/index.njk": "Property Care à Madère pour villas et appartements haut de gamme avec contrôles discrets et suivi fiable.",
    "fr/index.njk": "Luxury Property Care à Madère pour villas et appartements haut de gamme avec contrôle discret et préparation.",
    "fr/landing/alto/index.njk": "Nettoyage pour Alojamento Local à Madère avec préparation structurée et exécution fiable entre deux séjours.",
    "fr/legal/index.njk": "Mentions légales d’Anjo Property Care Madère avec données du prestataire, contacts et informations juridiques.",
    "fr/lieux/index.njk": "Property Care à Madère selon les régions, le microclimat et les exigences des propriétés haut de gamme.",
    "fr/privacy/index.njk": "Politique de confidentialité d’Anjo Property Care Madère sur les données, les demandes de contact et les droits.",
    "fr/services/index.njk": "Services exclusifs à Madère avec nettoyage soigné, entretien précis et exécution discrète.",
    "pt/404/index.njk": "A página solicitada não foi encontrada.",
    "pt/about/index.njk": "Sobre a Anjo Property Care Madeira, os nossos padrões e a proteção de propriedades de alto padrão.",
    "pt/check/index.njk": "Storm Check na Madeira para moradias e segundas residências após tempestade, chuva forte e vento.",
    "pt/contact/index.njk": "Contacto para Property Care, limpeza e apoio ao imóvel na Madeira com processos claros e resposta fiável.",
    "pt/faq/index.njk": "Perguntas sobre Property Care na Madeira, serviços, Storm Check e apoio selecionado para proprietários.",
    "pt/home/index.njk": "Property Care na Madeira para moradias e apartamentos de alto padrão com controlo discreto e acompanhamento.",
    "pt/index.njk": "Luxury Property Care na Madeira para moradias e apartamentos de luxo com controlo discreto e preparação.",
    "pt/landing/alto/index.njk": "Limpeza para Alojamento Local na Madeira com preparação estruturada e execução fiável entre reservas.",
    "pt/legal/index.njk": "Aviso legal da Anjo Property Care Madeira com dados do prestador, contactos e informações jurídicas.",
    "pt/locais/index.njk": "Property Care na Madeira ajustado a cada região, microclima e perfil de imóvel de alto padrão.",
    "pt/privacy/index.njk": "Política de privacidade da Anjo Property Care Madeira sobre dados, pedidos de contacto e direitos.",
    "pt/services/index.njk": "Serviços exclusivos na Madeira com limpeza cuidada, manutenção e execução discreta com Property Care.",
}

DESCRIPTION_LINE_RE = re.compile(r"(?m)^(description:\s*)(.*)$")
DIRECT_META_RE = re.compile(r"^[ \t]*<meta\s+name=['\"]description['\"]\s+content=.*?>\s*\n?", re.IGNORECASE | re.MULTILINE)
MAX_LEN = 135


def build_descriptions() -> dict[str, str]:
    descriptions = dict(BASE_DESCRIPTIONS)

    for slug, names in LOCATION_NAMES.items():
        descriptions[f"de/orte/{slug}/index.njk"] = (
            f"Property Care in {names['de']} auf Madeira für hochwertige Residenzen mit diskreten Kontrollen und verlässlicher Betreuung."
        )
        descriptions[f"en/locations/{slug}/index.njk"] = (
            f"Property Care in {names['en']}, Madeira for high-end residences with discreet checks and reliable supervision."
        )
        descriptions[f"fr/lieux/{slug}/index.njk"] = (
            f"Property Care à {names['fr']}, Madère pour résidences haut de gamme avec contrôles discrets et suivi fiable."
        )
        descriptions[f"pt/locais/{slug}/index.njk"] = (
            f"Property Care em {names['pt']}, Madeira para residências de alto padrão com controlo discreto e acompanhamento."
        )

    return descriptions


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def replace_description_line(text: str, new_description: str, rel_path: str) -> str:
    replacement = rf"\1{yaml_quote(new_description)}"
    new_text, count = DESCRIPTION_LINE_RE.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"description line not found or ambiguous in {rel_path}")
    return new_text


def remove_direct_meta_descriptions(text: str) -> tuple[str, int]:
    return DIRECT_META_RE.subn("", text)


def validate_project(src_dir: Path, descriptions: dict[str, str]) -> None:
    files_with_description = []
    offending_lengths = []
    direct_meta_outside_layout = []
    missing_targets = []
    unexpected_targets = []

    for path in sorted(src_dir.rglob("*.njk")):
        rel = path.relative_to(src_dir).as_posix()
        text = path.read_text(encoding="utf-8")

        if rel != "layouts/base.njk" and re.search(r'<meta\s+name=["\']description["\']', text, re.IGNORECASE):
            direct_meta_outside_layout.append(rel)

        match = DESCRIPTION_LINE_RE.search(text)
        if match:
            files_with_description.append(rel)
            raw = match.group(2).strip()
            value = raw
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
                value = value.replace('\\"', '"').replace('\\\\', '\\')
            if len(value) > MAX_LEN:
                offending_lengths.append((rel, len(value), value))

    expected = set(descriptions)
    actual = set(files_with_description)
    missing_targets = sorted(expected - actual)
    unexpected_targets = sorted(actual - expected)

    if missing_targets:
        raise RuntimeError(f"Expected description targets missing: {missing_targets}")
    if unexpected_targets:
        raise RuntimeError(f"Unexpected described templates found: {unexpected_targets}")
    if offending_lengths:
        sample = "\n".join(f"- {rel} ({length}) {value}" for rel, length, value in offending_lengths[:10])
        raise RuntimeError(f"Descriptions over {MAX_LEN} chars found:\n{sample}")
    if direct_meta_outside_layout:
        raise RuntimeError(
            "Direct <meta name=\"description\"> tags found outside src/layouts/base.njk: "
            + ", ".join(direct_meta_outside_layout)
        )


def main() -> int:
    project_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    src_dir = project_root / "src"

    if not src_dir.is_dir():
        raise SystemExit(f"src folder not found: {src_dir}")

    descriptions = build_descriptions()
    for rel, description in descriptions.items():
        if len(description) > MAX_LEN:
            raise RuntimeError(f"Description too long ({len(description)}): {rel} -> {description}")

    updated_files = 0
    removed_meta_tags = 0

    for rel, description in sorted(descriptions.items()):
        path = src_dir / rel
        if not path.is_file():
            raise RuntimeError(f"Target file not found: {rel}")

        original = path.read_text(encoding="utf-8")
        rewritten = replace_description_line(original, description, rel)
        rewritten, removed_count = remove_direct_meta_descriptions(rewritten)
        removed_meta_tags += removed_count

        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8", newline="\n")
            updated_files += 1

    validate_project(src_dir, descriptions)

    print(f"Updated {updated_files} templates.")
    print(f"Validated {len(descriptions)} descriptions at max {MAX_LEN} characters.")
    print(f"Removed {removed_meta_tags} direct meta description tag(s) outside the shared layout.")
    print("Description output is now standardized through frontmatter + src/layouts/base.njk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
