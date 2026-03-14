#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rewrites all page meta descriptions to max. 135 characters,
excluding only /de/, /en/, /fr/ and /pt/.

Run from the project root, e.g.:
    python scripts/rewrite_meta_descriptions_135.py
or:
    python rewrite_meta_descriptions_135.py
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

DESCRIPTION_MAP = {
  "src/404.njk": "The requested page could not be found. Return to the overview or contact Anjo Property Care Madeira.",
  "src/de/404/index.njk": "Die gesuchte Seite wurde nicht gefunden. Zur Übersicht zurückkehren oder Anjo Property Care Madeira kontaktieren.",
  "src/en/404/index.njk": "The requested page could not be found. Return to the overview or contact Anjo Property Care Madeira.",
  "src/fr/404/index.njk": "La page demandée est introuvable. Revenez à l’accueil ou contactez Anjo Property Care Madeira.",
  "src/pt/404/index.njk": "A página pedida não foi encontrada. Volte ao início ou contacte a Anjo Property Care Madeira.",
  "src/de/about/index.njk": "Erfahren Sie, wie Anjo hochwertige Immobilien auf Madeira mit klaren Abläufen, Diskretion und konstantem Standard betreut.",
  "src/en/about/index.njk": "Learn how Anjo cares for high-end properties in Madeira with clear processes, discretion and consistent standards.",
  "src/fr/about/index.njk": "Découvrez comment Anjo prend soin des biens haut de gamme à Madère avec méthode, discrétion et constance.",
  "src/pt/about/index.njk": "Saiba como a Anjo cuida de imóveis de alto padrão na Madeira com processos claros, discrição e consistência.",
  "src/de/check/index.njk": "Storm Check auf Madeira: Kontrolle nach Unwetter, Starkregen oder Wind mit klarer Rückmeldung für Eigentümer.",
  "src/en/check/index.njk": "Storm Check in Madeira with post-storm property checks and clear reporting for owners of high-end homes.",
  "src/fr/check/index.njk": "Storm Check à Madère avec contrôle après intempéries et retour clair pour les propriétaires.",
  "src/pt/check/index.njk": "Storm Check na Madeira com verificação após tempestade e retorno claro para proprietários.",
  "src/de/contact/index.njk": "Kontakt für Property Care, Reinigungen und Objektbetreuung auf Madeira. Klare Abläufe, schnelle Rückmeldung.",
  "src/en/contact/index.njk": "Contact us for property care, cleaning and home oversight in Madeira. Clear process and prompt response.",
  "src/fr/contact/index.njk": "Contact pour property care, nettoyage et suivi de résidence à Madère. Processus clair et réponse rapide.",
  "src/pt/contact/index.njk": "Contacto para property care, limpeza e acompanhamento do imóvel na Madeira. Processo claro e resposta rápida.",
  "src/de/faq/index.njk": "Antworten zu Property Care, Reinigungen, Storm Check und Abläufen für Eigentümer hochwertiger Immobilien auf Madeira.",
  "src/en/faq/index.njk": "Answers on property care, cleaning, storm checks and service processes for owners of high-end homes in Madeira.",
  "src/fr/faq/index.njk": "Réponses sur le property care, le nettoyage, le Storm Check et le fonctionnement du service à Madère.",
  "src/pt/faq/index.njk": "Respostas sobre property care, limpeza, Storm Check e funcionamento do serviço na Madeira.",
  "src/de/home/index.njk": "Exklusive Hausbetreuung auf Madeira für Villen und hochwertige Wohnungen mit diskreten Kontrollen und klaren Updates.",
  "src/en/home/index.njk": "Luxury property care in Madeira for villas and premium apartments with discreet checks and clear updates.",
  "src/fr/home/index.njk": "Property care haut de gamme à Madère pour villas et appartements premium avec contrôles discrets.",
  "src/pt/home/index.njk": "Property care premium na Madeira para villas e apartamentos de luxo com verificações discretas.",
  "src/de/landing/alto/index.njk": "AL-Reinigung auf Madeira mit strukturierter Vorbereitung, Premium-Standard und verlässlicher Übergabe.",
  "src/en/landing/alto/index.njk": "Cleaning for selected Alojamento Local properties in Madeira with structured prep and reliable turnover support.",
  "src/fr/landing/alto/index.njk": "Nettoyage AL à Madère avec préparation structurée, standard premium et turnovers fiables.",
  "src/pt/landing/alto/index.njk": "Limpeza AL na Madeira com preparação estruturada, padrão premium e turnovers fiáveis.",
  "src/de/legal/index.njk": "Impressum von Anjo Property Care Madeira mit Anbieterangaben, Kontaktdaten und rechtlichen Informationen.",
  "src/en/legal/index.njk": "Legal notice for Anjo Property Care Madeira with company details, contact data and legal information.",
  "src/fr/legal/index.njk": "Mentions légales d’Anjo Property Care Madeira avec coordonnées et informations juridiques.",
  "src/pt/legal/index.njk": "Aviso legal da Anjo Property Care Madeira com dados da empresa, contactos e informação jurídica.",
  "src/de/privacy/index.njk": "Datenschutzerklärung zu Website, Kontaktanfragen und Datenverarbeitung bei Anjo Property Care Madeira.",
  "src/en/privacy/index.njk": "Privacy policy for website use, contact requests and data processing at Anjo Property Care Madeira.",
  "src/fr/privacy/index.njk": "Politique de confidentialité sur le site, les contacts et le traitement des données chez Anjo Property Care Madeira.",
  "src/pt/privacy/index.njk": "Política de privacidade sobre o site, pedidos de contacto e tratamento de dados na Anjo Property Care Madeira.",
  "src/de/services/index.njk": "Premium-Reinigung und ergänzende Services auf Madeira für private Residenzen mit hohem Anspruch.",
  "src/en/services/index.njk": "Premium cleaning and support services in Madeira for private residences with high standards.",
  "src/fr/services/index.njk": "Nettoyage premium et services complémentaires à Madère pour résidences privées exigeantes.",
  "src/pt/services/index.njk": "Limpeza premium e serviços complementares na Madeira para residências privadas exigentes.",
  "src/de/orte/index.njk": "Property Care in ausgewählten Lagen auf Madeira für Villen, Zweitwohnsitze und hochwertige Residenzen.",
  "src/en/locations/index.njk": "Luxury property care across Madeira for villas, second homes and high-end residences.",
  "src/fr/lieux/index.njk": "Property care haut de gamme à Madère pour villas, résidences secondaires et biens de standing.",
  "src/pt/locais/index.njk": "Property care premium na Madeira para villas, segundas residências e imóveis de alto padrão.",
  "src/de/orte/boaventura/index.njk": "Property Care in Boaventura auf Madeira für ruhige Hanglagen und nordseitige Residenzen.",
  "src/en/locations/boaventura/index.njk": "Luxury property care in Boaventura, Madeira for quiet hillside homes on the north coast.",
  "src/fr/lieux/boaventura/index.njk": "Property care haut de gamme à Boaventura, Madère pour résidences calmes sur les hauteurs du nord.",
  "src/pt/locais/boaventura/index.njk": "Property care premium em Boaventura, Madeira para moradias tranquilas em encostas no norte.",
  "src/de/orte/calheta/index.njk": "Property Care in Calheta auf Madeira für sonnige Villenlagen und hochwertige Zweitwohnsitze.",
  "src/en/locations/calheta/index.njk": "Luxury property care in Calheta, Madeira for sunny villas and high-end second homes.",
  "src/fr/lieux/calheta/index.njk": "Property care haut de gamme à Calheta, Madère pour villas ensoleillées et résidences secondaires haut de gamme.",
  "src/pt/locais/calheta/index.njk": "Property care premium em Calheta, Madeira para villas soalheiras e segundas residências de alto padrão.",
  "src/de/orte/camara-de-lobos/index.njk": "Property Care in Câmara de Lobos auf Madeira für Meeresnähe, Hanglagen und exklusive Residenzen.",
  "src/en/locations/camara-de-lobos/index.njk": "Luxury property care in Câmara de Lobos, Madeira for coastal hillsides and exclusive residences.",
  "src/fr/lieux/camara-de-lobos/index.njk": "Property care haut de gamme à Câmara de Lobos, Madère pour résidences exclusives proches de la mer.",
  "src/pt/locais/camara-de-lobos/index.njk": "Property care premium em Câmara de Lobos, Madeira para residências exclusivas junto ao mar.",
  "src/de/orte/campanario/index.njk": "Property Care in Campanário auf Madeira für gepflegte Residenzen zwischen Küste und Hanglage.",
  "src/en/locations/campanario/index.njk": "Luxury property care in Campanário, Madeira for well-kept homes between coast and hillside.",
  "src/fr/lieux/campanario/index.njk": "Property care haut de gamme à Campanário, Madère pour résidences soignées entre côte et hauteur.",
  "src/pt/locais/campanario/index.njk": "Property care premium em Campanário, Madeira para residências cuidadas entre costa e encosta.",
  "src/de/orte/canico/index.njk": "Property Care in Caniço auf Madeira für hochwertige Immobilien in Küstennähe.",
  "src/en/locations/canico/index.njk": "Luxury property care in Caniço, Madeira for premium properties near the coast.",
  "src/fr/lieux/canico/index.njk": "Property care haut de gamme à Caniço, Madère pour biens haut de gamme près du littoral.",
  "src/pt/locais/canico/index.njk": "Property care premium em Caniço, Madeira para imóveis premium perto do litoral.",
  "src/de/orte/curral-das-freiras/index.njk": "Property Care in Curral das Freiras auf Madeira für abgelegene Residenzen im geschützten Bergtal.",
  "src/en/locations/curral-das-freiras/index.njk": "Luxury property care in Curral das Freiras, Madeira for secluded homes in the mountain valley.",
  "src/fr/lieux/curral-das-freiras/index.njk": "Property care haut de gamme à Curral das Freiras, Madère pour résidences isolées dans la vallée montagneuse.",
  "src/pt/locais/curral-das-freiras/index.njk": "Property care premium em Curral das Freiras, Madeira para residências isoladas no vale de montanha.",
  "src/de/orte/funchal/index.njk": "Property Care in Funchal auf Madeira für Stadtresidenzen, Villen und Luxuswohnungen.",
  "src/en/locations/funchal/index.njk": "Luxury property care in Funchal, Madeira for city residences, villas and luxury apartments.",
  "src/fr/lieux/funchal/index.njk": "Property care haut de gamme à Funchal, Madère pour résidences urbaines, villas et appartements de luxe.",
  "src/pt/locais/funchal/index.njk": "Property care premium em Funchal, Madeira para residências urbanas, villas e apartamentos de luxo.",
  "src/de/orte/jardim-do-mar/index.njk": "Property Care in Jardim do Mar auf Madeira für exponierte Küstenresidenzen mit Atlantiklage.",
  "src/en/locations/jardim-do-mar/index.njk": "Luxury property care in Jardim do Mar, Madeira for exposed coastal homes by the Atlantic.",
  "src/fr/lieux/jardim-do-mar/index.njk": "Property care haut de gamme à Jardim do Mar, Madère pour résidences côtières exposées à l’Atlantique.",
  "src/pt/locais/jardim-do-mar/index.njk": "Property care premium em Jardim do Mar, Madeira para residências costeiras expostas ao Atlântico.",
  "src/de/orte/paul-do-mar/index.njk": "Property Care in Paul do Mar auf Madeira für Küstenlagen mit Salzluft und Wetterexposition.",
  "src/en/locations/paul-do-mar/index.njk": "Luxury property care in Paul do Mar, Madeira for coastal homes facing salt air and weather.",
  "src/fr/lieux/paul-do-mar/index.njk": "Property care haut de gamme à Paul do Mar, Madère pour résidences côtières exposées au sel et au vent.",
  "src/pt/locais/paul-do-mar/index.njk": "Property care premium em Paul do Mar, Madeira para residências costeiras expostas a sal e vento.",
  "src/de/orte/ponta-do-pargo/index.njk": "Property Care in Ponta do Pargo auf Madeira für wetterexponierte Residenzen im Westen.",
  "src/en/locations/ponta-do-pargo/index.njk": "Luxury property care in Ponta do Pargo, Madeira for weather-exposed residences in the west.",
  "src/fr/lieux/ponta-do-pargo/index.njk": "Property care haut de gamme à Ponta do Pargo, Madère pour résidences exposées aux intempéries à l’ouest.",
  "src/pt/locais/ponta-do-pargo/index.njk": "Property care premium em Ponta do Pargo, Madeira para residências expostas ao clima no oeste.",
  "src/de/orte/ponta-do-sol/index.njk": "Property Care in Ponta do Sol auf Madeira für sonnige Luxusimmobilien und Zweitwohnsitze.",
  "src/en/locations/ponta-do-sol/index.njk": "Luxury property care in Ponta do Sol, Madeira for sunny luxury homes and second residences.",
  "src/fr/lieux/ponta-do-sol/index.njk": "Property care haut de gamme à Ponta do Sol, Madère pour demeures ensoleillées et résidences secondaires.",
  "src/pt/locais/ponta-do-sol/index.njk": "Property care premium em Ponta do Sol, Madeira para casas de luxo soalheiras e segundas residências.",
  "src/de/orte/porto-moniz/index.njk": "Property Care in Porto Moniz auf Madeira für nordwestliche Residenzen mit Wetterexposition.",
  "src/en/locations/porto-moniz/index.njk": "Luxury property care in Porto Moniz, Madeira for northwest homes exposed to Atlantic weather.",
  "src/fr/lieux/porto-moniz/index.njk": "Property care haut de gamme à Porto Moniz, Madère pour résidences du nord-ouest exposées au climat.",
  "src/pt/locais/porto-moniz/index.njk": "Property care premium em Porto Moniz, Madeira para residências no noroeste expostas ao clima.",
  "src/de/orte/ribeira-brava/index.njk": "Property Care in Ribeira Brava auf Madeira für exklusive Immobilien zwischen Küste und Hang.",
  "src/en/locations/ribeira-brava/index.njk": "Luxury property care in Ribeira Brava, Madeira for exclusive homes between coast and hillside.",
  "src/fr/lieux/ribeira-brava/index.njk": "Property care haut de gamme à Ribeira Brava, Madère pour biens exclusifs entre côte et versant.",
  "src/pt/locais/ribeira-brava/index.njk": "Property care premium em Ribeira Brava, Madeira para imóveis exclusivos entre costa e encosta.",
  "src/de/orte/santa-cruz/index.njk": "Property Care in Santa Cruz auf Madeira für küstennahe Residenzen und gepflegte Zweitwohnsitze.",
  "src/en/locations/santa-cruz/index.njk": "Luxury property care in Santa Cruz, Madeira for coastal residences and refined second homes.",
  "src/fr/lieux/santa-cruz/index.njk": "Property care haut de gamme à Santa Cruz, Madère pour résidences proches de la côte et secondaires soignées.",
  "src/pt/locais/santa-cruz/index.njk": "Property care premium em Santa Cruz, Madeira para residências costeiras e segundas casas cuidadas.",
  "src/de/orte/santana/index.njk": "Property Care in Santana auf Madeira für Residenzen in grüner, höherer Lage.",
  "src/en/locations/santana/index.njk": "Luxury property care in Santana, Madeira for residences in greener, elevated areas.",
  "src/fr/lieux/santana/index.njk": "Property care haut de gamme à Santana, Madère pour résidences en altitude dans un cadre verdoyant.",
  "src/pt/locais/santana/index.njk": "Property care premium em Santana, Madeira para residências em zonas verdes e elevadas.",
  "src/de/orte/sao-jorge/index.njk": "Property Care in São Jorge auf Madeira für ruhige Residenzen im grünen Norden.",
  "src/en/locations/sao-jorge/index.njk": "Luxury property care in São Jorge, Madeira for peaceful homes in Madeira’s green north.",
  "src/fr/lieux/sao-jorge/index.njk": "Property care haut de gamme à São Jorge, Madère pour résidences paisibles dans le nord verdoyant.",
  "src/pt/locais/sao-jorge/index.njk": "Property care premium em São Jorge, Madeira para residências tranquilas no verde norte.",
  "src/de/orte/sao-vicente/index.njk": "Property Care in São Vicente auf Madeira für nordseitige Residenzen und Zweitwohnsitze.",
  "src/en/locations/sao-vicente/index.njk": "Luxury property care in São Vicente, Madeira for north-coast residences and second homes.",
  "src/fr/lieux/sao-vicente/index.njk": "Property care haut de gamme à São Vicente, Madère pour résidences du nord et seconds séjours.",
  "src/pt/locais/sao-vicente/index.njk": "Property care premium em São Vicente, Madeira para residências no norte e segundas casas."
}

