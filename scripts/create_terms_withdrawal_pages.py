from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

COMPANY = {
    "name": "Anjo Cleaning Unipessoal Lda.",
    "represented_by": "Florian Engelmann",
    "address_lines": [
        "Campus da Penteada",
        "Startup Madeira - EV 278",
        "9020-105 São Roque, Funchal",
        "Ilha da Madeira, Portugal",
    ],
    "phone": "+351 926 669 223",
    "phone_href": "+351926669223",
    "email": "info@anjo-cleaning.com",
    "web": "anjo-cleaning.com",
    "register": "Conservatória do Registo Comercial do Funchal",
    "nipc": "519 242 416",
    "vat": "PT 519 242 416",
    "adr_name": "Centro de Arbitragem de Conflitos de Consumo da Região Autónoma da Madeira",
    "adr_address_1": "Rua Direita, n.º 27 - 1.º Andar - Esq.",
    "adr_address_2": "9050-450 Funchal",
    "adr_phone": "+351 291 147 115",
    "adr_phone_href": "+351291147115",
    "adr_email": "centroarbitragem.sritj@madeira.gov.pt",
    "adr_url": "https://www.madeira.gov.pt/cacc/",
    "complaints_url": "https://www.livroreclamacoes.pt",
}

LANG_MAP = {
    "de": {"terms_slug": "terms", "withdrawal_slug": "withdrawal"},
    "en": {"terms_slug": "terms", "withdrawal_slug": "withdrawal"},
    "fr": {"terms_slug": "terms", "withdrawal_slug": "withdrawal"},
    "pt": {"terms_slug": "terms", "withdrawal_slug": "withdrawal"},
}

def legal_block():
    addr = "<br>\n    ".join(COMPANY["address_lines"])
    return f"""
  <h2>Company details</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Represented by: <strong>{COMPANY["represented_by"]}</strong><br><br>
    Registered office:<br>
    {addr}
  </p>

  <h2>Contact</h2>
  <p>
    Phone: <a class="cta-link" href="tel:{COMPANY["phone_href"]}">{COMPANY["phone"]}</a><br>
    Email: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Web: <a class="cta-link" href="https://{COMPANY["web"]}" target="_blank" rel="noopener noreferrer">{COMPANY["web"]}</a>
  </p>

  <h2>Register / identification</h2>
  <p>
    Commercial register (Conservatória): {COMPANY["register"]}<br>
    NIPC: {COMPANY["nipc"]}<br>
    VAT (IVA): {COMPANY["vat"]}
  </p>
""".strip()


def build_terms_en():
    return f"""---
layout: base.njk
lang: en
title: "Terms and Conditions | Anjo Cleaning Madeira"
description: "Terms and conditions for Anjo Cleaning Unipessoal Lda. for international property care and cleaning services in Madeira, Portugal."
permalink: /en/terms/

langLinks:
  de: /de/terms/
  en: /en/terms/
  fr: /fr/terms/
  pt: /pt/terms/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Terms and Conditions</h1>
  <p class="lead"><strong>General terms for cleaning, property care and property check services performed in Madeira, Portugal.</strong></p>

  {legal_block()}

  <h2>1. Scope</h2>
  <p>
    These Terms and Conditions apply to all offers, contracts and services provided by <strong>{COMPANY["name"]}</strong>
    to consumers and business customers, unless a separate written agreement expressly overrides them.
  </p>

  <h2>2. Services</h2>
  <p>
    We provide, in particular, cleaning services, property care services, visual property checks, storm checks, attendance services,
    access coordination and related support services for residential, holiday and other properties.
  </p>

  <h2>3. Place of performance</h2>
  <p>
    All services are performed exclusively in Portugal, in particular on Madeira. The contractual place of performance is Madeira, Portugal.
  </p>

  <h2>4. Contract formation</h2>
  <p>
    A contract is formed when we confirm a booking in writing, by email, by message, or when we start performing the requested service
    on the customer's instruction. Offers are non-binding unless expressly stated otherwise.
  </p>

  <h2>5. Service standard and limitations</h2>
  <p>
    Unless expressly agreed otherwise in writing, we owe a service, not a guaranteed economic result.
    Cleaning and property care are carried out with reasonable professional care.
    Property checks, storm checks and status reports are visual, non-invasive checks only and do not constitute technical,
    structural, electrical, sanitary, legal, insurance or expert assessments.
  </p>

  <h2>6. Customer duties</h2>
  <p>
    The customer must provide correct and complete information, ensure access to the property at the agreed time,
    disclose relevant risks, alarms, animals, pre-existing damage, moisture, mould, infestations, sensitive surfaces
    and any other circumstances relevant to safe and proper performance.
  </p>

  <h2>7. Access and failed attendance</h2>
  <p>
    If access is not possible, if the customer or contact person is unreachable, or if the agreed service cannot be performed
    for reasons within the customer’s responsibility, we may charge waiting time, a wasted trip fee and any reserved service time.
  </p>

  <h2>8. Prices and payment</h2>
  <p>
    All prices are in euro. Unless stated otherwise, consumer prices include legally applicable VAT, while business prices may be shown
    excluding VAT where permitted. Invoices are due immediately unless another payment term is expressly agreed.
    We may request advance payment in full or in part before service.
  </p>

  <h2>9. Cancellations and rescheduling</h2>
  <p>
    Unless a specific offer states otherwise, the following applies:
    cancellations more than 72 hours before the agreed start time are free of charge;
    cancellations less than 72 hours but at least 24 hours before the agreed start time may be charged at 50%;
    cancellations less than 24 hours before the agreed start time, no-shows or failed access may be charged at 100%.
    The customer may prove that a lower loss or lower expense occurred.
  </p>

  <h2>10. Right of withdrawal for consumers</h2>
  <p>
    Consumers may have a statutory 14-day withdrawal right for distance or off-premises contracts.
    Details are set out on our separate <a class="cta-link" href="/en/withdrawal/">Withdrawal Information</a> page.
    If the customer expressly requests that performance begins before the withdrawal period expires,
    the customer must pay a proportionate amount for services already provided if a valid withdrawal is exercised later.
    The withdrawal right can expire once the service has been fully performed after the required express request and acknowledgement.
  </p>

  <h2>11. No voluntary refund after full performance</h2>
  <p>
    Because our contracts are service contracts, there is no general voluntary return or refund right once a service has been fully and properly performed,
    except where mandatory law requires otherwise or where non-performance or defective performance is proven.
  </p>

  <h2>12. Complaints and correction opportunity</h2>
  <p>
    Obvious complaints should be reported in text form as soon as possible, ideally within 48 hours after service performance,
    with a concrete description and, where available, photographs.
    We must be given a reasonable opportunity to inspect and, where appropriate, remedy the issue before third parties are instructed.
  </p>

  <h2>13. Liability</h2>
  <p>
    We are liable without limitation for intent, gross negligence, injury to life, body or health,
    and wherever mandatory law imposes unlimited liability.
    For slight negligence, we are liable only for breach of essential contractual obligations and only for foreseeable damage typical for the contract.
    To the extent permitted by law, liability for property and financial damage is limited to the value of the affected service order.
  </p>

  <h2>14. Exclusion of indirect losses</h2>
  <p>
    To the extent permitted by law, we are not liable for indirect losses, consequential losses, loss of profit, loss of rent,
    loss of bookings, loss of use, market losses or losses arising from hidden defects, pre-existing defects, material fatigue,
    corrosion, moisture, infestations, construction defects or inaccurate information supplied by the customer.
  </p>

  <h2>15. Keys, access devices and sensitive items</h2>
  <p>
    The customer must secure particularly valuable, irreplaceable or fragile items.
    Liability for loss of keys or access devices exists only in accordance with Clause 13 and, to the extent permitted by law,
    is limited to the direct and necessary cost of reasonable security measures.
  </p>

  <h2>16. International customers, including customers from the USA</h2>
  <p>
    Our services are performed exclusively in Portugal.
    To the extent legally permissible, Portuguese law applies.
    For business customers, the exclusive place of jurisdiction is Funchal, Madeira, Portugal.
    For consumers, mandatory statutory jurisdiction and consumer protection rules remain unaffected.
    To the extent legally permissible, implied warranties not expressly stated in writing are excluded.
    Services are provided on the basis of the agreed scope only.
  </p>

  <h2>17. Third-party claims / customer responsibility</h2>
  <p>
    The customer remains responsible for decisions on repairs, insurance notifications, emergency measures and specialist investigations,
    unless we have expressly accepted those tasks in writing.
    Business customers must indemnify us against third-party claims arising from incorrect instructions, information,
    access arrangements or materials provided by the customer, unless we are at fault.
  </p>

  <h2>18. Force majeure</h2>
  <p>
    We are not liable for delays or non-performance caused by circumstances beyond our reasonable control,
    including severe weather, storms, natural events, government restrictions, transport disruption, illness or safety risks.
  </p>

  <h2>19. Complaints book and ADR</h2>
  <p>
    Where legally required, we provide access to the Portuguese complaints system (<em>Livro de Reclamações</em>).
    Consumer ADR information for Madeira:
    <br><br>
    <strong>{COMPANY["adr_name"]}</strong><br>
    {COMPANY["adr_address_1"]}<br>
    {COMPANY["adr_address_2"]}<br>
    Phone: <a class="cta-link" href="tel:{COMPANY["adr_phone_href"]}">{COMPANY["adr_phone"]}</a><br>
    Email: <a class="cta-link" href="mailto:{COMPANY["adr_email"]}">{COMPANY["adr_email"]}</a><br>
    Website: <a class="cta-link" href="{COMPANY["adr_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["adr_url"]}</a><br>
    Livro de Reclamações: <a class="cta-link" href="{COMPANY["complaints_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["complaints_url"]}</a>
  </p>

  <h2>20. ODR platform</h2>
  <p>
    The former EU Online Dispute Resolution platform has been discontinued and is no longer available.
  </p>

  <h2>21. Language</h2>
  <p>
    English is the main contractual language for international customers.
    If these terms are also provided in another language, the English version prevails in case of conflict,
    to the extent permitted by mandatory law.
  </p>

  <h2>22. Severability</h2>
  <p>
    If any provision of these Terms and Conditions is or becomes invalid or unenforceable,
    the remaining provisions remain unaffected.
  </p>

  <p class="small" style="margin-top:18px;">
    Related page: <a class="cta-link" href="/en/withdrawal/">Withdrawal Information</a><br>
    Data protection information: <a class="cta-link" href="/en/privacy/">Privacy Policy</a><br>
    Legal provider information: <a class="cta-link" href="/en/legal/">Legal Notice</a>
  </p>
</section>
"""


