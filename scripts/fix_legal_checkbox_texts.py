from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

TEXTS = {
    "de": {
        "terms": "Ich akzeptiere die AGB",
        "withdrawal": "Ich habe die Widerrufsbelehrung gelesen",
        "early": "Ich verlange den vorzeitigen Beginn der Leistung und verstehe, dass ich mein Widerrufsrecht bei vollständiger Leistung verlieren kann",
    },
    "en": {
        "terms": "I accept the Terms and Conditions",
        "withdrawal": "I have read the withdrawal information",
        "early": "I request early execution and understand that I may lose my right of withdrawal once the service has been fully performed",
    },
    "fr": {
        "terms": "J’accepte les conditions générales",
        "withdrawal": "J’ai lu les informations sur la rétractation",
        "early": "Je demande l’exécution anticipée du service et je comprends que je peux perdre mon droit de rétractation une fois le service entièrement exécuté",
    },
    "pt": {
        "terms": "Aceito os Termos e Condições",
        "withdrawal": "Li a informação sobre livre resolução",
        "early": "Solicito o início antecipado do serviço e compreendo que posso perder o meu direito de livre resolução quando o serviço estiver totalmente executado",
    },
}

FILES = [
    SRC / "de" / "contact" / "index.njk",
    SRC / "en" / "contact" / "index.njk",
    SRC / "fr" / "contact" / "index.njk",
    SRC / "pt" / "contact" / "index.njk",
]


def replace_checkbox_label(content: str, field_name: str, new_text: str) -> str:
    pattern = re.compile(
        rf'(<input\s+type="checkbox"\s+name="{re.escape(field_name)}"[^>]*>\s*)(.*?)(\s*</label>)',
        re.DOTALL,
    )
    new_content, count = pattern.subn(rf'\1{new_text}\3', content, count=1)
    if count == 0:
        raise ValueError(f'Checkbox mit name="{field_name}" nicht gefunden.')
    return new_content


def main() -> None:
    for file_path in FILES:
        if not file_path.exists():
            print(f"Übersprungen (nicht gefunden): {file_path}")
            continue

        lang = file_path.parts[-3]
        texts = TEXTS[lang]

        content = file_path.read_text(encoding="utf-8")

        content = replace_checkbox_label(content, "accept_terms", texts["terms"])
        content = replace_checkbox_label(content, "accept_withdrawal", texts["withdrawal"])
        content = replace_checkbox_label(content, "accept_early", texts["early"])

        file_path.write_text(content, encoding="utf-8")
        print(f"Aktualisiert: {file_path.relative_to(ROOT)}")

    print("FERTIG: Checkbox-Texte in DE / EN / FR / PT sprachsauber korrigiert.")


if __name__ == "__main__":
    main()