EXCLUDED_ROOT_FILES = {
    "src/de/index.njk",
    "src/en/index.njk",
    "src/fr/index.njk",
    "src/pt/index.njk",
}

FRONTMATTER_RE = re.compile(r"^(---\r?\n)(.*?)(\r?\n---\r?\n)", re.DOTALL)

def get_frontmatter(raw: str, file_path: Path) -> tuple[str, str, str]:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        raise ValueError(f"Kein gültiger Frontmatter-Block in: {file_path}")
    return match.group(1), match.group(2), match.group(3)

def get_description(frontmatter: str, file_path: Path) -> str:
    for line in frontmatter.splitlines():
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            return value
    raise ValueError(f"Keine description-Zeile gefunden in: {file_path}")

def set_description(frontmatter: str, new_description: str, file_path: Path) -> str:
    lines = frontmatter.splitlines()
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith("description:"):
            lines[i] = f'description: "{new_description}"'
            replaced = True
            break
    if not replaced:
        raise ValueError(f"Keine description-Zeile gefunden in: {file_path}")
    return "\n".join(lines)

def replace_description(file_path: Path, new_description: str) -> tuple[bool, str]:
    raw = file_path.read_text(encoding="utf-8")
    opening, frontmatter, closing = get_frontmatter(raw, file_path)
    old_description = get_description(frontmatter, file_path)
    updated_frontmatter = set_description(frontmatter, new_description, file_path)
    updated_raw = opening + updated_frontmatter + closing + raw[len(opening) + len(frontmatter) + len(closing):]
    if updated_raw != raw:
        file_path.write_text(updated_raw, encoding="utf-8")
        return True, old_description
    return False, old_description