def build_withdrawal_en():
    return f"""---
layout: base.njk
lang: en
title: "Withdrawal Information | Anjo Cleaning Madeira"
description: "Withdrawal information for consumers booking Anjo Cleaning services in Madeira, Portugal."
permalink: /en/withdrawal/

langLinks:
  de: /de/withdrawal/
  en: /en/withdrawal/
  fr: /fr/withdrawal/
  pt: /pt/withdrawal/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Withdrawal Information</h1>
  <p class="lead"><strong>Information for consumers regarding the statutory right of withdrawal for distance and off-premises service contracts.</strong></p>

  {legal_block()}

  <h2>1. Statutory right of withdrawal</h2>
  <p>
    If you are a consumer and conclude a contract with us at a distance (for example by email, website form, telephone or message)
    or outside business premises, you may have a statutory right to withdraw from the contract within 14 days without giving any reason.
  </p>

  <h2>2. Withdrawal period</h2>
  <p>
    The withdrawal period is 14 days from the date of conclusion of the contract.
  </p>

  <h2>3. How to exercise the withdrawal right</h2>
  <p>
    To exercise your withdrawal right, you must inform us by means of a clear statement of your decision to withdraw from the contract.
    You may send your statement by email or post using the contact details above.
    You may use the model withdrawal form below, but this is not mandatory.
  </p>

  <h2>4. Model wording</h2>
  <p>
    You may use the following wording:
  </p>
  <p>
    “I / We hereby withdraw from the contract concluded by me / us for the provision of the following service: [service description],
    ordered on [date], name of consumer(s), address of consumer(s), date.”
  </p>

  <h2>5. Timely dispatch is sufficient</h2>
  <p>
    To meet the withdrawal deadline, it is sufficient that you send your communication concerning your exercise of the withdrawal right
    before the withdrawal period has expired.
  </p>

  <h2>6. Consequences of withdrawal</h2>
  <p>
    If you validly withdraw from the contract, we will reimburse payments received from you without undue delay
    and at the latest within 14 days from the day on which we receive your withdrawal notice.
    We will use the same means of payment that you used for the original transaction, unless something else has been expressly agreed.
  </p>

  <h2>7. Early performance at your request</h2>
  <p>
    If you expressly request that we begin the service before the withdrawal period expires,
    and you later exercise a valid withdrawal, you must pay us an amount proportionate to what has already been provided
    until the time you informed us of the withdrawal, compared with the full contractual scope.
  </p>

  <h2>8. Loss of the withdrawal right after full performance</h2>
  <p>
    In service contracts, your withdrawal right may expire once the service has been fully performed,
    provided that performance began after your express request and after you acknowledged that you may lose your withdrawal right
    once the contract has been fully performed.
  </p>

  <h2>9. Important practical note for urgent and date-specific services</h2>
  <p>
    Many of our services are booked for specific dates or at short notice, for example cleaning before arrival,
    attendance, urgent property checks or storm checks.
    If you ask us to start before the 14-day withdrawal period has ended, the rules in Clauses 7 and 8 apply.
  </p>

  <h2>10. No general withdrawal right for business customers</h2>
  <p>
    This withdrawal information applies to consumers only.
    Business customers do not benefit from a statutory consumer withdrawal right unless mandatory law provides otherwise.
  </p>

  <h2>11. Contact for withdrawal notices</h2>
  <p>
    Email: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Postal address:<br>
    <strong>{COMPANY["name"]}</strong><br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <p class="small" style="margin-top:18px;">
    Related page: <a class="cta-link" href="/en/terms/">Terms and Conditions</a><br>
    Data protection information: <a class="cta-link" href="/en/privacy/">Privacy Policy</a><br>
    Legal provider information: <a class="cta-link" href="/en/legal/">Legal Notice</a>
  </p>
</section>
"""


