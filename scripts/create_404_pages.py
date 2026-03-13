from pathlib import Path

FILES = {
    "src/404.njk": """---
layout: base.njk
lang: en
title: "Page not found | Anjo Property Care Madeira"
description: "The requested page could not be found."
permalink: /404.html
eleventyExcludeFromCollections: true

langLinks:
  de: /de/404/
  en: /en/404/
  fr: /fr/404/
  pt: /pt/404/
---

<section class="text-intro">
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Page not found</h1>
  <p class="lead">
    The page you are looking for does not exist or is no longer available.
  </p>
</section>

<section class="text-flow">
  <h2>Return to the correct area</h2>
  <p>Please continue via one of the main language versions.</p>
  <ul class="sectionList">
    <li><a class="cta-link" href="/en/">English homepage</a></li>
    <li><a class="cta-link" href="/de/">Deutsche Startseite</a></li>
    <li><a class="cta-link" href="/fr/">Accueil français</a></li>
    <li><a class="cta-link" href="/pt/">Página inicial em português</a></li>
  </ul>
  <p><a class="cta-link" href="/en/contact/">Contact us directly</a></p>
</section>
""",

    "src/en/404/index.njk": """---
layout: base.njk
lang: en
title: "Page not found | Anjo Property Care Madeira"
description: "The requested page could not be found."
permalink: /en/404/
eleventyExcludeFromCollections: true

langLinks:
  de: /de/404/
  en: /en/404/
  fr: /fr/404/
  pt: /pt/404/
---

<section class="text-intro">
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Page not found</h1>
  <p class="lead">
    The page you are looking for does not exist or is no longer available.
  </p>
</section>

<section class="text-flow">
  <h2>Return to the correct area</h2>
  <p>Please continue via the main English homepage or contact us directly.</p>
  <p><a class="cta-link" href="/en/">Go to the homepage</a></p>
  <p><a class="cta-link" href="/en/contact/">Contact us</a></p>
</section>
""",

    "src/de/404/index.njk": """---
layout: base.njk
lang: de
title: "Seite nicht gefunden | Anjo Property Care Madeira"
description: "Die angeforderte Seite konnte nicht gefunden werden."
permalink: /de/404/
eleventyExcludeFromCollections: true

langLinks:
  de: /de/404/
  en: /en/404/
  fr: /fr/404/
  pt: /pt/404/
---

<section class="text-intro">
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Seite nicht gefunden</h1>
  <p class="lead">
    Die aufgerufene Seite existiert nicht oder ist nicht mehr verfügbar.
  </p>
</section>

<section class="text-flow">
  <h2>Zur richtigen Seite zurück</h2>
  <p>Bitte gehen Sie über die deutsche Startseite weiter oder nehmen Sie direkt Kontakt auf.</p>
  <p><a class="cta-link" href="/de/">Zur Startseite</a></p>
  <p><a class="cta-link" href="/de/contact/">Kontakt</a></p>
</section>
""",

    "src/fr/404/index.njk": """---
layout: base.njk
lang: fr
title: "Page introuvable | Anjo Property Care Madeira"
description: "La page demandée est introuvable."
permalink: /fr/404/
eleventyExcludeFromCollections: true

langLinks:
  de: /de/404/
  en: /en/404/
  fr: /fr/404/
  pt: /pt/404/
---

<section class="text-intro">
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Page introuvable</h1>
  <p class="lead">
    La page demandée n’existe pas ou n’est plus disponible.
  </p>
</section>

<section class="text-flow">
  <h2>Revenir à la bonne page</h2>
  <p>Veuillez continuer via la page d’accueil française ou nous contacter directement.</p>
  <p><a class="cta-link" href="/fr/">Retour à l’accueil</a></p>
  <p><a class="cta-link" href="/fr/contact/">Nous contacter</a></p>
</section>
""",

    "src/pt/404/index.njk": """---
layout: base.njk
lang: pt
title: "Página não encontrada | Anjo Property Care Madeira"
description: "A página solicitada não foi encontrada."
permalink: /pt/404/
eleventyExcludeFromCollections: true

langLinks:
  de: /de/404/
  en: /en/404/
  fr: /fr/404/
  pt: /pt/404/
---

<section class="text-intro">
  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Página não encontrada</h1>
  <p class="lead">
    A página solicitada não existe ou já não está disponível.
  </p>
</section>

<section class="text-flow">
  <h2>Voltar à página correta</h2>
  <p>Continue através da página inicial em português ou entre em contacto diretamente.</p>
  <p><a class="cta-link" href="/pt/">Ir para a página inicial</a></p>
  <p><a class="cta-link" href="/pt/contact/">Entrar em contacto</a></p>
</section>
""",
}

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"OK: {file_path}")

print("\\n404 pages created.")