def main() -> int:
    project_root = Path.cwd()

    if not (project_root / "src").exists():
        alt_root = Path(__file__).resolve().parent.parent
        if (alt_root / "src").exists():
            project_root = alt_root
        else:
            print("Fehler: Projektwurzel mit src/-Ordner nicht gefunden.", file=sys.stderr)
            return 1

    missing_files: list[str] = []
    changed_files: list[str] = []
    unchanged_files: list[str] = []

    excluded_before = {}
    for rel_path in EXCLUDED_ROOT_FILES:
        file_path = project_root / rel_path
        if not file_path.exists():
            print(f"Fehler: Ausgeschlossene Datei fehlt: {rel_path}", file=sys.stderr)
            return 1
        raw = file_path.read_text(encoding="utf-8")
        _, frontmatter, _ = get_frontmatter(raw, file_path)
        excluded_before[rel_path] = get_description(frontmatter, file_path)

    for rel_path, new_description in DESCRIPTION_MAP.items():
        file_path = project_root / rel_path
        if not file_path.exists():
            missing_files.append(rel_path)
            continue

        if len(new_description) > 135:
            print(
                f"Fehler: Description länger als 135 Zeichen: {rel_path} ({len(new_description)})",
                file=sys.stderr,
            )
            return 1

        changed, _old_description = replace_description(file_path, new_description)
        if changed:
            changed_files.append(rel_path)
        else:
            unchanged_files.append(rel_path)

    if missing_files:
        print("Fehlende Dateien:", file=sys.stderr)
        for item in missing_files:
            print(f" - {item}", file=sys.stderr)
        return 1

    for rel_path, expected_description in DESCRIPTION_MAP.items():
        file_path = project_root / rel_path
        raw = file_path.read_text(encoding="utf-8")
        _, frontmatter, _ = get_frontmatter(raw, file_path)
        actual_description = get_description(frontmatter, file_path)
        if actual_description != expected_description:
            print(f"Fehler: Falsche Description nach Update in {rel_path}", file=sys.stderr)
            print(f"Erwartet: {expected_description}", file=sys.stderr)
            print(f"Ist:      {actual_description}", file=sys.stderr)
            return 1
        if len(actual_description) > 135:
            print(f"Fehler: Description nach Update zu lang in {rel_path}", file=sys.stderr)
            return 1

    for rel_path, original_description in excluded_before.items():
        file_path = project_root / rel_path
        raw = file_path.read_text(encoding="utf-8")
        _, frontmatter, _ = get_frontmatter(raw, file_path)
        current_description = get_description(frontmatter, file_path)
        if current_description != original_description:
            print(f"Fehler: Ausgeschlossene Root-Seite wurde verändert: {rel_path}", file=sys.stderr)
            return 1

    print(f"Erfolgreich aktualisiert und geprüft: {len(DESCRIPTION_MAP)} Dateien.")
    print(f"Geändert: {len(changed_files)}")
    print(f"Bereits identisch: {len(unchanged_files)}")
    print("Ausgeschlossen und unverändert geprüft: 4 Root-Seiten (/de/, /en/, /fr/, /pt/).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