def build_terms_de():
    return f"""---
layout: base.njk
lang: de
title: "AGB | Anjo Cleaning Madeira"
description: "Allgemeine Geschäftsbedingungen von Anjo Cleaning Unipessoal Lda. für internationale Reinigungs- und Property-Care-Dienstleistungen auf Madeira."
permalink: /de/terms/

langLinks:
  de: /de/terms/
  en: /en/terms/
  fr: /fr/terms/
  pt: /pt/terms/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Allgemeine Geschäftsbedingungen</h1>
  <p class="lead"><strong>Allgemeine Bedingungen für Reinigungs-, Property-Care- und Objektkontrollleistungen auf Madeira, Portugal.</strong></p>

  <h2>Anbieter</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Vertreten durch: <strong>{COMPANY["represented_by"]}</strong><br><br>
    Sitz:<br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <h2>Kontakt</h2>
  <p>
    Telefon: <a class="cta-link" href="tel:{COMPANY["phone_href"]}">{COMPANY["phone"]}</a><br>
    E-Mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Web: <a class="cta-link" href="https://{COMPANY["web"]}" target="_blank" rel="noopener noreferrer">{COMPANY["web"]}</a>
  </p>

  <h2>Register / Identifikation</h2>
  <p>
    Registo comercial (Conservatória): {COMPANY["register"]}<br>
    NIPC: {COMPANY["nipc"]}<br>
    USt-ID (IVA): {COMPANY["vat"]}
  </p>

  <h2>1. Geltungsbereich</h2>
  <p>
    Diese Allgemeinen Geschäftsbedingungen gelten für alle Angebote, Verträge und Leistungen von <strong>{COMPANY["name"]}</strong>
    gegenüber Verbrauchern und Unternehmern, soweit keine gesonderte schriftliche Vereinbarung ausdrücklich vorgeht.
  </p>

  <h2>2. Leistungen</h2>
  <p>
    Wir erbringen insbesondere Reinigungsleistungen, Property-Care-Leistungen, visuelle Objektkontrollen, Storm Checks,
    Anwesenheitsservices, Zugangskoordination und damit verbundene Unterstützungsleistungen für Wohnimmobilien,
    Ferienimmobilien und sonstige Objekte.
  </p>

  <h2>3. Leistungsort</h2>
  <p>
    Sämtliche Leistungen werden ausschließlich in Portugal, insbesondere auf Madeira, erbracht.
    Vertragsmäßiger Leistungsort ist Madeira, Portugal.
  </p>

  <h2>4. Vertragsschluss</h2>
  <p>
    Ein Vertrag kommt zustande, wenn wir eine Buchung schriftlich, per E-Mail oder Nachricht bestätigen
    oder wenn wir auf Weisung des Kunden mit der Ausführung der gewünschten Leistung beginnen.
    Angebote sind freibleibend, sofern sie nicht ausdrücklich als verbindlich bezeichnet sind.
  </p>

  <h2>5. Leistungsstandard und Leistungsgrenzen</h2>
  <p>
    Soweit nicht ausdrücklich schriftlich etwas anderes vereinbart ist, schulden wir eine Dienstleistung,
    keinen garantierten wirtschaftlichen Erfolg.
    Reinigungs- und Property-Care-Leistungen werden mit angemessener fachlicher Sorgfalt ausgeführt.
    Objektchecks, Storm Checks und Statusberichte sind ausschließlich visuelle, nicht-invasive Kontrollen
    und stellen keine technische, statische, elektrische, sanitäre, rechtliche, versicherungsrechtliche oder gutachterliche Prüfung dar.
  </p>

  <h2>6. Mitwirkungspflichten des Kunden</h2>
  <p>
    Der Kunde hat richtige und vollständige Informationen bereitzustellen, den Zugang zum Objekt zum vereinbarten Zeitpunkt sicherzustellen
    und relevante Risiken, Alarmanlagen, Tiere, Vorschäden, Feuchtigkeit, Schimmel, Schädlingsbefall, empfindliche Oberflächen
    sowie sonstige für eine sichere und ordnungsgemäße Leistungserbringung bedeutsame Umstände offenzulegen.
  </p>

  <h2>7. Zugang und erfolglose Anfahrt</h2>
  <p>
    Ist ein Zugang nicht möglich, ist der Kunde oder eine benannte Kontaktperson nicht erreichbar oder kann die vereinbarte Leistung
    aus Gründen aus dem Verantwortungsbereich des Kunden nicht erbracht werden, können Wartezeiten, Leerfahrten und reservierte Einsatzzeiten berechnet werden.
  </p>

  <h2>8. Preise und Zahlung</h2>
  <p>
    Alle Preise verstehen sich in Euro.
    Soweit nicht anders angegeben, enthalten Verbraucherpreise die gesetzlich anwendbare Umsatzsteuer,
    während Unternehmerpreise, soweit zulässig, auch netto ausgewiesen werden können.
    Rechnungen sind sofort fällig, sofern nicht ausdrücklich ein anderes Zahlungsziel vereinbart wurde.
    Wir können vollständige oder teilweise Vorauszahlung verlangen.
  </p>

  <h2>9. Stornierung und Umbuchung</h2>
  <p>
    Soweit im konkreten Angebot nichts Abweichendes geregelt ist, gilt:
    Stornierungen mehr als 72 Stunden vor dem vereinbarten Beginn sind kostenfrei;
    Stornierungen weniger als 72 Stunden, aber mindestens 24 Stunden vor dem vereinbarten Beginn können mit 50 % berechnet werden;
    Stornierungen weniger als 24 Stunden vor dem vereinbarten Beginn, Nichterscheinen oder fehlender Zugang können mit 100 % berechnet werden.
    Dem Kunden bleibt der Nachweis vorbehalten, dass ein geringerer Schaden oder Aufwand entstanden ist.
  </p>

  <h2>10. Widerrufsrecht für Verbraucher</h2>
  <p>
    Verbrauchern kann bei Fernabsatz- oder Außergeschäftsraumverträgen ein gesetzliches 14-tägiges Widerrufsrecht zustehen.
    Einzelheiten finden sich auf unserer separaten Seite
    <a class="cta-link" href="/de/withdrawal/">Widerrufsbelehrung</a>.
    Verlangt der Kunde ausdrücklich, dass wir vor Ablauf der Widerrufsfrist mit der Leistung beginnen,
    hat er bei einem später wirksamen Widerruf einen angemessenen Wertersatz für die bis dahin bereits erbrachten Leistungen zu zahlen.
    Das Widerrufsrecht kann bei vollständiger Erbringung der Dienstleistung unter den gesetzlichen Voraussetzungen vorzeitig erlöschen.
  </p>

  <h2>11. Kein freiwilliges Rückgaberecht nach vollständiger Leistung</h2>
  <p>
    Da es sich um Dienstleistungsverträge handelt, besteht nach vollständiger und ordnungsgemäßer Leistungserbringung
    grundsätzlich kein allgemeines freiwilliges Rückgabe- oder Erstattungsrecht,
    außer soweit zwingendes Recht etwas anderes verlangt oder eine Nicht- bzw. Schlechtleistung nachgewiesen wird.
  </p>

  <h2>12. Reklamationen und Nachbesserungsmöglichkeit</h2>
  <p>
    Offensichtliche Beanstandungen sind möglichst unverzüglich, idealerweise innerhalb von 48 Stunden nach Leistungserbringung,
    in Textform und möglichst mit konkreter Beschreibung sowie Fotos mitzuteilen.
    Vor Beauftragung Dritter ist uns eine angemessene Gelegenheit zur Prüfung und, soweit angemessen, zur Nachbesserung zu geben.
  </p>

  <h2>13. Haftung</h2>
  <p>
    Wir haften unbeschränkt bei Vorsatz, grober Fahrlässigkeit, Verletzung von Leben, Körper oder Gesundheit
    sowie in den Fällen zwingender gesetzlicher Haftung.
    Bei leichter Fahrlässigkeit haften wir nur bei Verletzung wesentlicher Vertragspflichten
    und nur für den vertragstypischen, vorhersehbaren Schaden.
    Soweit gesetzlich zulässig, ist unsere Haftung für Sach- und Vermögensschäden auf den Wert des betroffenen Einzelauftrags begrenzt.
  </p>

  <h2>14. Ausschluss mittelbarer Schäden</h2>
  <p>
    Soweit gesetzlich zulässig, haften wir nicht für mittelbare Schäden, Folgeschäden, entgangenen Gewinn,
    Mietausfall, Buchungsausfall, Nutzungsausfall, Marktschäden oder Schäden,
    die auf verborgenen Mängeln, bereits vorhandenen Defekten, Materialermüdung, Korrosion, Feuchtigkeit,
    Schädlingsbefall, Baumängeln oder unzutreffenden Angaben des Kunden beruhen.
  </p>

  <h2>15. Schlüssel, Zugangsmittel und empfindliche Gegenstände</h2>
  <p>
    Besonders wertvolle, unersetzliche oder zerbrechliche Gegenstände hat der Kunde selbst zu sichern.
    Eine Haftung für den Verlust von Schlüsseln oder Zugangsmitteln besteht nur nach Maßgabe von Ziffer 13
    und ist, soweit gesetzlich zulässig, auf die unmittelbaren und erforderlichen Kosten angemessener Sicherungsmaßnahmen begrenzt.
  </p>

  <h2>16. Internationale Kunden, einschließlich Kunden aus den USA</h2>
  <p>
    Unsere Leistungen werden ausschließlich in Portugal erbracht.
    Soweit gesetzlich zulässig, gilt portugiesisches Recht.
    Für Unternehmer ist ausschließlicher Gerichtsstand Funchal, Madeira, Portugal.
    Für Verbraucher bleiben zwingende gesetzliche Gerichtsstände und Verbraucherschutzvorschriften unberührt.
    Soweit gesetzlich zulässig, sind stillschweigende Garantien ausgeschlossen, soweit sie nicht ausdrücklich schriftlich übernommen wurden.
    Maßgeblich ist ausschließlich der vereinbarte Leistungsumfang.
  </p>

  <h2>17. Drittansprüche / Kundenverantwortung</h2>
  <p>
    Der Kunde bleibt für Entscheidungen über Reparaturen, Versicherungsanzeigen, Notmaßnahmen und Fachprüfungen verantwortlich,
    sofern wir diese Aufgaben nicht ausdrücklich schriftlich übernommen haben.
    Unternehmer haben uns von Ansprüchen Dritter freizustellen, die auf fehlerhaften Weisungen, Informationen,
    Zugangsregelungen oder vom Kunden bereitgestellten Materialien beruhen, soweit wir die Ursache nicht zu vertreten haben.
  </p>

  <h2>18. Höhere Gewalt</h2>
  <p>
    Für Verzögerungen oder Nichterfüllung aufgrund von Umständen außerhalb unseres angemessenen Einflussbereichs,
    insbesondere bei Unwetter, Sturm, Naturereignissen, behördlichen Maßnahmen, Verkehrsunterbrechungen,
    Krankheit oder Sicherheitsrisiken, haften wir nicht.
  </p>

  <h2>19. Livro de Reclamações und ADR</h2>
  <p>
    Soweit gesetzlich vorgeschrieben, stellen wir Zugang zum portugiesischen Beschwerdesystem (<em>Livro de Reclamações</em>) bereit.
    Verbraucherinformationen zur alternativen Streitbeilegung auf Madeira:
    <br><br>
    <strong>{COMPANY["adr_name"]}</strong><br>
    {COMPANY["adr_address_1"]}<br>
    {COMPANY["adr_address_2"]}<br>
    Telefon: <a class="cta-link" href="tel:{COMPANY["adr_phone_href"]}">{COMPANY["adr_phone"]}</a><br>
    E-Mail: <a class="cta-link" href="mailto:{COMPANY["adr_email"]}">{COMPANY["adr_email"]}</a><br>
    Website: <a class="cta-link" href="{COMPANY["adr_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["adr_url"]}</a><br>
    Livro de Reclamações: <a class="cta-link" href="{COMPANY["complaints_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["complaints_url"]}</a>
  </p>

  <h2>20. ODR-Plattform</h2>
  <p>
    Die frühere EU-Online-Streitbeilegungsplattform wurde eingestellt und steht nicht mehr zur Verfügung.
  </p>

  <h2>21. Sprache</h2>
  <p>
    Für internationale Kunden ist Englisch die maßgebliche Vertragssprache.
    Werden diese Bedingungen zusätzlich in einer anderen Sprache bereitgestellt,
    geht im Kollisionsfall die englische Fassung vor, soweit zwingendes Recht dem nicht entgegensteht.
  </p>

  <h2>22. Salvatorische Klausel</h2>
  <p>
    Sollten einzelne Bestimmungen dieser AGB ganz oder teilweise unwirksam oder undurchsetzbar sein oder werden,
    bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.
  </p>

  <p class="small" style="margin-top:18px;">
    Zugehörige Seite: <a class="cta-link" href="/de/withdrawal/">Widerrufsbelehrung</a><br>
    Datenschutzinformationen: <a class="cta-link" href="/de/privacy/">Datenschutz</a><br>
    Anbieterkennzeichnung: <a class="cta-link" href="/de/legal/">Impressum / Rechtliches</a>
  </p>
</section>
"""


