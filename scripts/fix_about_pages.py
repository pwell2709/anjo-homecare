from pathlib import Path

FILES = {
    "src/de/about/index.njk": """---
layout: base.njk
lang: de
title: Über Anjo Cleaning Madeira | Ablauf, Qualität & Standards
description: "Erfahren Sie mehr über unser Luxury Property Care auf Madeira, unsere Standards, ausgewählte Services und wie wir hochwertige Immobilien für internationale Eigentümer betreuen."
permalink: /de/about/

langLinks:
  de: /de/about/
  en: /en/about/
  fr: /fr/about/
  pt: /pt/about/
---

<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Über uns</h1>
  <p class="lead">
    Anjo Cleaning steht für diskretes Property Care und ausgewählte Premium-Services auf Madeira — geprägt von deutschen Standards, klaren Abläufen und echter Inselverbundenheit.
  </p>
</section>

<section class="text-flow">
  <h2>Wo deutsche Präzision auf Madeira trifft</h2>
  <p>Anjo Cleaning basiert auf einem persönlichen Weg: von Deutschland nach Madeira — an einen Ort, der schnell zu einem Zuhause geworden ist.</p>
  <p>Wir bringen genau das mit, was Eigentümer hochwertiger Immobilien am meisten brauchen: Zuverlässigkeit, Pünktlichkeit und einen kompromisslosen Blick für Details. Vor Ort ergänzen wir das durch praktische Erfahrung und direkte, transparente Kommunikation.</p>
</section>

<section class="text-flow">
  <h2>Unsere Philosophie: das Beste aus zwei Welten</h2>
  <ul class="sectionList">
    <li><strong>Deutsche Gründlichkeit:</strong> strukturierte Abläufe, Checklisten und konsequente Endkontrollen — für Ergebnisse, die sichtbar und verlässlich sind.</li>
    <li><strong>Inselbewusstsein:</strong> Respekt für Ihre Immobilie, Einrichtung und Umgebung — wir behandeln jedes Objekt, als wäre es unser eigenes.</li>
    <li><strong>Echte Verlässlichkeit:</strong> klare Absprachen, pünktliche Ausführung, schnelles Feedback — damit Sie jederzeit den Überblick behalten.</li>
  </ul>
</section>

<section class="text-flow">
  <h2>Warum „Anjo“?</h2>
  <p>„Anjo“ bedeutet Engel — und genau so verstehen wir unsere Rolle: als ruhige, verlässliche Hand im Hintergrund, die Ihre Immobilie gepflegt, präsentabel und jederzeit bereit hält — ob private Residenz, Zweitwohnsitz oder sorgfältig betreutes Objekt auf Madeira.</p>
  <div aria-label="Founder quote" class="quote">
    <p>"Meine Liebe zu Madeira treibt mich an, diese Insel Stück für Stück schöner zu machen — Immobilie für Immobilie, mit Präzision und Herz."</p>
    <div class="sig">Florian Engelmann, CEO</div>
  </div>
</section>

<section class="text-flow">
  <h2>Ihr Partner auf Madeira — auch aus der Ferne</h2>
  <p>Ob Sie selbst auf Madeira leben oder Ihre Immobilie aus dem Ausland betreuen lassen: Anjo Cleaning ist der Partner, der Premium-Qualität liefert, Verantwortung übernimmt und mit Werten arbeitet, auf die Sie sich verlassen können.</p>
  <p>
    Erfahren Sie mehr über unsere <a class="cta-link" data-local-link href="/de/landing/alto/">Reinigung für Alojamento Local auf Madeira</a> oder <a class="cta-link" href="/de/contact/">kontaktieren Sie uns direkt</a> zu Ihrer Immobilie auf Madeira.
  </p>
  <p>
    Unser Fokus liegt auf diskretem Property Care für hochwertige Immobilien sowie auf ausgewählten Premium-Services, die Eigentümern helfen, ihr Objekt geschützt, vorbereitet und dauerhaft auf hohem Niveau betreut zu halten.
  </p>
</section>
""",

    "src/en/about/index.njk": """---
layout: base.njk
lang: en
title: About Anjo Cleaning Madeira | Process, Quality & Standards
description: "Learn more about our luxury Property Care in Madeira, our standards, selected services and how we protect high-end properties for international owners."
permalink: /en/about/

langLinks:
  de: /de/about/
  en: /en/about/
  fr: /fr/about/
  pt: /pt/about/
---

<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>About us</h1>
  <p class="lead">
    Anjo Cleaning delivers discreet Property Care and selected premium services in Madeira — guided by German standards, clear routines, and genuine island commitment.
  </p>
</section>

<section class="text-flow">
  <h2>Where German precision meets Madeira</h2>
  <p>Anjo Cleaning is built on a personal journey: from Germany to Madeira — a place that quickly became home.</p>
  <p>We bring what property owners need most: reliability, punctuality, and an uncompromising eye for detail. Locally, we add hands-on experience and direct, transparent communication.</p>
</section>

<section class="text-flow">
  <h2>Our philosophy: the best of two worlds</h2>
  <ul class="sectionList">
    <li><strong>German thoroughness:</strong> structured workflows, checklists, and consistent final inspections — for results you can see and trust.</li>
    <li><strong>Island care:</strong> respect for your property, furnishings, and surroundings — we treat every home as if it were our own.</li>
    <li><strong>True reliability:</strong> clear agreements, on-time delivery, fast feedback — so you stay in control at all times.</li>
  </ul>
</section>

<section class="text-flow">
  <h2>Why "Anjo"?</h2>
  <p>"Anjo" means angel — and that is how we see our role: a calm, dependable hand in the background that keeps your property maintained, presentable, and ready whenever you need it — whether it is a private residence, second home, or carefully managed property in Madeira.</p>
  <div aria-label="Founder quote" class="quote">
    <p>"My love for Madeira drives me to make this island a little more beautiful — property by property, with precision and heart."</p>
    <div class="sig">Florian Engelmann, CEO</div>
  </div>
</section>

<section class="text-flow">
  <h2>Your partner in Madeira — even from afar</h2>
  <p>Whether you live in Madeira or manage your property remotely, Anjo Cleaning is the partner that delivers premium quality, takes responsibility, and works with values you can trust.</p>
  <p>
    Learn more about our <a class="cta-link" data-local-link href="/en/landing/alto/">Cleaning for Alojamento Local in Madeira</a> and <a class="cta-link" href="/en/contact/">get in touch directly</a> about your property in Madeira.
  </p>
  <p>
    Our focus is discreet Property Care for high-end homes and selected premium services that help owners keep their property protected, prepared, and consistently maintained to a high standard.
  </p>
</section>
""",

    "src/fr/about/index.njk": """---
layout: base.njk
lang: fr
title: À propos d’Anjo Cleaning Madeira | Processus, qualité et standards
description: "Découvrez notre Property Care haut de gamme à Madère, nos standards, nos services sélectionnés et la manière dont nous protégeons les propriétés de standing pour des propriétaires internationaux."
permalink: /fr/about/

langLinks:
  de: /de/about/
  en: /en/about/
  fr: /fr/about/
  pt: /pt/about/
---

<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>À propos</h1>
  <p class="lead">
    Anjo Cleaning propose un Property Care discret et des services premium sélectionnés à Madère — guidés par des standards allemands, des processus clairs et un véritable attachement à l’île.
  </p>
</section>

<section class="text-flow">
  <h2>Là où la précision allemande rencontre Madère</h2>
  <p>Anjo Cleaning repose sur un parcours personnel : de l’Allemagne à Madère — un lieu devenu rapidement un foyer.</p>
  <p>Nous apportons exactement ce dont les propriétaires de biens haut de gamme ont le plus besoin : fiabilité, ponctualité et sens du détail sans compromis. Sur place, nous y ajoutons une expérience concrète et une communication directe et transparente.</p>
</section>

<section class="text-flow">
  <h2>Notre philosophie : le meilleur de deux mondes</h2>
  <ul class="sectionList">
    <li><strong>Rigueur allemande :</strong> des processus structurés, des check-lists et des contrôles finaux systématiques — pour des résultats visibles et fiables.</li>
    <li><strong>Sensibilité locale :</strong> du respect pour votre propriété, son aménagement et son environnement — nous traitons chaque bien comme s’il s’agissait du nôtre.</li>
    <li><strong>Véritable fiabilité :</strong> accords clairs, exécution ponctuelle, retour rapide — pour que vous gardiez le contrôle à tout moment.</li>
  </ul>
</section>

<section class="text-flow">
  <h2>Pourquoi « Anjo » ?</h2>
  <p>« Anjo » signifie ange — et c’est exactement ainsi que nous voyons notre rôle : une présence calme et fiable en arrière-plan, qui maintient votre propriété soignée, présentable et prête à tout moment — qu’il s’agisse d’une résidence privée, d’une résidence secondaire ou d’un bien soigneusement suivi à Madère.</p>
  <div aria-label="Founder quote" class="quote">
    <p>"Mon amour pour Madère me pousse à rendre cette île un peu plus belle — propriété après propriété, avec précision et cœur."</p>
    <div class="sig">Florian Engelmann, CEO</div>
  </div>
</section>

<section class="text-flow">
  <h2>Votre partenaire à Madère — même à distance</h2>
  <p>Que vous viviez à Madère ou que vous gériez votre propriété depuis l’étranger, Anjo Cleaning est le partenaire qui offre une qualité premium, assume ses responsabilités et travaille avec des valeurs dignes de confiance.</p>
  <p>
    Découvrez notre <a class="cta-link" data-local-link href="/fr/landing/alto/">Nettoyage pour Alojamento Local à Madère</a> ou <a class="cta-link" href="/fr/contact/">contactez-nous directement</a> au sujet de votre propriété à Madère.
  </p>
  <p>
    Notre priorité est un Property Care discret pour des biens haut de gamme ainsi que des services premium sélectionnés qui aident les propriétaires à garder leur propriété protégée, préparée et durablement entretenue à un niveau élevé.
  </p>
</section>
""",

    "src/pt/about/index.njk": """---
layout: base.njk
lang: pt
title: Sobre a Anjo Cleaning Madeira | Processos, qualidade e padrões
description: "Saiba mais sobre o nosso Property Care de luxo na Madeira, os nossos padrões, serviços selecionados e a forma como protegemos propriedades de alto padrão para proprietários internacionais."
permalink: /pt/about/

langLinks:
  de: /de/about/
  en: /en/about/
  fr: /fr/about/
  pt: /pt/about/
---

<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Sobre nós</h1>
  <p class="lead">
    A Anjo Cleaning oferece Property Care discreto e serviços premium selecionados na Madeira — orientados por padrões alemães, processos claros e uma ligação genuína à ilha.
  </p>
</section>

<section class="text-flow">
  <h2>Onde a precisão alemã encontra a Madeira</h2>
  <p>A Anjo Cleaning nasce de um percurso pessoal: da Alemanha para a Madeira — um lugar que rapidamente se tornou casa.</p>
  <p>Trazemos exatamente aquilo de que os proprietários de imóveis de alto padrão mais precisam: fiabilidade, pontualidade e um olhar rigoroso para os detalhes. Localmente, juntamos experiência prática e comunicação direta e transparente.</p>
</section>

<section class="text-flow">
  <h2>A nossa filosofia: o melhor de dois mundos</h2>
  <ul class="sectionList">
    <li><strong>Rigor alemão:</strong> processos estruturados, checklists e controlo final consistente — para resultados visíveis e fiáveis.</li>
    <li><strong>Sensibilidade pela ilha:</strong> respeito pela sua propriedade, pelo mobiliário e pela envolvente — tratamos cada imóvel como se fosse nosso.</li>
    <li><strong>Verdadeira fiabilidade:</strong> acordos claros, execução pontual, resposta rápida — para que mantenha sempre o controlo.</li>
  </ul>
</section>

<section class="text-flow">
  <h2>Porque “Anjo”?</h2>
  <p>“Anjo” significa anjo — e é exatamente assim que vemos o nosso papel: uma presença calma e fiável nos bastidores, que mantém a sua propriedade cuidada, apresentável e pronta sempre que necessário — seja uma residência privada, uma segunda habitação ou um imóvel cuidadosamente acompanhado na Madeira.</p>
  <div aria-label="Founder quote" class="quote">
    <p>"O meu amor pela Madeira motiva-me a tornar esta ilha um pouco mais bonita — propriedade após propriedade, com precisão e coração."</p>
    <div class="sig">Florian Engelmann, CEO</div>
  </div>
</section>

<section class="text-flow">
  <h2>O seu parceiro na Madeira — mesmo à distância</h2>
  <p>Quer viva na Madeira ou acompanhe a sua propriedade a partir do estrangeiro, a Anjo Cleaning é o parceiro que entrega qualidade premium, assume responsabilidade e trabalha com valores em que pode confiar.</p>
  <p>
    Saiba mais sobre a nossa <a class="cta-link" data-local-link href="/pt/landing/alto/">Limpeza para Alojamento Local na Madeira</a> ou <a class="cta-link" href="/pt/contact/">entre em contacto diretamente</a> sobre a sua propriedade na Madeira.
  </p>
  <p>
    O nosso foco está no Property Care discreto para imóveis de alto padrão e em serviços premium selecionados que ajudam os proprietários a manter a sua propriedade protegida, preparada e consistentemente cuidada a um nível elevado.
  </p>
</section>
""",
}

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"OK: {file_path}")

print("\\nAlle 4 About-Seiten wurden neu geschrieben.")