def build_withdrawal_de():
    return f"""---
layout: base.njk
lang: de
title: "Widerrufsbelehrung | Anjo Cleaning Madeira"
description: "Widerrufsbelehrung für Verbraucher bei der Buchung von Dienstleistungen von Anjo Cleaning auf Madeira, Portugal."
permalink: /de/withdrawal/

langLinks:
  de: /de/withdrawal/
  en: /en/withdrawal/
  fr: /fr/withdrawal/
  pt: /pt/withdrawal/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Widerrufsbelehrung</h1>
  <p class="lead"><strong>Informationen für Verbraucher zum gesetzlichen Widerrufsrecht bei Fernabsatz- und Außergeschäftsraumverträgen über Dienstleistungen.</strong></p>

  <h2>Anbieter</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Vertreten durch: <strong>{COMPANY["represented_by"]}</strong><br><br>
    {'<br>'.join(COMPANY["address_lines"])}<br>
    E-Mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a>
  </p>

  <h2>1. Gesetzliches Widerrufsrecht</h2>
  <p>
    Wenn Sie Verbraucher sind und den Vertrag mit uns im Fernabsatz
    (zum Beispiel per E-Mail, Website-Formular, Telefon oder Nachricht)
    oder außerhalb von Geschäftsräumen schließen, kann Ihnen ein gesetzliches Widerrufsrecht von 14 Tagen ohne Angabe von Gründen zustehen.
  </p>

  <h2>2. Widerrufsfrist</h2>
  <p>
    Die Widerrufsfrist beträgt 14 Tage ab dem Tag des Vertragsschlusses.
  </p>

  <h2>3. Ausübung des Widerrufsrechts</h2>
  <p>
    Um Ihr Widerrufsrecht auszuüben, müssen Sie uns mittels einer eindeutigen Erklärung
    über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren.
    Dies kann per E-Mail oder Post unter Verwendung der oben genannten Kontaktdaten erfolgen.
    Sie können dafür das unten stehende Muster verwenden, sind dazu aber nicht verpflichtet.
  </p>

  <h2>4. Musterformulierung</h2>
  <p>
    Sie können folgende Formulierung verwenden:
  </p>
  <p>
    „Hiermit widerrufe ich / widerrufen wir den von mir / uns abgeschlossenen Vertrag
    über die Erbringung der folgenden Dienstleistung: [Leistungsbeschreibung],
    bestellt am [Datum], Name des / der Verbraucher(s), Anschrift des / der Verbraucher(s), Datum.“
  </p>

  <h2>5. Rechtzeitige Absendung genügt</h2>
  <p>
    Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts
    vor Ablauf der Widerrufsfrist absenden.
  </p>

  <h2>6. Folgen des Widerrufs</h2>
  <p>
    Wenn Sie den Vertrag wirksam widerrufen, erstatten wir Ihnen erhaltene Zahlungen unverzüglich
    und spätestens binnen 14 Tagen ab dem Tag, an dem uns Ihre Widerrufserklärung zugegangen ist.
    Für die Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Zahlung eingesetzt haben,
    sofern nicht ausdrücklich etwas anderes vereinbart wurde.
  </p>

  <h2>7. Vorzeitiger Leistungsbeginn auf Ihren Wunsch</h2>
  <p>
    Wenn Sie ausdrücklich verlangen, dass wir vor Ablauf der Widerrufsfrist mit der Leistung beginnen,
    und Sie später wirksam widerrufen, müssen Sie einen angemessenen Betrag zahlen,
    der dem Anteil der bis zum Zeitpunkt des Widerrufs bereits erbrachten Leistungen
    im Verhältnis zum vertraglich vereinbarten Gesamtumfang entspricht.
  </p>

  <h2>8. Erlöschen des Widerrufsrechts bei vollständiger Leistung</h2>
  <p>
    Bei Dienstleistungsverträgen kann Ihr Widerrufsrecht erlöschen,
    sobald die Leistung vollständig erbracht wurde,
    wenn die Ausführung erst begonnen hat, nachdem Sie dies ausdrücklich verlangt haben
    und zugleich bestätigt haben, dass Sie mit vollständiger Vertragserfüllung Ihr Widerrufsrecht verlieren können.
  </p>

  <h2>9. Wichtiger Praxishinweis für kurzfristige und terminierte Leistungen</h2>
  <p>
    Viele unserer Leistungen werden kurzfristig oder zu einem konkreten Termin gebucht,
    zum Beispiel Reinigungen vor Anreise, Anwesenheitsservices, dringende Objektkontrollen oder Storm Checks.
    Wenn Sie wünschen, dass wir bereits vor Ablauf der 14-tägigen Widerrufsfrist tätig werden,
    gelten die Regelungen der Ziffern 7 und 8.
  </p>

  <h2>10. Kein allgemeines Widerrufsrecht für Unternehmer</h2>
  <p>
    Diese Widerrufsbelehrung gilt nur für Verbraucher.
    Unternehmern steht kein gesetzliches Verbraucher-Widerrufsrecht zu,
    soweit zwingendes Recht nichts anderes vorsieht.
  </p>

  <h2>11. Kontakt für Widerrufserklärungen</h2>
  <p>
    E-Mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Postanschrift:<br>
    <strong>{COMPANY["name"]}</strong><br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <p class="small" style="margin-top:18px;">
    Zugehörige Seite: <a class="cta-link" href="/de/terms/">AGB</a><br>
    Datenschutzinformationen: <a class="cta-link" href="/de/privacy/">Datenschutz</a><br>
    Anbieterkennzeichnung: <a class="cta-link" href="/de/legal/">Impressum / Rechtliches</a>
  </p>
</section>
"""


def build_terms_fr():
    return f"""---
layout: base.njk
lang: fr
title: "Conditions générales | Anjo Cleaning Madeira"
description: "Conditions générales d’Anjo Cleaning Unipessoal Lda. pour les services internationaux de nettoyage et de property care à Madère."
permalink: /fr/terms/

langLinks:
  de: /de/terms/
  en: /en/terms/
  fr: /fr/terms/
  pt: /pt/terms/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Conditions générales</h1>
  <p class="lead"><strong>Conditions générales applicables aux services de nettoyage, de property care et de contrôle visuel de biens à Madère, Portugal.</strong></p>

  <h2>Prestataire</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Représentée par : <strong>{COMPANY["represented_by"]}</strong><br><br>
    Siège :<br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <h2>Contact</h2>
  <p>
    Téléphone : <a class="cta-link" href="tel:{COMPANY["phone_href"]}">{COMPANY["phone"]}</a><br>
    E-mail : <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Site web : <a class="cta-link" href="https://{COMPANY["web"]}" target="_blank" rel="noopener noreferrer">{COMPANY["web"]}</a>
  </p>

  <h2>Registre / identification</h2>
  <p>
    Registo comercial (Conservatória) : {COMPANY["register"]}<br>
    NIPC : {COMPANY["nipc"]}<br>
    TVA (IVA) : {COMPANY["vat"]}
  </p>

  <h2>1. Champ d’application</h2>
  <p>
    Les présentes conditions générales s’appliquent à toutes les offres, à tous les contrats et à toutes les prestations de
    <strong>{COMPANY["name"]}</strong> envers les consommateurs et les professionnels,
    sauf si un accord écrit distinct y déroge expressément.
  </p>

  <h2>2. Prestations</h2>
  <p>
    Nous fournissons notamment des services de nettoyage, de property care, de contrôle visuel de biens,
    de storm check, de présence sur site, de coordination d’accès et des services d’assistance liés
    aux biens résidentiels, aux locations de vacances et à d’autres biens.
  </p>

  <h2>3. Lieu d’exécution</h2>
  <p>
    Toutes les prestations sont exécutées exclusivement au Portugal, notamment à Madère.
    Le lieu contractuel d’exécution est Madère, Portugal.
  </p>

  <h2>4. Conclusion du contrat</h2>
  <p>
    Un contrat est conclu lorsque nous confirmons une réservation par écrit, par e-mail ou par message,
    ou lorsque nous commençons à exécuter la prestation demandée sur instruction du client.
    Les offres sont sans engagement sauf mention expresse contraire.
  </p>

  <h2>5. Niveau de prestation et limites</h2>
  <p>
    Sauf accord écrit contraire, nous sommes tenus à une prestation de service et non à un résultat économique garanti.
    Les services de nettoyage et de property care sont exécutés avec un niveau raisonnable de diligence professionnelle.
    Les contrôles de biens, storm checks et rapports d’état sont des contrôles uniquement visuels et non invasifs ;
    ils ne constituent pas une expertise technique, structurelle, électrique, sanitaire, juridique, d’assurance ou autre expertise spécialisée.
  </p>

  <h2>6. Obligations du client</h2>
  <p>
    Le client doit fournir des informations exactes et complètes, garantir l’accès au bien au moment convenu,
    et signaler les risques pertinents, alarmes, animaux, dommages préexistants, humidité, moisissures, infestations,
    surfaces sensibles et toute autre circonstance utile à une exécution sûre et correcte.
  </p>

  <h2>7. Accès et déplacement inutile</h2>
  <p>
    Si l’accès est impossible, si le client ou la personne de contact n’est pas joignable,
    ou si la prestation convenue ne peut pas être exécutée pour des raisons relevant de la responsabilité du client,
    nous pouvons facturer le temps d’attente, le déplacement inutile et le créneau réservé.
  </p>

  <h2>8. Prix et paiement</h2>
  <p>
    Tous les prix sont indiqués en euro.
    Sauf indication contraire, les prix consommateurs incluent la TVA légalement applicable,
    tandis que les prix professionnels peuvent, lorsque cela est autorisé, être présentés hors TVA.
    Les factures sont exigibles immédiatement sauf accord exprès sur un autre délai.
    Nous pouvons exiger un paiement anticipé total ou partiel avant l’exécution.
  </p>

  <h2>9. Annulation et changement de date</h2>
  <p>
    Sauf disposition contraire figurant dans une offre particulière, les règles suivantes s’appliquent :
    annulation plus de 72 heures avant le début convenu : sans frais ;
    annulation moins de 72 heures mais au moins 24 heures avant le début convenu : jusqu’à 50 % ;
    annulation moins de 24 heures avant le début convenu, absence ou accès impossible : jusqu’à 100 %.
    Le client peut prouver qu’un préjudice ou des frais moindres ont été subis.
  </p>

  <h2>10. Droit de rétractation pour les consommateurs</h2>
  <p>
    Les consommateurs peuvent bénéficier d’un droit légal de rétractation de 14 jours pour les contrats à distance
    ou hors établissement. Les détails figurent sur notre page séparée
    <a class="cta-link" href="/fr/withdrawal/">Informations sur la rétractation</a>.
    Si le client demande expressément que nous commencions la prestation avant l’expiration du délai de rétractation,
    il devra payer un montant proportionnel aux prestations déjà exécutées en cas de rétractation valable ultérieure.
    Le droit de rétractation peut s’éteindre de manière anticipée lorsque la prestation a été entièrement exécutée
    dans les conditions prévues par la loi.
  </p>

  <h2>11. Pas de droit de retour volontaire après exécution complète</h2>
  <p>
    S’agissant de contrats de services, il n’existe pas de droit général volontaire de retour ou de remboursement
    après exécution complète et correcte de la prestation,
    sauf disposition impérative contraire ou preuve d’une inexécution ou d’une mauvaise exécution.
  </p>

  <h2>12. Réclamations et possibilité de remédiation</h2>
  <p>
    Les réclamations apparentes doivent être signalées dès que possible, idéalement dans les 48 heures suivant la prestation,
    sous forme écrite, avec une description concrète et, si possible, des photos.
    Avant de mandater un tiers, le client doit nous laisser une possibilité raisonnable d’examiner la situation
    et, le cas échéant, d’y remédier.
  </p>

  <h2>13. Responsabilité</h2>
  <p>
    Notre responsabilité est illimitée en cas de dol, de faute lourde, d’atteinte à la vie, au corps ou à la santé,
    ainsi que dans les cas où la loi impose une responsabilité illimitée.
    En cas de négligence légère, nous ne répondons qu’en cas de violation d’une obligation essentielle
    et uniquement pour les dommages prévisibles typiques du contrat.
    Dans la mesure permise par la loi, notre responsabilité pour les dommages matériels et financiers
    est limitée à la valeur de la commande concernée.
  </p>

  <h2>14. Exclusion des dommages indirects</h2>
  <p>
    Dans la mesure permise par la loi, nous ne répondons pas des dommages indirects, consécutifs,
    pertes de bénéfices, pertes de loyers, pertes de réservations, pertes d’usage, pertes de marché
    ou des dommages résultant de vices cachés, de défauts préexistants, de fatigue des matériaux,
    de corrosion, d’humidité, d’infestations, de défauts de construction ou d’informations inexactes fournies par le client.
  </p>

  <h2>15. Clés, moyens d’accès et objets sensibles</h2>
  <p>
    Il appartient au client de sécuriser les objets particulièrement précieux, irremplaçables ou fragiles.
    Toute responsabilité en cas de perte de clés ou de moyens d’accès n’existe que conformément à l’article 13
    et, dans la mesure permise par la loi, est limitée aux coûts directs et nécessaires de mesures de sécurité raisonnables.
  </p>

  <h2>16. Clients internationaux, y compris les clients des États-Unis</h2>
  <p>
    Nos prestations sont exécutées exclusivement au Portugal.
    Dans la mesure légalement permise, le droit portugais s’applique.
    Pour les professionnels, le tribunal exclusivement compétent est celui de Funchal, Madère, Portugal.
    Pour les consommateurs, les règles impératives de compétence et de protection du consommateur restent inchangées.
    Dans la mesure légalement permise, toute garantie implicite non expressément accordée par écrit est exclue.
    Seul le périmètre de prestation convenu est déterminant.
  </p>

  <h2>17. Réclamations de tiers / responsabilité du client</h2>
  <p>
    Le client reste responsable des décisions relatives aux réparations, déclarations d’assurance,
    mesures d’urgence et expertises spécialisées, sauf si nous avons expressément accepté ces missions par écrit.
    Les clients professionnels doivent nous garantir contre les réclamations de tiers résultant
    d’instructions, d’informations, d’organisations d’accès ou de matériels fournis par le client,
    sauf faute de notre part.
  </p>

  <h2>18. Force majeure</h2>
  <p>
    Nous ne sommes pas responsables des retards ou inexécutions causés par des circonstances échappant à notre contrôle raisonnable,
    notamment intempéries sévères, tempêtes, événements naturels, restrictions administratives,
    perturbations de transport, maladie ou risques de sécurité.
  </p>

  <h2>19. Livro de Reclamações et ADR</h2>
  <p>
    Lorsque la loi l’exige, nous mettons à disposition l’accès au système portugais de réclamations (<em>Livro de Reclamações</em>).
    Informations ADR pour Madère :
    <br><br>
    <strong>{COMPANY["adr_name"]}</strong><br>
    {COMPANY["adr_address_1"]}<br>
    {COMPANY["adr_address_2"]}<br>
    Téléphone : <a class="cta-link" href="tel:{COMPANY["adr_phone_href"]}">{COMPANY["adr_phone"]}</a><br>
    E-mail : <a class="cta-link" href="mailto:{COMPANY["adr_email"]}">{COMPANY["adr_email"]}</a><br>
    Site : <a class="cta-link" href="{COMPANY["adr_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["adr_url"]}</a><br>
    Livro de Reclamações : <a class="cta-link" href="{COMPANY["complaints_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["complaints_url"]}</a>
  </p>

  <h2>20. Plateforme ODR</h2>
  <p>
    L’ancienne plateforme européenne de règlement en ligne des litiges a été supprimée et n’est plus disponible.
  </p>

  <h2>21. Langue</h2>
  <p>
    Pour les clients internationaux, l’anglais constitue la langue contractuelle principale.
    Si ces conditions sont également fournies dans une autre langue,
    la version anglaise prévaut en cas de contradiction, dans la mesure permise par le droit impératif.
  </p>

  <h2>22. Clause de sauvegarde</h2>
  <p>
    Si une disposition des présentes conditions générales est ou devient nulle ou inapplicable en tout ou en partie,
    la validité des autres dispositions n’en est pas affectée.
  </p>

  <p class="small" style="margin-top:18px;">
    Page associée : <a class="cta-link" href="/fr/withdrawal/">Informations sur la rétractation</a><br>
    Protection des données : <a class="cta-link" href="/fr/privacy/">Politique de confidentialité</a><br>
    Mentions légales : <a class="cta-link" href="/fr/legal/">Mentions légales</a>
  </p>
</section>
"""


def build_withdrawal_fr():
    return f"""---
layout: base.njk
lang: fr
title: "Informations sur la rétractation | Anjo Cleaning Madeira"
description: "Informations sur le droit de rétractation pour les consommateurs réservant des services Anjo Cleaning à Madère, Portugal."
permalink: /fr/withdrawal/

langLinks:
  de: /de/withdrawal/
  en: /en/withdrawal/
  fr: /fr/withdrawal/
  pt: /pt/withdrawal/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Informations sur la rétractation</h1>
  <p class="lead"><strong>Informations destinées aux consommateurs concernant le droit légal de rétractation applicable aux contrats de services à distance et hors établissement.</strong></p>

  <h2>Prestataire</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Représentée par : <strong>{COMPANY["represented_by"]}</strong><br><br>
    {'<br>'.join(COMPANY["address_lines"])}<br>
    E-mail : <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a>
  </p>

  <h2>1. Droit légal de rétractation</h2>
  <p>
    Si vous êtes un consommateur et que vous concluez un contrat avec nous à distance
    (par exemple par e-mail, formulaire du site, téléphone ou message)
    ou hors établissement, vous pouvez bénéficier d’un droit légal de rétractation de 14 jours sans indication de motif.
  </p>

  <h2>2. Délai de rétractation</h2>
  <p>
    Le délai de rétractation est de 14 jours à compter de la conclusion du contrat.
  </p>

  <h2>3. Exercice du droit de rétractation</h2>
  <p>
    Pour exercer votre droit de rétractation, vous devez nous notifier clairement votre décision de vous rétracter du contrat.
    Cette notification peut être envoyée par e-mail ou par courrier aux coordonnées ci-dessus.
    Vous pouvez utiliser la formulation modèle ci-dessous, sans que cela soit obligatoire.
  </p>

  <h2>4. Formulation modèle</h2>
  <p>
    Vous pouvez utiliser la formulation suivante :
  </p>
  <p>
    « Je / Nous me / nous rétracte / rétractons du contrat conclu pour la prestation suivante : [description du service],
    commandée le [date], nom du / des consommateur(s), adresse du / des consommateur(s), date. »
  </p>

  <h2>5. L’envoi dans le délai suffit</h2>
  <p>
    Pour respecter le délai de rétractation, il suffit d’envoyer votre communication relative à l’exercice du droit de rétractation
    avant l’expiration du délai.
  </p>

  <h2>6. Effets de la rétractation</h2>
  <p>
    Si vous vous rétractez valablement du contrat, nous vous rembourserons les paiements reçus sans retard injustifié
    et au plus tard dans les 14 jours à compter du jour où nous recevons votre notification de rétractation.
    Le remboursement sera effectué par le même moyen de paiement que celui utilisé lors de la transaction initiale,
    sauf accord exprès contraire.
  </p>

  <h2>7. Début anticipé de l’exécution à votre demande</h2>
  <p>
    Si vous demandez expressément que nous commencions la prestation avant l’expiration du délai de rétractation,
    et que vous exercez ensuite valablement ce droit, vous devez nous payer un montant proportionnel
    à ce qui a déjà été fourni jusqu’au moment où vous nous avez informés de la rétractation,
    par rapport à l’ensemble de la prestation prévue au contrat.
  </p>

  <h2>8. Perte du droit de rétractation après exécution complète</h2>
  <p>
    Pour les contrats de services, votre droit de rétractation peut prendre fin lorsque la prestation a été entièrement exécutée,
    à condition que l’exécution ait commencé après votre demande expresse
    et après que vous avez reconnu que vous pouviez perdre votre droit de rétractation
    une fois le contrat entièrement exécuté.
  </p>

  <h2>9. Note pratique importante pour les services urgents et datés</h2>
  <p>
    Nombre de nos services sont réservés pour des dates précises ou à court terme,
    par exemple des nettoyages avant arrivée, des services de présence, des contrôles urgents de biens ou des storm checks.
    Si vous nous demandez d’intervenir avant la fin du délai de 14 jours,
    les règles des articles 7 et 8 s’appliquent.
  </p>

  <h2>10. Pas de droit général de rétractation pour les professionnels</h2>
  <p>
    Les présentes informations ne concernent que les consommateurs.
    Les professionnels ne bénéficient pas d’un droit légal de rétractation du consommateur,
    sauf disposition impérative contraire.
  </p>

  <h2>11. Contact pour les notifications de rétractation</h2>
  <p>
    E-mail : <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Adresse postale :<br>
    <strong>{COMPANY["name"]}</strong><br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <p class="small" style="margin-top:18px;">
    Page associée : <a class="cta-link" href="/fr/terms/">Conditions générales</a><br>
    Protection des données : <a class="cta-link" href="/fr/privacy/">Politique de confidentialité</a><br>
    Mentions légales : <a class="cta-link" href="/fr/legal/">Mentions légales</a>
  </p>
</section>
"""


def build_terms_pt():
    return f"""---
layout: base.njk
lang: pt
title: "Termos e Condições | Anjo Cleaning Madeira"
description: "Termos e condições da Anjo Cleaning Unipessoal Lda. para serviços internacionais de limpeza e property care na Madeira."
permalink: /pt/terms/

langLinks:
  de: /de/terms/
  en: /en/terms/
  fr: /fr/terms/
  pt: /pt/terms/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Termos e Condições</h1>
  <p class="lead"><strong>Condições gerais aplicáveis a serviços de limpeza, property care e verificações visuais de imóveis na Madeira, Portugal.</strong></p>

  <h2>Prestador</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Representada por: <strong>{COMPANY["represented_by"]}</strong><br><br>
    Sede:<br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <h2>Contacto</h2>
  <p>
    Telefone: <a class="cta-link" href="tel:{COMPANY["phone_href"]}">{COMPANY["phone"]}</a><br>
    E-mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Web: <a class="cta-link" href="https://{COMPANY["web"]}" target="_blank" rel="noopener noreferrer">{COMPANY["web"]}</a>
  </p>

  <h2>Registo / identificação</h2>
  <p>
    Registo comercial (Conservatória): {COMPANY["register"]}<br>
    NIPC: {COMPANY["nipc"]}<br>
    IVA: {COMPANY["vat"]}
  </p>

  <h2>1. Âmbito</h2>
  <p>
    Os presentes Termos e Condições aplicam-se a todas as ofertas, contratos e serviços prestados por
    <strong>{COMPANY["name"]}</strong> a consumidores e clientes empresariais,
    salvo se um acordo escrito separado prevalecer expressamente.
  </p>

  <h2>2. Serviços</h2>
  <p>
    Prestamos, nomeadamente, serviços de limpeza, property care, verificações visuais de imóveis,
    storm checks, presença no local, coordenação de acessos e serviços de apoio relacionados
    com imóveis residenciais, alojamentos de férias e outros imóveis.
  </p>

  <h2>3. Local de prestação</h2>
  <p>
    Todos os serviços são prestados exclusivamente em Portugal, em especial na Madeira.
    O local contratual de prestação é a Madeira, Portugal.
  </p>

  <h2>4. Formação do contrato</h2>
  <p>
    O contrato é celebrado quando confirmamos a reserva por escrito, por e-mail ou por mensagem,
    ou quando iniciamos a execução do serviço solicitado por instrução do cliente.
    As propostas não são vinculativas salvo indicação expressa em contrário.
  </p>

  <h2>5. Padrão do serviço e limites</h2>
  <p>
    Salvo acordo escrito em contrário, prestamos um serviço e não garantimos um resultado económico específico.
    Os serviços de limpeza e property care são executados com diligência profissional razoável.
    Verificações de imóveis, storm checks e relatórios de estado são apenas verificações visuais, não invasivas,
    e não constituem avaliação técnica, estrutural, elétrica, sanitária, jurídica, pericial ou de seguros.
  </p>

  <h2>6. Deveres do cliente</h2>
  <p>
    O cliente deve fornecer informações corretas e completas, assegurar o acesso ao imóvel na data e hora acordadas
    e informar sobre riscos relevantes, alarmes, animais, danos pré-existentes, humidade, bolor, infestações,
    superfícies sensíveis e quaisquer outras circunstâncias importantes para uma execução segura e adequada.
  </p>

  <h2>7. Acesso e deslocação inútil</h2>
  <p>
    Se o acesso não for possível, se o cliente ou a pessoa de contacto não estiver contactável,
    ou se o serviço não puder ser executado por razões imputáveis ao cliente,
    poderemos cobrar tempo de espera, deslocação inútil e o tempo reservado para o serviço.
  </p>

  <h2>8. Preços e pagamento</h2>
  <p>
    Todos os preços são indicados em euros.
    Salvo indicação em contrário, os preços para consumidores incluem o IVA legalmente aplicável,
    enquanto os preços para empresas podem, quando permitido, ser apresentados sem IVA.
    As faturas vencem-se imediatamente, salvo acordo expresso em contrário.
    Podemos exigir pagamento antecipado total ou parcial antes da prestação do serviço.
  </p>

  <h2>9. Cancelamentos e reagendamentos</h2>
  <p>
    Salvo disposição diferente numa proposta específica, aplica-se o seguinte:
    cancelamentos com mais de 72 horas antes do início acordado são gratuitos;
    cancelamentos com menos de 72 horas mas pelo menos 24 horas antes do início acordado podem ser cobrados a 50%;
    cancelamentos com menos de 24 horas antes do início acordado, ausência ou impossibilidade de acesso podem ser cobrados a 100%.
    O cliente pode provar que o prejuízo ou custo foi inferior.
  </p>

  <h2>10. Direito de livre resolução para consumidores</h2>
  <p>
    Os consumidores podem beneficiar de um direito legal de livre resolução de 14 dias
    em contratos celebrados à distância ou fora do estabelecimento.
    Os detalhes constam da nossa página separada
    <a class="cta-link" href="/pt/withdrawal/">Informação sobre livre resolução</a>.
    Se o cliente solicitar expressamente que iniciemos o serviço antes do termo do prazo de resolução,
    e exercer depois validamente esse direito, deverá pagar um montante proporcional ao serviço já prestado.
    O direito de livre resolução pode extinguir-se antecipadamente quando o serviço estiver totalmente prestado
    nos termos legais aplicáveis.
  </p>

  <h2>11. Sem direito voluntário geral de reembolso após execução completa</h2>
  <p>
    Tratando-se de contratos de prestação de serviços, não existe um direito voluntário geral de devolução ou reembolso
    após a execução completa e adequada do serviço,
    exceto quando a lei imperativa o exigir ou quando se prove a falta ou má execução.
  </p>

  <h2>12. Reclamações e oportunidade de correção</h2>
  <p>
    Reclamações aparentes devem ser comunicadas por escrito o mais rapidamente possível,
    idealmente no prazo de 48 horas após a prestação do serviço, com descrição concreta e, quando possível, fotografias.
    Antes de recorrer a terceiros, deve ser-nos dada uma oportunidade razoável de inspeção
    e, se adequado, de correção.
  </p>

  <h2>13. Responsabilidade</h2>
  <p>
    Respondemos sem limite em caso de dolo, negligência grosseira, lesão da vida, integridade física ou saúde,
    bem como nos casos em que a lei imponha responsabilidade ilimitada.
    Em caso de negligência simples, respondemos apenas pela violação de obrigações contratuais essenciais
    e apenas pelos danos previsíveis típicos do contrato.
    Na medida permitida por lei, a responsabilidade por danos patrimoniais e materiais
    fica limitada ao valor da encomenda afetada.
  </p>

  <h2>14. Exclusão de danos indiretos</h2>
  <p>
    Na medida permitida por lei, não respondemos por danos indiretos, consequenciais,
    lucros cessantes, perda de rendas, perda de reservas, perda de uso, perdas de mercado
    ou danos resultantes de defeitos ocultos, defeitos pré-existentes, fadiga de materiais,
    corrosão, humidade, infestações, defeitos de construção ou informações incorretas fornecidas pelo cliente.
  </p>

  <h2>15. Chaves, meios de acesso e objetos sensíveis</h2>
  <p>
    O cliente deve proteger os objetos especialmente valiosos, insubstituíveis ou frágeis.
    A responsabilidade pela perda de chaves ou meios de acesso existe apenas nos termos da cláusula 13
    e, na medida permitida por lei, limita-se aos custos diretos e necessários de medidas razoáveis de segurança.
  </p>

  <h2>16. Clientes internacionais, incluindo clientes dos EUA</h2>
  <p>
    Os nossos serviços são prestados exclusivamente em Portugal.
    Na medida legalmente permitida, aplica-se a lei portuguesa.
    Para clientes empresariais, o foro exclusivo é Funchal, Madeira, Portugal.
    Para consumidores, mantêm-se inalteradas as regras imperativas de foro e de proteção do consumidor.
    Na medida legalmente permitida, excluem-se garantias implícitas não assumidas expressamente por escrito.
    Apenas o âmbito de serviço acordado é vinculativo.
  </p>

  <h2>17. Reclamações de terceiros / responsabilidade do cliente</h2>
  <p>
    O cliente continua responsável pelas decisões relativas a reparações, participações ao seguro,
    medidas de emergência e avaliações especializadas,
    salvo se tivermos aceite expressamente essas tarefas por escrito.
    Os clientes empresariais devem indemnizar-nos por reclamações de terceiros resultantes
    de instruções, informações, condições de acesso ou materiais fornecidos pelo cliente,
    salvo se a causa nos for imputável.
  </p>

  <h2>18. Força maior</h2>
  <p>
    Não somos responsáveis por atrasos ou não execução causados por circunstâncias fora do nosso controlo razoável,
    incluindo mau tempo severo, tempestades, fenómenos naturais, restrições governamentais,
    perturbações de transporte, doença ou riscos de segurança.
  </p>

  <h2>19. Livro de Reclamações e RAL</h2>
  <p>
    Sempre que legalmente exigido, disponibilizamos acesso ao sistema português de reclamações (<em>Livro de Reclamações</em>).
    Informação RAL para a Madeira:
    <br><br>
    <strong>{COMPANY["adr_name"]}</strong><br>
    {COMPANY["adr_address_1"]}<br>
    {COMPANY["adr_address_2"]}<br>
    Telefone: <a class="cta-link" href="tel:{COMPANY["adr_phone_href"]}">{COMPANY["adr_phone"]}</a><br>
    E-mail: <a class="cta-link" href="mailto:{COMPANY["adr_email"]}">{COMPANY["adr_email"]}</a><br>
    Website: <a class="cta-link" href="{COMPANY["adr_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["adr_url"]}</a><br>
    Livro de Reclamações: <a class="cta-link" href="{COMPANY["complaints_url"]}" target="_blank" rel="noopener noreferrer">{COMPANY["complaints_url"]}</a>
  </p>

  <h2>20. Plataforma ODR</h2>
  <p>
    A antiga plataforma europeia de resolução de litígios em linha foi descontinuada e já não está disponível.
  </p>

  <h2>21. Idioma</h2>
  <p>
    Para clientes internacionais, o inglês é o idioma contratual principal.
    Se estes termos também forem disponibilizados noutra língua,
    a versão inglesa prevalece em caso de conflito, na medida permitida por lei imperativa.
  </p>

  <h2>22. Cláusula de separação</h2>
  <p>
    Se alguma disposição destes Termos e Condições for ou se tornar inválida ou inexequível, no todo ou em parte,
    as restantes disposições mantêm-se em vigor.
  </p>

  <p class="small" style="margin-top:18px;">
    Página relacionada: <a class="cta-link" href="/pt/withdrawal/">Informação sobre livre resolução</a><br>
    Proteção de dados: <a class="cta-link" href="/pt/privacy/">Privacidade</a><br>
    Informação legal: <a class="cta-link" href="/pt/legal/">Informação legal</a>
  </p>
</section>
"""


def build_withdrawal_pt():
    return f"""---
layout: base.njk
lang: pt
title: "Informação sobre livre resolução | Anjo Cleaning Madeira"
description: "Informação sobre o direito de livre resolução para consumidores que reservam serviços da Anjo Cleaning na Madeira, Portugal."
permalink: /pt/withdrawal/

langLinks:
  de: /de/withdrawal/
  en: /en/withdrawal/
  fr: /fr/withdrawal/
  pt: /pt/withdrawal/
sitemap: false
---

<section class="content">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>

  <h1>Informação sobre livre resolução</h1>
  <p class="lead"><strong>Informação para consumidores sobre o direito legal de livre resolução aplicável a contratos de prestação de serviços celebrados à distância e fora do estabelecimento.</strong></p>

  <h2>Prestador</h2>
  <p>
    <strong>{COMPANY["name"]}</strong><br>
    Representada por: <strong>{COMPANY["represented_by"]}</strong><br><br>
    {'<br>'.join(COMPANY["address_lines"])}<br>
    E-mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a>
  </p>

  <h2>1. Direito legal de livre resolução</h2>
  <p>
    Se for consumidor e celebrar connosco um contrato à distância
    (por exemplo, por e-mail, formulário do website, telefone ou mensagem)
    ou fora do estabelecimento, poderá beneficiar de um direito legal de livre resolução no prazo de 14 dias, sem necessidade de indicar o motivo.
  </p>

  <h2>2. Prazo de resolução</h2>
  <p>
    O prazo de livre resolução é de 14 dias a contar da data da celebração do contrato.
  </p>

  <h2>3. Como exercer o direito de resolução</h2>
  <p>
    Para exercer o seu direito de livre resolução, deve informar-nos, através de uma declaração inequívoca,
    da sua decisão de resolver o contrato.
    Pode fazê-lo por e-mail ou por correio utilizando os contactos acima indicados.
    Pode utilizar o texto modelo abaixo, mas tal não é obrigatório.
  </p>

  <h2>4. Formulação modelo</h2>
  <p>
    Pode utilizar a seguinte formulação:
  </p>
  <p>
    “Pela presente, resolvo / resolvemos o contrato celebrado por mim / por nós relativo à prestação do seguinte serviço:
    [descrição do serviço], encomendado em [data], nome do(s) consumidor(es), morada do(s) consumidor(es), data.”
  </p>

  <h2>5. O envio dentro do prazo é suficiente</h2>
  <p>
    Para respeitar o prazo de resolução, basta que envie a comunicação relativa ao exercício do direito
    antes de terminar o respetivo prazo.
  </p>

  <h2>6. Efeitos da resolução</h2>
  <p>
    Se resolver validamente o contrato, reembolsaremos os pagamentos recebidos sem demora injustificada
    e, no máximo, no prazo de 14 dias a contar do dia em que recebemos a sua comunicação de resolução.
    O reembolso será efetuado pelo mesmo meio de pagamento utilizado na transação inicial,
    salvo acordo expresso em contrário.
  </p>

  <h2>7. Início antecipado da prestação a seu pedido</h2>
  <p>
    Se solicitar expressamente que iniciemos o serviço antes de terminar o prazo de livre resolução,
    e exercer depois validamente esse direito, terá de pagar um montante proporcional ao que já tiver sido prestado
    até ao momento em que nos informou da resolução,
    em comparação com a cobertura integral do contrato.
  </p>

  <h2>8. Perda do direito de resolução após execução integral</h2>
  <p>
    Nos contratos de prestação de serviços, o direito de livre resolução pode extinguir-se
    quando o serviço tiver sido integralmente prestado,
    desde que a execução tenha começado após o seu pedido expresso
    e depois de ter reconhecido que pode perder o direito de resolução
    quando o contrato estiver totalmente executado.
  </p>

  <h2>9. Nota prática importante para serviços urgentes e com data marcada</h2>
  <p>
    Muitos dos nossos serviços são reservados para datas específicas ou com pouca antecedência,
    por exemplo limpezas antes da chegada, serviços de presença, verificações urgentes de imóveis ou storm checks.
    Se nos pedir para começar antes de terminar o prazo de 14 dias,
    aplicam-se as regras das cláusulas 7 e 8.
  </p>

  <h2>10. Sem direito geral de livre resolução para empresas</h2>
  <p>
    Esta informação aplica-se apenas a consumidores.
    Clientes empresariais não beneficiam de um direito legal de livre resolução do consumidor,
    salvo disposição imperativa em contrário.
  </p>

  <h2>11. Contacto para comunicações de resolução</h2>
  <p>
    E-mail: <a class="cta-link" href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a><br>
    Morada postal:<br>
    <strong>{COMPANY["name"]}</strong><br>
    {'<br>'.join(COMPANY["address_lines"])}
  </p>

  <p class="small" style="margin-top:18px;">
    Página relacionada: <a class="cta-link" href="/pt/terms/">Termos e Condições</a><br>
    Proteção de dados: <a class="cta-link" href="/pt/privacy/">Privacidade</a><br>
    Informação legal: <a class="cta-link" href="/pt/legal/">Informação legal</a>
  </p>
</section>
"""


PAGES = {
    "en": {
        "terms": build_terms_en(),
        "withdrawal": build_withdrawal_en(),
    },
    "de": {
        "terms": build_terms_de(),
        "withdrawal": build_withdrawal_de(),
    },
    "fr": {
        "terms": build_terms_fr(),
        "withdrawal": build_withdrawal_fr(),
    },
    "pt": {
        "terms": build_terms_pt(),
        "withdrawal": build_withdrawal_pt(),
    },
}

def write_page(lang: str, slug: str, content: str) -> None:
    target_dir = SRC / lang / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "index.njk"
    target_file.write_text(content, encoding="utf-8")
    print(f"written: {target_file.relative_to(ROOT)}")

def main() -> None:
    if not SRC.exists():
        raise SystemExit("ERROR: src directory not found. Run this script from inside your project repository.")
    for lang, pages in PAGES.items():
        for slug, content in pages.items():
            write_page(lang, slug, content)
    print("DONE: terms and withdrawal pages created/updated in EN / DE / FR / PT.")

if __name__ == "__main__":
    main()