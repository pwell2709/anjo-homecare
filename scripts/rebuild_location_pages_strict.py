#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rewrites all 17 location pages in DE/EN/FR/PT with long-form, location-specific content
to reduce duplicate-content risk and bring each page into the 900-1200 word range.

This strict version also:
- scans both src and _site for unresolved placeholders like {loc}
- mirrors the rewritten content into _site if matching built files exist
- aborts on any unresolved placeholder in source or build output

Run from the project root:
    python scripts/rebuild_location_pages_strict.py
or:
    python rebuild_location_pages_strict.py
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from collections import Counter

LOCATIONS = {
  "boaventura": {
    "region": "north_green",
    "setting": "rural_hillside",
    "property_mix": [
      "stone_retreats",
      "sea_view_villas",
      "garden_estates"
    ],
    "owners": [
      "second_home",
      "long_stay_retreat"
    ],
    "pressures": [
      "humidity",
      "growth",
      "drainage"
    ],
    "ops": [
      "garden_control",
      "hillside_checks",
      "arrival_readiness"
    ],
    "vendors": "remote_coordination",
    "signature": {
      "de": "Boaventura passt zu Eigentümern, die Ruhe, Landschaft und Rückzug höher gewichten als schnelle urbane Verfügbarkeit.",
      "en": "Boaventura suits owners who value silence, landscape and retreat more than quick urban convenience.",
      "fr": "Boaventura convient aux propriétaires qui privilégient le calme, le paysage et le retrait plutôt que la commodité urbaine immédiate.",
      "pt": "Boaventura adequa-se a proprietários que valorizam silêncio, paisagem e recolhimento acima da conveniência urbana imediata."
    },
    "name": {
      "de": "Boaventura",
      "en": "Boaventura",
      "fr": "Boaventura",
      "pt": "Boaventura"
    }
  },
  "calheta": {
    "region": "sunny_southwest",
    "setting": "marina_hillside",
    "property_mix": [
      "design_villas",
      "pool_homes",
      "ocean_terraces"
    ],
    "owners": [
      "second_home",
      "international_family"
    ],
    "pressures": [
      "sun_uv",
      "salt_air",
      "pool_areas"
    ],
    "ops": [
      "arrival_readiness",
      "pool_garden_standard",
      "vendor_coordination"
    ],
    "vendors": "premium_trades",
    "signature": {
      "de": "Calheta verlangt einen Auftritt, der zur modernen Architektur passt: klar, repräsentativ und jederzeit bereit für Eigentümer oder Gäste.",
      "en": "Calheta demands a presentation that matches modern architecture: crisp, representative and always ready for owners or guests.",
      "fr": "Calheta exige une présentation à la hauteur de son architecture contemporaine: nette, représentative et toujours prête pour les propriétaires ou leurs invités.",
      "pt": "Calheta exige uma apresentação à altura da sua arquitetura contemporânea: limpa, representativa e sempre pronta para proprietários ou convidados."
    },
    "name": {
      "de": "Calheta",
      "en": "Calheta",
      "fr": "Calheta",
      "pt": "Calheta"
    }
  },
  "camara-de-lobos": {
    "region": "cliffside_south",
    "setting": "urban_hillside",
    "property_mix": [
      "cliff_villas",
      "mixed_residences",
      "panoramic_homes"
    ],
    "owners": [
      "second_home",
      "frequent_short_stays"
    ],
    "pressures": [
      "salt_air",
      "traffic_access",
      "retaining_walls"
    ],
    "ops": [
      "access_logistics",
      "presentation_standard",
      "technical_checks"
    ],
    "vendors": "urban_coordination",
    "signature": {
      "de": "In Câmara de Lobos trifft spektakuläre Lage auf kurze Wege nach Funchal, was die Region für anspruchsvolle Eigentümer besonders attraktiv macht.",
      "en": "In Câmara de Lobos, spectacular scenery meets fast access to Funchal, which makes the area especially attractive to demanding owners.",
      "fr": "À Câmara de Lobos, le paysage spectaculaire rencontre l'accès rapide à Funchal, ce qui rend la zone particulièrement attractive pour des propriétaires exigeants.",
      "pt": "Em Câmara de Lobos, a paisagem espetacular encontra acesso rápido ao Funchal, o que torna a zona especialmente atrativa para proprietários exigentes."
    },
    "name": {
      "de": "Câmara de Lobos",
      "en": "Câmara de Lobos",
      "fr": "Câmara de Lobos",
      "pt": "Câmara de Lobos"
    }
  },
  "campanario": {
    "region": "central_south",
    "setting": "quiet_hillside",
    "property_mix": [
      "family_villas",
      "terrace_homes",
      "garden_properties"
    ],
    "owners": [
      "residential_with_absence",
      "second_home"
    ],
    "pressures": [
      "wind_exposure",
      "garden_growth",
      "exterior_wear"
    ],
    "ops": [
      "routine_checks",
      "garden_control",
      "vendor_coordination"
    ],
    "vendors": "central_coordination",
    "signature": {
      "de": "Campanário wirkt ruhiger als die großen Hotspots, ist aber genau deshalb ideal für Eigentümer, die diskrete Ordnung statt touristischer Unruhe suchen.",
      "en": "Campanário feels calmer than the major hotspots and is therefore ideal for owners who prefer discreet order to tourist intensity.",
      "fr": "Campanário paraît plus paisible que les grands points chauds et convient donc parfaitement aux propriétaires qui préfèrent l'ordre discret à l'agitation touristique.",
      "pt": "Campanário parece mais tranquilo do que os grandes pontos quentes e por isso é ideal para proprietários que preferem ordem discreta à intensidade turística."
    },
    "name": {
      "de": "Campanário",
      "en": "Campanário",
      "fr": "Campanário",
      "pt": "Campanário"
    }
  },
  "canico": {
    "region": "east_south",
    "setting": "residential_coast",
    "property_mix": [
      "premium_apartments",
      "residence_villas",
      "sea_view_condos"
    ],
    "owners": [
      "second_home",
      "work_travel"
    ],
    "pressures": [
      "salt_air",
      "shared_access",
      "balcony_exposure"
    ],
    "ops": [
      "arrival_readiness",
      "building_coordination",
      "presentation_standard"
    ],
    "vendors": "residential_coordination",
    "signature": {
      "de": "Caniço verlangt oft einen anderen Betreuungsstil als reine Villenlagen, weil Apartments, Residenzen und Gemeinschaftsbereiche sauber eingebunden werden müssen.",
      "en": "Caniço often requires a different supervision style than pure villa districts because apartments, residences and shared access points need to be integrated cleanly.",
      "fr": "Caniço demande souvent un style de suivi différent des quartiers composés uniquement de villas, car appartements, résidences et accès communs doivent être intégrés avec précision.",
      "pt": "O Caniço exige muitas vezes um estilo de acompanhamento diferente das zonas compostas apenas por villas, porque apartamentos, residências e acessos comuns têm de ser integrados com rigor."
    },
    "name": {
      "de": "Caniço",
      "en": "Caniço",
      "fr": "Caniço",
      "pt": "Caniço"
    }
  },
  "curral-das-freiras": {
    "region": "mountain_valley",
    "setting": "isolated_mountain",
    "property_mix": [
      "mountain_houses",
      "retreat_properties",
      "heritage_homes"
    ],
    "owners": [
      "retreat_use",
      "seasonal_use"
    ],
    "pressures": [
      "humidity",
      "weather_swings",
      "access_challenges"
    ],
    "ops": [
      "weather_readiness",
      "drainage_checks",
      "remote_coordination"
    ],
    "vendors": "limited_access",
    "signature": {
      "de": "Curral das Freiras ist keine klassische Küstenlage, sondern eine geschützte Bergwelt, in der Betreuung vor allem auf Verlässlichkeit, Wetterbeobachtung und Planung basiert.",
      "en": "Curral das Freiras is not a classic coastal address but a protected mountain setting where supervision depends above all on reliability, weather awareness and planning.",
      "fr": "Curral das Freiras n'est pas une adresse côtière classique, mais un univers de montagne protégé où le suivi repose avant tout sur la fiabilité, l'observation du temps et l'anticipation.",
      "pt": "Curral das Freiras não é uma localização costeira clássica, mas um cenário de montanha protegido onde o acompanhamento depende acima de tudo de fiabilidade, atenção ao tempo e planeamento."
    },
    "name": {
      "de": "Curral das Freiras",
      "en": "Curral das Freiras",
      "fr": "Curral das Freiras",
      "pt": "Curral das Freiras"
    }
  },
  "funchal": {
    "region": "capital_city",
    "setting": "urban_premium",
    "property_mix": [
      "city_apartments",
      "penthouses",
      "hillside_villas"
    ],
    "owners": [
      "frequent_arrivals",
      "international_family"
    ],
    "pressures": [
      "city_logistics",
      "presentation_standard",
      "technical_systems"
    ],
    "ops": [
      "access_logistics",
      "arrival_readiness",
      "vendor_coordination"
    ],
    "vendors": "city_speed",
    "signature": {
      "de": "Funchal verbindet repräsentatives Wohnen, kurze Wege und hohe Erwartungen an Diskretion, Tempo und perfekten Zustand bei jeder Rückkehr.",
      "en": "Funchal combines representative living with short distances and high expectations regarding discretion, speed and perfect condition at every return.",
      "fr": "Funchal réunit habitat représentatif, distances courtes et fortes attentes en matière de discrétion, de réactivité et d'état impeccable à chaque retour.",
      "pt": "O Funchal combina habitação representativa, distâncias curtas e expectativas elevadas de discrição, rapidez e estado impecável em cada regresso."
    },
    "name": {
      "de": "Funchal",
      "en": "Funchal",
      "fr": "Funchal",
      "pt": "Funchal"
    }
  },
  "jardim-do-mar": {
    "region": "west_seaside",
    "setting": "village_cliff",
    "property_mix": [
      "renovated_houses",
      "coastal_retreats",
      "terrace_homes"
    ],
    "owners": [
      "retreat_use",
      "creative_remote"
    ],
    "pressures": [
      "salt_air",
      "humidity",
      "narrow_access"
    ],
    "ops": [
      "access_logistics",
      "exterior_checks",
      "arrival_readiness"
    ],
    "vendors": "narrow_lane_coordination",
    "signature": {
      "de": "Jardim do Mar lebt von Atmosphäre, Küstennähe und Charakter, weshalb kleine Nachlässigkeiten den Eindruck einer hochwertigen Immobilie besonders schnell stören.",
      "en": "Jardim do Mar lives from atmosphere, proximity to the ocean and character, which means small neglect quickly disrupts the impression of a premium property.",
      "fr": "Jardim do Mar vit de son atmosphère, de sa proximité avec l'océan et de son caractère, ce qui signifie que la moindre négligence perturbe vite l'image d'un bien haut de gamme.",
      "pt": "Jardim do Mar vive da sua atmosfera, da proximidade ao oceano e do seu carácter, o que significa que pequenas negligências perturbam rapidamente a imagem de um imóvel premium."
    },
    "name": {
      "de": "Jardim do Mar",
      "en": "Jardim do Mar",
      "fr": "Jardim do Mar",
      "pt": "Jardim do Mar"
    }
  },
  "paul-do-mar": {
    "region": "sunny_far_west",
    "setting": "surf_coast",
    "property_mix": [
      "holiday_villas",
      "oceanfront_homes",
      "terrace_properties"
    ],
    "owners": [
      "short_rental_with_private_use",
      "second_home"
    ],
    "pressures": [
      "sun_uv",
      "salt_air",
      "fast_turnover"
    ],
    "ops": [
      "arrival_readiness",
      "presentation_standard",
      "exterior_checks"
    ],
    "vendors": "coastal_coordination",
    "signature": {
      "de": "Paul do Mar verbindet extreme Küstennähe mit viel Sonne und einem lässigen Image, verlangt im Hintergrund aber eine sehr präzise Organisation.",
      "en": "Paul do Mar combines extreme coastal proximity with intense sun and a relaxed image, yet behind the scenes it requires very precise organisation.",
      "fr": "Paul do Mar associe une proximité extrême avec l'océan, beaucoup de soleil et une image décontractée, tout en exigeant en coulisses une organisation très précise.",
      "pt": "Paul do Mar combina proximidade extrema ao oceano, muito sol e uma imagem descontraída, mas nos bastidores exige uma organização muito precisa."
    },
    "name": {
      "de": "Paul do Mar",
      "en": "Paul do Mar",
      "fr": "Paul do Mar",
      "pt": "Paul do Mar"
    }
  },
  "ponta-do-pargo": {
    "region": "far_west_plateau",
    "setting": "remote_exposed",
    "property_mix": [
      "estate_villas",
      "view_properties",
      "large_plots"
    ],
    "owners": [
      "seasonal_use",
      "privacy_first"
    ],
    "pressures": [
      "wind_exposure",
      "distance",
      "exterior_wear"
    ],
    "ops": [
      "remote_coordination",
      "weather_readiness",
      "garden_control"
    ],
    "vendors": "remote_coordination",
    "signature": {
      "de": "Ponta do Pargo ist eine Lage für Eigentümer, die Weite, Ruhe und Privatsphäre suchen und deshalb eine besonders selbständige Betreuung brauchen.",
      "en": "Ponta do Pargo is for owners who seek openness, silence and privacy and therefore need especially autonomous supervision.",
      "fr": "Ponta do Pargo est une adresse pour des propriétaires en quête d'espace, de silence et de confidentialité, et qui ont donc besoin d'un suivi particulièrement autonome.",
      "pt": "A Ponta do Pargo é um endereço para proprietários que procuram amplitude, silêncio e privacidade e por isso precisam de um acompanhamento especialmente autónomo."
    },
    "name": {
      "de": "Ponta do Pargo",
      "en": "Ponta do Pargo",
      "fr": "Ponta do Pargo",
      "pt": "Ponta do Pargo"
    }
  },
  "ponta-do-sol": {
    "region": "sunny_south",
    "setting": "design_hillside",
    "property_mix": [
      "designer_villas",
      "glass_homes",
      "pool_homes"
    ],
    "owners": [
      "second_home",
      "creative_remote"
    ],
    "pressures": [
      "sun_uv",
      "pool_areas",
      "glass_exposure"
    ],
    "ops": [
      "presentation_standard",
      "arrival_readiness",
      "technical_checks"
    ],
    "vendors": "premium_trades",
    "signature": {
      "de": "Ponta do Sol steht für Licht, Architektur und ein sehr bewusst kuratiertes Lebensgefühl, das nur mit konstant hoher Pflegequalität funktioniert.",
      "en": "Ponta do Sol stands for light, architecture and a deliberately curated lifestyle that only works with consistently high care standards.",
      "fr": "Ponta do Sol incarne la lumière, l'architecture et un art de vivre très intentionnel qui ne fonctionne qu'avec un niveau de soin constamment élevé.",
      "pt": "A Ponta do Sol representa luz, arquitetura e um estilo de vida muito intencional que só funciona com um nível de cuidado consistentemente elevado."
    },
    "name": {
      "de": "Ponta do Sol",
      "en": "Ponta do Sol",
      "fr": "Ponta do Sol",
      "pt": "Ponta do Sol"
    }
  },
  "porto-moniz": {
    "region": "northwest_coast",
    "setting": "lava_coast",
    "property_mix": [
      "holiday_homes",
      "view_villas",
      "stone_properties"
    ],
    "owners": [
      "seasonal_use",
      "second_home"
    ],
    "pressures": [
      "salt_air",
      "weather_swings",
      "distance"
    ],
    "ops": [
      "weather_readiness",
      "arrival_readiness",
      "remote_coordination"
    ],
    "vendors": "remote_coordination",
    "signature": {
      "de": "Porto Moniz fasziniert durch seine dramatische Küste, verlangt wegen Wetter, Distanz und Meersalz aber eine besonders vorausschauende Betreuung.",
      "en": "Porto Moniz fascinates with its dramatic coastline, yet weather, distance and sea salt require especially forward-looking supervision.",
      "fr": "Porto Moniz séduit par son littoral spectaculaire, mais le temps, la distance et le sel marin exigent un suivi particulièrement anticipatif.",
      "pt": "O Porto Moniz fascina pela sua costa dramática, mas o tempo, a distância e o sal marinho exigem um acompanhamento especialmente preventivo."
    },
    "name": {
      "de": "Porto Moniz",
      "en": "Porto Moniz",
      "fr": "Porto Moniz",
      "pt": "Porto Moniz"
    }
  },
  "ribeira-brava": {
    "region": "central_south",
    "setting": "connected_valley",
    "property_mix": [
      "family_villas",
      "mixed_residences",
      "hillside_homes"
    ],
    "owners": [
      "residential_with_absence",
      "second_home"
    ],
    "pressures": [
      "sun_uv",
      "traffic_access",
      "garden_growth"
    ],
    "ops": [
      "routine_checks",
      "access_logistics",
      "vendor_coordination"
    ],
    "vendors": "central_coordination",
    "signature": {
      "de": "Ribeira Brava profitiert von seiner zentralen Lage, doch genau diese gute Erreichbarkeit erhöht oft die Erwartungen an Tempo, Koordination und ständige Einsatzbereitschaft.",
      "en": "Ribeira Brava benefits from its central position, yet that very accessibility often raises expectations regarding speed, coordination and constant readiness.",
      "fr": "Ribeira Brava profite de sa position centrale, mais cette accessibilité augmente souvent les attentes en matière de réactivité, de coordination et de disponibilité.",
      "pt": "A Ribeira Brava beneficia da sua posição central, mas essa mesma acessibilidade aumenta frequentemente as expectativas em relação a rapidez, coordenação e disponibilidade."
    },
    "name": {
      "de": "Ribeira Brava",
      "en": "Ribeira Brava",
      "fr": "Ribeira Brava",
      "pt": "Ribeira Brava"
    }
  },
  "santa-cruz": {
    "region": "airport_coast",
    "setting": "connected_coast",
    "property_mix": [
      "coastal_villas",
      "apartments",
      "family_residences"
    ],
    "owners": [
      "frequent_arrivals",
      "work_travel"
    ],
    "pressures": [
      "wind_exposure",
      "salt_air",
      "arrival_cycles"
    ],
    "ops": [
      "arrival_readiness",
      "access_logistics",
      "building_coordination"
    ],
    "vendors": "airport_corridor",
    "signature": {
      "de": "Santa Cruz profitiert von der Nähe zum Flughafen und von guten Verbindungen, wodurch Eigentümer oft spontanere Anreisen und einen sofort funktionsfähigen Zustand erwarten.",
      "en": "Santa Cruz benefits from airport proximity and strong connections, so owners often expect more spontaneous arrivals and a home that works immediately.",
      "fr": "Santa Cruz profite de la proximité de l'aéroport et de bonnes liaisons, si bien que les propriétaires attendent souvent des arrivées plus spontanées et un bien immédiatement fonctionnel.",
      "pt": "Santa Cruz beneficia da proximidade ao aeroporto e de boas ligações, pelo que os proprietários esperam muitas vezes chegadas mais espontâneas e um imóvel imediatamente funcional."
    },
    "name": {
      "de": "Santa Cruz",
      "en": "Santa Cruz",
      "fr": "Santa Cruz",
      "pt": "Santa Cruz"
    }
  },
  "santana": {
    "region": "north_forest",
    "setting": "rural_green",
    "property_mix": [
      "heritage_homes",
      "estate_houses",
      "garden_properties"
    ],
    "owners": [
      "retreat_use",
      "seasonal_use"
    ],
    "pressures": [
      "humidity",
      "roof_wear",
      "garden_growth"
    ],
    "ops": [
      "weather_readiness",
      "garden_control",
      "routine_checks"
    ],
    "vendors": "rural_coordination",
    "signature": {
      "de": "Santana steht für Grün, traditionelle Baukultur und größere Grundstücke, was Property Care hier besonders stark mit Substanzschutz verbindet.",
      "en": "Santana stands for greenery, traditional building culture and larger plots, which means Property Care here is closely tied to protecting the substance of the home.",
      "fr": "Santana évoque la verdure, l'architecture traditionnelle et les parcelles plus vastes, ce qui lie ici le Property Care à la préservation même du bâti.",
      "pt": "Santana representa verde, cultura construtiva tradicional e lotes maiores, o que liga aqui o Property Care à uma forte proteção da própria estrutura do imóvel."
    },
    "name": {
      "de": "Santana",
      "en": "Santana",
      "fr": "Santana",
      "pt": "Santana"
    }
  },
  "sao-jorge": {
    "region": "north_terraces",
    "setting": "green_hillside",
    "property_mix": [
      "traditional_houses",
      "estate_villas",
      "terrace_properties"
    ],
    "owners": [
      "seasonal_use",
      "privacy_first"
    ],
    "pressures": [
      "humidity",
      "steep_access",
      "garden_growth"
    ],
    "ops": [
      "hillside_checks",
      "garden_control",
      "remote_coordination"
    ],
    "vendors": "rural_coordination",
    "signature": {
      "de": "São Jorge verlangt wegen seiner Hanglagen, Gärten und Nordküstenfeuchte eine Betreuung, die Natur und Gebäude gemeinsam denkt.",
      "en": "Because of its slopes, gardens and north-coast humidity, São Jorge needs supervision that thinks about landscape and building as one system.",
      "fr": "En raison de ses pentes, de ses jardins et de l'humidité de la côte nord, São Jorge a besoin d'un suivi qui considère paysage et bâtiment comme un seul système.",
      "pt": "Devido às encostas, aos jardins e à humidade da costa norte, São Jorge precisa de um acompanhamento que pense paisagem e edifício como um único sistema."
    },
    "name": {
      "de": "São Jorge",
      "en": "São Jorge",
      "fr": "São Jorge",
      "pt": "São Jorge"
    }
  },
  "sao-vicente": {
    "region": "north_valley",
    "setting": "valley_village",
    "property_mix": [
      "restored_houses",
      "view_villas",
      "stone_properties"
    ],
    "owners": [
      "seasonal_use",
      "second_home"
    ],
    "pressures": [
      "humidity",
      "drainage",
      "weather_swings"
    ],
    "ops": [
      "routine_checks",
      "weather_readiness",
      "arrival_readiness"
    ],
    "vendors": "rural_coordination",
    "signature": {
      "de": "São Vicente kombiniert Tal, Berge und Nordküste, weshalb Häuser hier oft gleichzeitig gegen Feuchte, Pflanzenwachstum und wetterbedingte Belastung geschützt werden müssen.",
      "en": "São Vicente combines valley, mountains and north coast, so homes often need protection from humidity, plant growth and weather-driven wear at the same time.",
      "fr": "São Vicente combine vallée, montagne et côte nord, si bien que les maisons doivent souvent être protégées en même temps contre l'humidité, la végétation et l'usure liée au temps.",
      "pt": "São Vicente combina vale, montanha e costa norte, pelo que as casas precisam muitas vezes de proteção simultânea contra humidade, crescimento vegetal e desgaste provocado pelo tempo."
    },
    "name": {
      "de": "São Vicente",
      "en": "São Vicente",
      "fr": "São Vicente",
      "pt": "São Vicente"
    }
  }
}

LANG_META = {
  "de": {
    "folders": "orte",
    "home": "/de/home/",
    "lang_name": "de",
    "title_fmt": "Hausbetreuung in {loc} | Luxury Property Care Madeira",
    "desc_fmt": "Luxury Property Care in {loc} für hochwertige Immobilien auf Madeira mit strukturierter Betreuung, Kontrollen und Vorbereitung.",
    "h1_fmt": "Luxury Property Care für Luxusimmobilien in {loc}",
    "sections": {
      "overview": "Warum {loc} eine besondere Betreuung verlangt",
      "properties": "Welche Immobilien in {loc} besonders profitieren",
      "owners": "Nutzungsmuster internationaler Eigentümer",
      "risks": "Welche lokalen Risiken wirklich relevant sind",
      "service": "Wie unser Property Care in {loc} praktisch arbeitet",
      "arrival": "Vorbereitung, Koordination und Anreisebereitschaft",
      "value": "Warum diese Betreuung den Immobilienwert schützt"
    },
    "intro_lead": "{signature} {geo_sentence}"
  },
  "en": {
    "folders": "locations",
    "home": "/en/home/",
    "lang_name": "en",
    "title_fmt": "Luxury Property Care in {loc} | Madeira",
    "desc_fmt": "Luxury Property Care in {loc} for premium properties in Madeira with structured supervision, inspections and arrival preparation.",
    "h1_fmt": "Luxury Property Care for High-End Properties in {loc}",
    "sections": {
      "overview": "Why {loc} requires a distinct level of supervision",
      "properties": "Which properties in {loc} benefit most",
      "owners": "Usage patterns of international owners",
      "risks": "Which local risk factors truly matter",
      "service": "How our Property Care works in {loc} in practice",
      "arrival": "Preparation, coordination and readiness before arrival",
      "value": "Why this level of care protects long-term value"
    },
    "intro_lead": "{signature} {geo_sentence}"
  },
  "fr": {
    "folders": "lieux",
    "home": "/fr/home/",
    "lang_name": "fr",
    "title_fmt": "Property Care à {loc} | Immobilier haut de gamme à Madère",
    "desc_fmt": "Luxury Property Care à {loc} pour biens haut de gamme à Madère avec suivi structuré, contrôles et préparation avant arrivée.",
    "h1_fmt": "Luxury Property Care pour biens haut de gamme à {loc}",
    "sections": {
      "overview": "Pourquoi {loc} exige un suivi particulier",
      "properties": "Quels biens à {loc} en profitent le plus",
      "owners": "Modes d'usage des propriétaires internationaux",
      "risks": "Quels facteurs de risque locaux comptent vraiment",
      "service": "Comment notre Property Care fonctionne concrètement à {loc}",
      "arrival": "Préparation, coordination et disponibilité avant arrivée",
      "value": "Pourquoi ce niveau de suivi protège la valeur du bien"
    },
    "intro_lead": "{signature} {geo_sentence}"
  },
  "pt": {
    "folders": "locais",
    "home": "/pt/home/",
    "lang_name": "pt",
    "title_fmt": "Property Care em {loc} | Imóveis premium na Madeira",
    "desc_fmt": "Luxury Property Care em {loc} para imóveis premium na Madeira com acompanhamento estruturado, verificações e preparação.",
    "h1_fmt": "Luxury Property Care para imóveis premium em {loc}",
    "sections": {
      "overview": "Porque {loc} exige um acompanhamento próprio",
      "properties": "Que imóveis em {loc} beneficiam mais",
      "owners": "Padrões de utilização de proprietários internacionais",
      "risks": "Que fatores de risco locais realmente contam",
      "service": "Como o nosso Property Care funciona em {loc} na prática",
      "arrival": "Preparação, coordenação e prontidão antes da chegada",
      "value": "Porque este nível de cuidado protege o valor do imóvel"
    },
    "intro_lead": "{signature} {geo_sentence}"
  }
}

REGION_PHRASE = {
  "de": {
    "north_green": "an der grünen Nordküste",
    "sunny_southwest": "im sonnigen Südwesten",
    "cliffside_south": "an der spektakulären Südküste mit Steillagen",
    "central_south": "im gut angebundenen Süden der Insel",
    "east_south": "an der südöstlichen Küste",
    "mountain_valley": "im geschützten Bergtal des Inselinneren",
    "capital_city": "in der Hauptstadt Funchal",
    "west_seaside": "im kleinen Küstendorf an der Westseite",
    "sunny_far_west": "an der sonnigen Küste des weit entfernten Westens",
    "far_west_plateau": "auf dem exponierten Plateau im äußersten Westen",
    "sunny_south": "an der hellen und sonnigen Südküste",
    "northwest_coast": "an der dramatischen Nordwestküste",
    "airport_coast": "an der Küste nahe Flughafen und Schnellstraße",
    "north_forest": "im grünen Norden mit stärkerer Vegetation",
    "north_terraces": "an der terrassierten Nordküste",
    "north_valley": "im nördlichen Tal zwischen Bergen und Küste"
  },
  "en": {
    "north_green": "on Madeira's green north coast",
    "sunny_southwest": "in the sunny southwest",
    "cliffside_south": "on the dramatic south coast with cliffside addresses",
    "central_south": "in the well-connected south of the island",
    "east_south": "on the southeast coast",
    "mountain_valley": "in the protected mountain valley of the interior",
    "capital_city": "in the capital city of Funchal",
    "west_seaside": "in a small west-coast seaside village",
    "sunny_far_west": "on the sunlit coast of the far west",
    "far_west_plateau": "on the exposed plateau in the far west",
    "sunny_south": "on the bright, sunny south coast",
    "northwest_coast": "on the dramatic northwest coastline",
    "airport_coast": "on the coast near the airport and main road links",
    "north_forest": "in the greener north with stronger vegetation growth",
    "north_terraces": "on the terraced north coast",
    "north_valley": "in the northern valley between mountains and coastline"
  },
  "fr": {
    "north_green": "sur la côte nord verdoyante",
    "sunny_southwest": "dans le sud-ouest ensoleillé",
    "cliffside_south": "sur la côte sud spectaculaire aux implantations en pente",
    "central_south": "dans le sud bien connecté de l'île",
    "east_south": "sur la côte sud-est",
    "mountain_valley": "dans la vallée de montagne protégée de l'intérieur",
    "capital_city": "dans la capitale Funchal",
    "west_seaside": "dans un petit village côtier de l'ouest",
    "sunny_far_west": "sur la côte ensoleillée de l'extrême ouest",
    "far_west_plateau": "sur le plateau exposé tout à l'ouest",
    "sunny_south": "sur la côte sud lumineuse et ensoleillée",
    "northwest_coast": "sur la côte nord-ouest spectaculaire",
    "airport_coast": "sur la côte proche de l'aéroport et des voies rapides",
    "north_forest": "dans le nord plus vert avec une végétation plus active",
    "north_terraces": "sur la côte nord en terrasses",
    "north_valley": "dans la vallée du nord entre montagnes et littoral"
  },
  "pt": {
    "north_green": "na costa norte verdejante",
    "sunny_southwest": "no sudoeste soalheiro",
    "cliffside_south": "na costa sul dramática com moradias em encosta",
    "central_south": "no sul bem ligado da ilha",
    "east_south": "na costa sudeste",
    "mountain_valley": "no vale de montanha protegido do interior",
    "capital_city": "na capital Funchal",
    "west_seaside": "num pequeno povoado costeiro a oeste",
    "sunny_far_west": "na costa solarenga do extremo oeste",
    "far_west_plateau": "no planalto exposto do extremo oeste",
    "sunny_south": "na costa sul luminosa e soalheira",
    "northwest_coast": "na dramática costa noroeste",
    "airport_coast": "na costa próxima do aeroporto e das ligações rápidas",
    "north_forest": "no norte mais verde com vegetação mais intensa",
    "north_terraces": "na costa norte em socalcos",
    "north_valley": "no vale do norte entre montanhas e litoral"
  }
}

SETTING_PHRASE = {
  "de": {
    "rural_hillside": "ländlich und hangorientiert",
    "marina_hillside": "modern, marinanah und von Hangvillen geprägt",
    "urban_hillside": "städtisch angebunden und zugleich panoramisch",
    "quiet_hillside": "ruhig, wohnlich und von Einfamilienhäusern geprägt",
    "residential_coast": "wohnorientiert mit Villen, Apartments und Residenzen",
    "isolated_mountain": "abgelegen, bergig und wetterabhängig",
    "urban_premium": "urban, repräsentativ und logistisch anspruchsvoll",
    "village_cliff": "kleinteilig, charakterstark und küstennah",
    "surf_coast": "lässig im Auftreten, aber exponiert an der Küste",
    "remote_exposed": "weit, windoffen und stark auf Eigenorganisation angewiesen",
    "design_hillside": "architektonisch anspruchsvoll und bildstark",
    "lava_coast": "spektakulär, salzhaltig und vom Atlantik geprägt",
    "connected_valley": "zentral gelegen und schnell erreichbar",
    "connected_coast": "mobil, anreiseorientiert und flexibel genutzt",
    "rural_green": "traditionell, grün und grundstücksintensiv",
    "green_hillside": "grün, steil und gartenintensiv",
    "valley_village": "talgeprägt, feucht und landschaftlich stark"
  },
  "en": {
    "rural_hillside": "rural and hillside-oriented",
    "marina_hillside": "modern, marina-adjacent and shaped by hillside villas",
    "urban_hillside": "well connected yet panoramic",
    "quiet_hillside": "calm, residential and defined by family homes",
    "residential_coast": "residential in character with villas, apartments and compounds",
    "isolated_mountain": "remote, mountainous and weather-dependent",
    "urban_premium": "urban, representative and logistically demanding",
    "village_cliff": "small-scale, characterful and close to the sea",
    "surf_coast": "relaxed in image yet exposed on the coast",
    "remote_exposed": "open, wind-exposed and dependent on autonomous organisation",
    "design_hillside": "architecturally ambitious and visually driven",
    "lava_coast": "dramatic, salty and Atlantic-shaped",
    "connected_valley": "central and quickly accessible",
    "connected_coast": "mobile, arrival-oriented and flexibly used",
    "rural_green": "traditional, green and plot-intensive",
    "green_hillside": "green, steep and garden-intensive",
    "valley_village": "valley-based, humid and strongly landscape-driven"
  },
  "fr": {
    "rural_hillside": "rural et construit en pente",
    "marina_hillside": "moderne, proche de la marina et marqué par les villas en hauteur",
    "urban_hillside": "bien connecté tout en restant panoramique",
    "quiet_hillside": "paisible, résidentiel et dominé par les maisons familiales",
    "residential_coast": "résidentiel avec villas, appartements et résidences",
    "isolated_mountain": "isolé, montagneux et dépendant de la météo",
    "urban_premium": "urbain, représentatif et exigeant sur le plan logistique",
    "village_cliff": "à taille humaine, plein de caractère et proche de l'océan",
    "surf_coast": "décontracté en apparence mais exposé sur le littoral",
    "remote_exposed": "ouvert, exposé au vent et dépendant d'une organisation autonome",
    "design_hillside": "architecturalement ambitieux et très visuel",
    "lava_coast": "spectaculaire, salin et façonné par l'Atlantique",
    "connected_valley": "central et rapidement accessible",
    "connected_coast": "mobile, rythmé par les arrivées et utilisé de façon flexible",
    "rural_green": "traditionnel, verdoyant et lié à de grandes parcelles",
    "green_hillside": "vert, pentu et très lié aux jardins",
    "valley_village": "marqué par la vallée, l'humidité et le paysage"
  },
  "pt": {
    "rural_hillside": "rural e marcado pela encosta",
    "marina_hillside": "moderno, próximo da marina e dominado por villas em altitude",
    "urban_hillside": "bem ligado mas ainda panorâmico",
    "quiet_hillside": "tranquilo, residencial e marcado por moradias familiares",
    "residential_coast": "residencial com villas, apartamentos e conjuntos habitacionais",
    "isolated_mountain": "isolado, montanhoso e dependente do tempo",
    "urban_premium": "urbano, representativo e exigente em logística",
    "village_cliff": "de pequena escala, com carácter e perto do mar",
    "surf_coast": "descontraído na imagem mas exposto na costa",
    "remote_exposed": "aberto, exposto ao vento e dependente de organização autónoma",
    "design_hillside": "arquitetonicamente ambicioso e muito visual",
    "lava_coast": "espetacular, salino e moldado pelo Atlântico",
    "connected_valley": "central e de acesso rápido",
    "connected_coast": "móvel, orientado para chegadas e usado de forma flexível",
    "rural_green": "tradicional, verde e ligado a lotes maiores",
    "green_hillside": "verde, inclinado e muito ligado aos jardins",
    "valley_village": "marcado pelo vale, pela humidade e pela paisagem"
  }
}

MIX_PHRASE = {
  "de": {
    "stone_retreats": "renovierte Naturstein- und Rückzugshäuser",
    "sea_view_villas": "Villen mit weitem Meerblick",
    "garden_estates": "größere Grundstücke mit Gartenbereichen",
    "design_villas": "moderne Designvillen",
    "pool_homes": "Häuser mit Pool und Außendecks",
    "ocean_terraces": "Immobilien mit großen Meerblick-Terrassen",
    "cliff_villas": "Villen in spektakulären Hanglagen",
    "mixed_residences": "hochwertige gemischte Wohnimmobilien",
    "panoramic_homes": "panoramisch ausgerichtete Häuser",
    "family_villas": "familiengeeignete Villen",
    "terrace_homes": "Häuser mit nutzbaren Terrassenflächen",
    "garden_properties": "gartenorientierte Wohnimmobilien",
    "premium_apartments": "hochwertige Apartments",
    "residence_villas": "Villen in Residenzlagen",
    "sea_view_condos": "Wohnungen mit Meerblick und Gemeinschaftsstruktur",
    "mountain_houses": "Berg- und Rückzugshäuser",
    "retreat_properties": "stille Retreat-Immobilien",
    "heritage_homes": "traditionell geprägte Häuser mit Substanz",
    "city_apartments": "repräsentative Stadtapartments",
    "penthouses": "Penthouses mit Serviceanspruch",
    "hillside_villas": "Villen oberhalb der Stadt",
    "renovated_houses": "renovierte Küstenhäuser",
    "coastal_retreats": "kleinere Rückzugsimmobilien am Meer",
    "holiday_villas": "Ferienvillen",
    "oceanfront_homes": "Häuser in unmittelbarer Küstennähe",
    "estate_villas": "großzügige Villen mit Grundstück",
    "view_properties": "Immobilien mit freier Aussicht",
    "glass_homes": "glasbetonte Architekturhäuser",
    "stone_properties": "steinbetonte Bestandsimmobilien",
    "apartments": "Apartments",
    "family_residences": "Familienresidenzen",
    "traditional_houses": "traditionelle Wohnhäuser",
    "restored_houses": "restaurierte Bestandsobjekte",
    "terrace_properties": "Häuser mit nutzbaren Terrassenflächen",
    "large_plots": "große Grundstücke mit Weite und Abstand",
    "designer_villas": "moderne Designvillen",
    "holiday_homes": "Ferienhäuser in guter Aussichtslage",
    "view_villas": "Villen in aussichtsreicher Lage",
    "hillside_homes": "Häuser in Hanglage",
    "coastal_villas": "Küstenvillen",
    "estate_houses": "größere Land- und Wohnhäuser mit Grundstück"
  },
  "en": {
    "stone_retreats": "renovated stone retreat homes",
    "sea_view_villas": "villas with broad sea views",
    "garden_estates": "larger garden-based estates",
    "design_villas": "modern design villas",
    "pool_homes": "homes with pools and outdoor decks",
    "ocean_terraces": "properties with broad sea-facing terraces",
    "cliff_villas": "villas in dramatic hillside positions",
    "mixed_residences": "high-quality mixed residential properties",
    "panoramic_homes": "panoramic homes",
    "family_villas": "family-oriented villas",
    "terrace_homes": "homes with usable terrace areas",
    "garden_properties": "garden-oriented residences",
    "premium_apartments": "premium apartments",
    "residence_villas": "villas in residential compounds",
    "sea_view_condos": "sea-view apartments with shared structures",
    "mountain_houses": "mountain and retreat homes",
    "retreat_properties": "quiet retreat properties",
    "heritage_homes": "traditional homes with substance",
    "city_apartments": "representative city apartments",
    "penthouses": "penthouses with service expectations",
    "hillside_villas": "villas above the city",
    "renovated_houses": "renovated coastal houses",
    "coastal_retreats": "smaller sea-oriented retreat properties",
    "holiday_villas": "holiday villas",
    "oceanfront_homes": "homes very close to the ocean",
    "estate_villas": "larger villas on sizeable plots",
    "view_properties": "properties with open views",
    "glass_homes": "glass-led architectural homes",
    "stone_properties": "stone-based existing properties",
    "apartments": "apartments",
    "family_residences": "family residences",
    "traditional_houses": "traditional homes",
    "restored_houses": "restored existing houses",
    "terrace_properties": "homes with usable terrace areas",
    "large_plots": "large plots with space and separation",
    "designer_villas": "modern design villas",
    "holiday_homes": "holiday homes in strong view positions",
    "view_villas": "villas in strong view positions",
    "hillside_homes": "hillside homes",
    "coastal_villas": "coastal villas",
    "estate_houses": "larger residential houses on substantial plots"
  },
  "fr": {
    "stone_retreats": "maisons de retraite en pierre rénovées",
    "sea_view_villas": "villas avec larges vues mer",
    "garden_estates": "propriétés plus vastes avec jardins",
    "design_villas": "villas de design contemporain",
    "pool_homes": "maisons avec piscine et terrasses extérieures",
    "ocean_terraces": "biens dotés de grandes terrasses ouvertes sur l'océan",
    "cliff_villas": "villas situées dans des positions spectaculaires en pente",
    "mixed_residences": "biens résidentiels haut de gamme de typologie mixte",
    "panoramic_homes": "maisons à forte orientation panoramique",
    "family_villas": "villas adaptées à la vie familiale",
    "terrace_homes": "maisons avec véritables surfaces de terrasse utilisables",
    "garden_properties": "résidences orientées vers les jardins",
    "premium_apartments": "appartements haut de gamme",
    "residence_villas": "villas au sein d'environnements résidentiels",
    "sea_view_condos": "appartements vue mer avec structures communes",
    "mountain_houses": "maisons de montagne et de retraite",
    "retreat_properties": "propriétés calmes de type refuge",
    "heritage_homes": "maisons traditionnelles avec valeur de bâti",
    "city_apartments": "appartements urbains représentatifs",
    "penthouses": "penthouses avec fortes attentes de service",
    "hillside_villas": "villas situées au-dessus de la ville",
    "renovated_houses": "maisons côtières rénovées",
    "coastal_retreats": "petits biens de retraite tournés vers l'océan",
    "holiday_villas": "villas de vacances",
    "oceanfront_homes": "maisons au contact direct du littoral",
    "estate_villas": "villas généreuses sur de grandes parcelles",
    "view_properties": "biens avec vues dégagées",
    "glass_homes": "maisons d'architecture dominée par le verre",
    "stone_properties": "biens existants à forte composante minérale",
    "apartments": "appartements",
    "family_residences": "résidences familiales",
    "traditional_houses": "maisons traditionnelles",
    "restored_houses": "maisons restaurées",
    "terrace_properties": "maisons avec véritables surfaces de terrasse utilisables",
    "large_plots": "grandes parcelles avec espace et distance",
    "designer_villas": "villas de design contemporain",
    "holiday_homes": "maisons de vacances bénéficiant de belles vues",
    "view_villas": "villas en position dominante avec belle vue",
    "hillside_homes": "maisons en pente",
    "coastal_villas": "villas côtières",
    "estate_houses": "maisons résidentielles plus vastes sur parcelles importantes"
  },
  "pt": {
    "stone_retreats": "casas de refúgio em pedra renovadas",
    "sea_view_villas": "villas com ampla vista mar",
    "garden_estates": "propriedades maiores com jardins",
    "design_villas": "villas de design contemporâneo",
    "pool_homes": "casas com piscina e decks exteriores",
    "ocean_terraces": "imóveis com grandes terraços voltados para o mar",
    "cliff_villas": "villas em posições dramáticas de encosta",
    "mixed_residences": "imóveis residenciais premium de tipologia mista",
    "panoramic_homes": "casas de forte orientação panorâmica",
    "family_villas": "villas adequadas a famílias",
    "terrace_homes": "casas com áreas de terraço realmente utilizáveis",
    "garden_properties": "residências orientadas para jardins",
    "premium_apartments": "apartamentos premium",
    "residence_villas": "villas em contextos residenciais",
    "sea_view_condos": "apartamentos com vista mar e estruturas comuns",
    "mountain_houses": "casas de montanha e refúgio",
    "retreat_properties": "propriedades tranquilas de retiro",
    "heritage_homes": "casas tradicionais com substância construtiva",
    "city_apartments": "apartamentos urbanos representativos",
    "penthouses": "penthouses com elevadas expectativas de serviço",
    "hillside_villas": "villas acima da cidade",
    "renovated_houses": "casas costeiras renovadas",
    "coastal_retreats": "pequenas propriedades de retiro junto ao mar",
    "holiday_villas": "villas de férias",
    "oceanfront_homes": "casas muito próximas do oceano",
    "estate_villas": "villas amplas em lotes generosos",
    "view_properties": "imóveis com vistas abertas",
    "glass_homes": "casas de arquitetura dominada pelo vidro",
    "stone_properties": "imóveis existentes com forte componente mineral",
    "apartments": "apartamentos",
    "family_residences": "residências familiares",
    "traditional_houses": "casas tradicionais",
    "restored_houses": "casas restauradas",
    "terrace_properties": "casas com áreas de terraço realmente utilizáveis",
    "large_plots": "grandes lotes com espaço e separação",
    "designer_villas": "villas de design contemporâneo",
    "holiday_homes": "casas de férias com boas posições de vista",
    "view_villas": "villas em posições com vista privilegiada",
    "hillside_homes": "casas em encosta",
    "coastal_villas": "villas costeiras",
    "estate_houses": "casas residenciais maiores em lotes amplos"
  }
}

OWNER_PHRASE = {
  "de": {
    "second_home": "klassische Zweitwohnsitze",
    "long_stay_retreat": "Rückzugsorte für längere Aufenthalte",
    "international_family": "Immobilien für internationale Familiennutzung",
    "frequent_short_stays": "Häuser mit häufigeren, kürzeren Aufenthalten",
    "residential_with_absence": "Haupt- oder Teilzeitwohnsitze mit Abwesenheitsphasen",
    "work_travel": "Objekte von Eigentümern mit beruflich bedingten Reisen",
    "retreat_use": "bewusst ruhige Rückzugsimmobilien",
    "seasonal_use": "saisonal genutzte Häuser",
    "creative_remote": "Standorte für flexible Remote-Nutzung",
    "short_rental_with_private_use": "Modelle mit Gästebelegung und privater Eigennutzung",
    "privacy_first": "Nutzung mit starkem Fokus auf Ruhe und Privatsphäre",
    "frequent_arrivals": "Objekte mit spontanen oder häufigen Anreisen"
  },
  "en": {
    "second_home": "classic second homes",
    "long_stay_retreat": "retreats for longer stays",
    "international_family": "homes used by international families",
    "frequent_short_stays": "properties with more frequent, shorter stays",
    "residential_with_absence": "main or part-time residences with absence periods",
    "work_travel": "homes owned by people who travel for work",
    "retreat_use": "deliberately quiet retreat properties",
    "seasonal_use": "seasonally used homes",
    "creative_remote": "bases for flexible remote living",
    "short_rental_with_private_use": "models that combine guest stays with private use",
    "privacy_first": "use patterns centred on silence and privacy",
    "frequent_arrivals": "properties with spontaneous or frequent arrivals"
  },
  "fr": {
    "second_home": "résidences secondaires classiques",
    "long_stay_retreat": "refuges pour des séjours prolongés",
    "international_family": "biens utilisés par des familles internationales",
    "frequent_short_stays": "biens avec des séjours plus fréquents mais plus courts",
    "residential_with_absence": "résidences principales ou partielles avec périodes d'absence",
    "work_travel": "biens de propriétaires qui voyagent pour le travail",
    "retreat_use": "propriétés de retraite volontairement calmes",
    "seasonal_use": "maisons utilisées de manière saisonnière",
    "creative_remote": "bases pour un mode de vie flexible à distance",
    "short_rental_with_private_use": "modèles combinant séjours invités et usage privé",
    "privacy_first": "usage centré sur le calme et la discrétion",
    "frequent_arrivals": "biens avec arrivées spontanées ou fréquentes"
  },
  "pt": {
    "second_home": "segundas residências clássicas",
    "long_stay_retreat": "refúgios para estadias prolongadas",
    "international_family": "imóveis usados por famílias internacionais",
    "frequent_short_stays": "imóveis com estadias mais frequentes e mais curtas",
    "residential_with_absence": "residências principais ou parciais com períodos de ausência",
    "work_travel": "imóveis de proprietários que viajam por trabalho",
    "retreat_use": "propriedades de refúgio deliberadamente tranquilas",
    "seasonal_use": "casas usadas de forma sazonal",
    "creative_remote": "bases para um modo de vida remoto flexível",
    "short_rental_with_private_use": "modelos que combinam estadias de hóspedes e uso privado",
    "privacy_first": "utilizações centradas em silêncio e privacidade",
    "frequent_arrivals": "imóveis com chegadas espontâneas ou frequentes"
  }
}

PRESSURE_PHRASE = {
  "de": {
    "humidity": "dauerhafte Feuchtebelastung",
    "growth": "schnelles Pflanzenwachstum",
    "drainage": "empfindliche Entwässerungspunkte",
    "sun_uv": "starke Sonne und UV-Belastung",
    "salt_air": "salzhaltige Atlantikluft",
    "pool_areas": "pflegeintensive Pool- und Terrassenzonen",
    "traffic_access": "sensible Zufahrts- und Logistikthemen",
    "retaining_walls": "Mauern, Hangsicherungen und Außenkanten",
    "wind_exposure": "stärkere Windbelastung",
    "exterior_wear": "Abnutzung an Außenflächen",
    "shared_access": "Gemeinschafts- und Zugangsbereiche",
    "balcony_exposure": "exponierte Balkone und Geländer",
    "weather_swings": "rasche Wetterwechsel",
    "access_challenges": "erschwerte Zufahrt oder längere Wege",
    "city_logistics": "urbane Koordination und Terminpräzision",
    "presentation_standard": "ein besonders hoher Anspruch an optische Perfektion",
    "technical_systems": "technische Systeme mit hohem Komfortanspruch",
    "narrow_access": "enge Wege und eingeschränkte Zufahrt",
    "fast_turnover": "schnelle Wechsel zwischen Nutzungsphasen",
    "distance": "große Distanz zu spontanen Lösungen",
    "glass_exposure": "sichtbare Spuren auf Glasflächen",
    "arrival_cycles": "häufige An- und Abreisezyklen",
    "roof_wear": "Belastung von Dächern und wasserführenden Elementen",
    "steep_access": "steile Zugänge und Stufenanlagen",
    "garden_growth": "schnelles Pflanzenwachstum"
  },
  "en": {
    "humidity": "constant humidity pressure",
    "growth": "fast vegetation growth",
    "drainage": "sensitive drainage points",
    "sun_uv": "strong sun and UV exposure",
    "salt_air": "salty Atlantic air",
    "pool_areas": "maintenance-heavy pool and terrace zones",
    "traffic_access": "sensitive access and logistics themes",
    "retaining_walls": "retaining walls, edges and slope structures",
    "wind_exposure": "higher wind exposure",
    "exterior_wear": "wear on exterior surfaces",
    "shared_access": "shared entrances and access points",
    "balcony_exposure": "exposed balconies and railings",
    "weather_swings": "rapid weather shifts",
    "access_challenges": "difficult access or longer approach routes",
    "city_logistics": "urban coordination and timing precision",
    "presentation_standard": "a particularly high demand for visual perfection",
    "technical_systems": "technical systems with high comfort expectations",
    "narrow_access": "narrow lanes and limited access",
    "fast_turnover": "quick changes between occupancy phases",
    "distance": "greater distance from spontaneous solutions",
    "glass_exposure": "visible marks on glass surfaces",
    "arrival_cycles": "frequent arrival and departure cycles",
    "roof_wear": "stress on roofs and water-carrying elements",
    "steep_access": "steep approaches and stair sections",
    "garden_growth": "fast vegetation growth"
  },
  "fr": {
    "humidity": "pression d'humidité durable",
    "growth": "croissance rapide de la végétation",
    "drainage": "points de drainage sensibles",
    "sun_uv": "soleil fort et exposition UV",
    "salt_air": "air atlantique chargé en sel",
    "pool_areas": "zones de piscine et de terrasse exigeantes en entretien",
    "traffic_access": "questions sensibles d'accès et de logistique",
    "retaining_walls": "murs de soutènement, arêtes et structures de pente",
    "wind_exposure": "exposition plus forte au vent",
    "exterior_wear": "usure des surfaces extérieures",
    "shared_access": "entrées et accès partagés",
    "balcony_exposure": "balcons et garde-corps exposés",
    "weather_swings": "changements rapides de météo",
    "access_challenges": "accès plus difficile ou trajets plus longs",
    "city_logistics": "coordination urbaine et précision des horaires",
    "presentation_standard": "niveau d'exigence très élevé sur l'apparence",
    "technical_systems": "systèmes techniques avec fortes attentes de confort",
    "narrow_access": "ruelles étroites et accès limités",
    "fast_turnover": "changements rapides entre phases d'occupation",
    "distance": "plus grande distance face aux solutions de dernière minute",
    "glass_exposure": "traces visibles sur les surfaces vitrées",
    "arrival_cycles": "cycles fréquents d'arrivée et de départ",
    "roof_wear": "contraintes sur les toitures et les éléments d'évacuation d'eau",
    "steep_access": "accès pentus et escaliers extérieurs",
    "garden_growth": "croissance rapide de la végétation"
  },
  "pt": {
    "humidity": "pressão constante de humidade",
    "growth": "crescimento rápido da vegetação",
    "drainage": "pontos sensíveis de drenagem",
    "sun_uv": "sol forte e exposição UV",
    "salt_air": "ar atlântico salgado",
    "pool_areas": "zonas de piscina e terraço exigentes em manutenção",
    "traffic_access": "questões sensíveis de acesso e logística",
    "retaining_walls": "muros de suporte, arestas e estruturas de encosta",
    "wind_exposure": "maior exposição ao vento",
    "exterior_wear": "desgaste de superfícies exteriores",
    "shared_access": "entradas e acessos partilhados",
    "balcony_exposure": "varandas e guardas expostas",
    "weather_swings": "mudanças rápidas de tempo",
    "access_challenges": "acesso mais difícil ou percursos mais longos",
    "city_logistics": "coordenação urbana e precisão de horários",
    "presentation_standard": "um nível especialmente alto de exigência visual",
    "technical_systems": "sistemas técnicos com elevadas expectativas de conforto",
    "narrow_access": "ruas estreitas e acesso limitado",
    "fast_turnover": "mudanças rápidas entre fases de ocupação",
    "distance": "maior distância de soluções improvisadas",
    "glass_exposure": "marcas visíveis em superfícies de vidro",
    "arrival_cycles": "ciclos frequentes de chegada e partida",
    "roof_wear": "pressão sobre coberturas e elementos de escoamento",
    "steep_access": "acessos inclinados e zonas de escadas",
    "garden_growth": "crescimento rápido da vegetação"
  }
}

OPS_PHRASE = {
  "de": {
    "garden_control": "kontrollierte Pflege von Gärten und Außenbereichen",
    "hillside_checks": "systematische Sichtkontrollen an Hanglagen, Stufen und Mauern",
    "arrival_readiness": "eine verlässliche Vorbereitung vor jeder Eigentümerankunft",
    "pool_garden_standard": "ein repräsentativer Standard bei Pool, Terrasse und Garten",
    "vendor_coordination": "koordinierte Einbindung von Handwerkern und Dienstleistern",
    "access_logistics": "saubere Steuerung von Zufahrt, Zugang und Terminfenstern",
    "presentation_standard": "sichtbar hoher Präsentations- und Sauberkeitsstandard",
    "technical_checks": "regelmäßige Kontrolle technischer Basisfunktionen",
    "routine_checks": "klar getaktete Objektkontrollen im festen Rhythmus",
    "building_coordination": "Abstimmung mit Gebäudestrukturen, Residenzen oder Hauszugängen",
    "weather_readiness": "vorausschauendes Handeln vor und nach Wetterphasen",
    "drainage_checks": "Kontrolle von Abläufen, Wasserwegen und sensiblen Außenpunkten",
    "remote_coordination": "selbständige Organisation auch bei größerer Distanz",
    "exterior_checks": "gezielte Kontrolle von Fassaden, Geländern und Außenkanten"
  },
  "en": {
    "garden_control": "controlled care of gardens and outdoor areas",
    "hillside_checks": "systematic visual checks on slopes, steps and retaining walls",
    "arrival_readiness": "reliable preparation before every owner arrival",
    "pool_garden_standard": "a representative standard around pool, terrace and garden",
    "vendor_coordination": "coordinated involvement of tradespeople and service partners",
    "access_logistics": "clean handling of access, entry and time windows",
    "presentation_standard": "a visibly high standard of presentation and cleanliness",
    "technical_checks": "regular checks of technical basics",
    "routine_checks": "clearly timed inspections on a fixed rhythm",
    "building_coordination": "alignment with building structures, residences or shared entries",
    "weather_readiness": "forward-looking action before and after weather phases",
    "drainage_checks": "checks of drains, water paths and sensitive exterior points",
    "remote_coordination": "autonomous organisation even across greater distance",
    "exterior_checks": "targeted checks of façades, railings and exterior edges"
  },
  "fr": {
    "garden_control": "entretien maîtrisé des jardins et extérieurs",
    "hillside_checks": "contrôles visuels systématiques sur les pentes, marches et murs",
    "arrival_readiness": "préparation fiable avant chaque arrivée des propriétaires",
    "pool_garden_standard": "standard représentatif autour de la piscine, de la terrasse et du jardin",
    "vendor_coordination": "coordination structurée des artisans et prestataires",
    "access_logistics": "gestion propre des accès, entrées et créneaux",
    "presentation_standard": "niveau visiblement élevé de présentation et de propreté",
    "technical_checks": "contrôles réguliers des fonctions techniques de base",
    "routine_checks": "contrôles clairement planifiés selon un rythme fixe",
    "building_coordination": "coordination avec les structures de résidence et les accès partagés",
    "weather_readiness": "action anticipative avant et après les phases météo",
    "drainage_checks": "contrôle des évacuations, parcours d'eau et points extérieurs sensibles",
    "remote_coordination": "organisation autonome même à plus grande distance",
    "exterior_checks": "contrôles ciblés des façades, garde-corps et arêtes extérieures"
  },
  "pt": {
    "garden_control": "cuidado controlado de jardins e exteriores",
    "hillside_checks": "verificações visuais sistemáticas em encostas, escadas e muros",
    "arrival_readiness": "preparação fiável antes de cada chegada dos proprietários",
    "pool_garden_standard": "um padrão representativo em piscina, terraço e jardim",
    "vendor_coordination": "coordenação estruturada de técnicos e parceiros",
    "access_logistics": "gestão limpa de acessos, entradas e janelas horárias",
    "presentation_standard": "um nível visivelmente elevado de apresentação e limpeza",
    "technical_checks": "verificações regulares das funções técnicas básicas",
    "routine_checks": "verificações claramente planeadas em ritmo fixo",
    "building_coordination": "coordenação com estruturas residenciais e acessos comuns",
    "weather_readiness": "ação preventiva antes e depois de fases meteorológicas",
    "drainage_checks": "verificação de ralos, percursos de água e pontos exteriores sensíveis",
    "remote_coordination": "organização autónoma mesmo a maior distância",
    "exterior_checks": "verificações direcionadas de fachadas, guardas e arestas exteriores"
  }
}

VENDOR_PHRASE = {
  "de": {
    "remote_coordination": "Spontane Lösungen sind hier seltener, deshalb muss die Betreuung eigenständig organisieren, priorisieren und sauber dokumentieren.",
    "premium_trades": "Hochwertige Architektur und sichtbare Außenbereiche verlangen gut koordinierte Fachpartner, damit das Ergebnis dem Niveau der Immobilie entspricht.",
    "urban_coordination": "Die Nähe zu Funchal verbessert Verfügbarkeit, erhöht aber zugleich den Anspruch an Geschwindigkeit, Terminpräzision und diskrete Abwicklung.",
    "central_coordination": "Die gute Erreichbarkeit hilft im Alltag, trotzdem braucht eine hochwertige Immobilie klare Zuständigkeiten statt improvisierter Einzelmaßnahmen.",
    "residential_coordination": "In Residenzlagen muss Betreuung nicht nur die Wohnung selbst, sondern auch Zugänge, Aufzüge, Eingangsbereiche und Hausregeln mitdenken.",
    "limited_access": "Wetter, Höhenlage und längere Wege machen eine gute Vorausplanung besonders wichtig, weil Ausweichlösungen nicht jederzeit verfügbar sind.",
    "city_speed": "In der Hauptstadt zählt neben Qualität auch Tempo: Eigentümer erwarten kurze Reaktionswege, klare Kommunikation und einen perfekten Zustand ohne Reibungsverluste.",
    "narrow_lane_coordination": "Enge Wege, kleine Zufahrten und die besondere Dorfstruktur verlangen ruhige Planung statt hektischer Nachbesserung am Anreisetag.",
    "coastal_coordination": "Küstennähe und Nutzung als Ferienimmobilie erhöhen die Erwartung an einen schnellen, repräsentativen Wechsel zwischen unbewohnt, vorbereitet und bewohnt.",
    "airport_corridor": "Die Nähe zum Flughafen erhöht die Zahl kurzfristiger Anreisen, wodurch Zeitfenster, Schlüsselmanagement und sofortige Nutzbarkeit besonders wichtig werden.",
    "rural_coordination": "In grüneren, ländlicheren Regionen schützt gute Koordination vor unnötigen Anfahrten, Verzögerungen und sichtbaren Pflegebrüchen."
  },
  "en": {
    "remote_coordination": "Spontaneous fixes are less realistic here, so supervision has to organise, prioritise and document matters independently.",
    "premium_trades": "High-end architecture and visible exterior zones require well-coordinated specialist partners so that results match the level of the property.",
    "urban_coordination": "Proximity to Funchal improves availability but also raises expectations regarding speed, timing precision and discreet execution.",
    "central_coordination": "Good accessibility helps in daily operations, yet a premium property still needs clear responsibilities instead of improvised one-off actions.",
    "residential_coordination": "In residence-style settings, supervision must consider not only the apartment itself but also entries, lifts, common approaches and house rules.",
    "limited_access": "Weather, altitude and longer routes make forward planning especially important because alternatives are not always instantly available.",
    "city_speed": "In the capital, quality alone is not enough; owners also expect fast reaction times, clear communication and a frictionless result.",
    "narrow_lane_coordination": "Narrow lanes, smaller access points and the specific village fabric call for calm planning instead of hectic last-minute correction.",
    "coastal_coordination": "Coastal proximity and holiday-home usage increase expectations regarding a quick and representative shift between vacant, prepared and occupied.",
    "airport_corridor": "Airport proximity increases the frequency of short-notice arrivals, making time windows, key handling and immediate usability especially important.",
    "rural_coordination": "In greener and more rural regions, good coordination prevents unnecessary journeys, delays and visible gaps in upkeep."
  },
  "fr": {
    "remote_coordination": "Les solutions de dernière minute sont moins réalistes ici; le suivi doit donc organiser, prioriser et documenter de manière autonome.",
    "premium_trades": "L'architecture haut de gamme et les extérieurs très visibles exigent des partenaires spécialisés bien coordonnés afin que le résultat corresponde au niveau du bien.",
    "urban_coordination": "La proximité de Funchal améliore la disponibilité, mais renforce aussi les attentes en matière de rapidité, de précision et de discrétion.",
    "central_coordination": "La bonne accessibilité aide au quotidien, mais un bien premium a tout de même besoin de responsabilités claires plutôt que d'actions isolées improvisées.",
    "residential_coordination": "Dans les résidences, le suivi doit intégrer non seulement le logement lui-même, mais aussi les entrées, ascenseurs, accès communs et règles de l'immeuble.",
    "limited_access": "La météo, l'altitude et les trajets plus longs rendent l'anticipation particulièrement importante, car les alternatives ne sont pas toujours immédiatement disponibles.",
    "city_speed": "Dans la capitale, la qualité ne suffit pas; les propriétaires attendent aussi des réactions rapides, une communication claire et un résultat sans friction.",
    "narrow_lane_coordination": "Les ruelles étroites, les accès réduits et la structure spécifique du village exigent une planification calme plutôt qu'une correction agitée le jour d'arrivée.",
    "coastal_coordination": "La proximité de l'océan et l'usage comme résidence de vacances renforcent l'attente d'une transition rapide et représentative entre vacant, préparé et occupé.",
    "airport_corridor": "La proximité de l'aéroport augmente les arrivées à court terme, ce qui rend les créneaux, la gestion des clés et l'usage immédiat particulièrement importants.",
    "rural_coordination": "Dans les zones plus vertes et rurales, une bonne coordination évite les trajets inutiles, les retards et les ruptures visibles dans l'entretien."
  },
  "pt": {
    "remote_coordination": "As soluções de última hora são menos realistas aqui, por isso o acompanhamento tem de organizar, priorizar e documentar de forma autónoma.",
    "premium_trades": "Arquitetura premium e exteriores muito visíveis exigem parceiros especializados bem coordenados para que o resultado corresponda ao nível do imóvel.",
    "urban_coordination": "A proximidade ao Funchal melhora a disponibilidade, mas também aumenta a exigência quanto a rapidez, precisão e execução discreta.",
    "central_coordination": "A boa acessibilidade ajuda no dia a dia, mas um imóvel premium continua a precisar de responsabilidades claras em vez de ações improvisadas isoladas.",
    "residential_coordination": "Em contextos residenciais, o acompanhamento deve considerar não só o apartamento em si, mas também entradas, elevadores, acessos comuns e regras do edifício.",
    "limited_access": "Tempo, altitude e percursos mais longos tornam o planeamento antecipado especialmente importante, porque as alternativas nem sempre estão imediatamente disponíveis.",
    "city_speed": "Na capital, qualidade por si só não basta; os proprietários também esperam rapidez de reação, comunicação clara e um resultado sem fricção.",
    "narrow_lane_coordination": "Ruas estreitas, acessos reduzidos e a estrutura específica do povoado exigem planeamento calmo em vez de correções apressadas no dia da chegada.",
    "coastal_coordination": "A proximidade ao oceano e o uso como casa de férias aumentam a expectativa de uma transição rápida e representativa entre vazio, preparado e ocupado.",
    "airport_corridor": "A proximidade ao aeroporto aumenta as chegadas de curto prazo, tornando janelas horárias, gestão de chaves e utilização imediata especialmente importantes.",
    "rural_coordination": "Nas regiões mais verdes e rurais, uma boa coordenação evita deslocações desnecessárias, atrasos e falhas visíveis na manutenção."
  }
}

MICRO_NOTE = {
  "boaventura": {
    "de": "Boaventura verlangt vor allem Aufmerksamkeit für Übergänge zwischen Natur und Gebäude. Wo Gärten, Hangwasser, Mauern und Wege direkt an das Haus anschließen, entscheidet nicht ein einzelner Einsatz, sondern die konsequente Beobachtung vieler kleiner Punkte über den langfristig gepflegten Zustand. Gerade abgelegene Rückzugsimmobilien brauchen hier sichtbar mehr Vorausdenken.",
    "en": "Boaventura above all requires attention to the transitions between landscape and building. Where gardens, slope water, walls and paths connect directly to the house, long-term condition depends less on one large intervention than on the consistent observation of many small points.",
    "fr": "Boaventura demande surtout une attention aux zones de transition entre nature et bâtiment. Là où jardins, eau de ruissellement, murs et chemins se raccordent directement à la maison, l'état durable dépend moins d'une grande intervention que de l'observation régulière de nombreux petits détails.",
    "pt": "Boaventura exige sobretudo atenção às zonas de transição entre natureza e edifício. Onde jardins, água de encosta, muros e caminhos tocam diretamente a casa, o estado duradouro depende menos de uma grande intervenção e mais da observação constante de muitos pequenos pontos."
  },
  "calheta": {
    "de": "In Calheta spielen klare Linien, Poolbereiche und sonnenexponierte Außenflächen eine besonders große Rolle. Eigentümer erwarten hier oft, dass die Immobilie schon beim ersten Blick den Anspruch moderner Architektur erfüllt und nicht erst nachgebessert werden muss.",
    "en": "In Calheta, clean lines, pool areas and sun-exposed exterior spaces play an especially strong role. Owners often expect the property to express the standard of modern architecture at first glance rather than needing correction after arrival.",
    "fr": "À Calheta, les lignes claires, les zones de piscine et les extérieurs exposés au soleil jouent un rôle particulièrement important. Les propriétaires attendent souvent que le bien reflète immédiatement le niveau d'une architecture contemporaine, sans devoir être corrigé après l'arrivée.",
    "pt": "Na Calheta, linhas limpas, zonas de piscina e exteriores expostos ao sol têm um papel especialmente forte. Os proprietários esperam muitas vezes que o imóvel revele logo à primeira vista o padrão de uma arquitetura moderna, sem precisar de correções após a chegada."
  },
  "camara-de-lobos": {
    "de": "Câmara de Lobos kombiniert Panorama mit Nähe zu urbanen Abläufen. Dadurch muss Betreuung nicht nur den Zustand des Hauses sichern, sondern auch Termine, Zufahrten und Dienstleister so steuern, dass die Immobilie trotz lebendigem Umfeld ruhig und hochwertig wirkt.",
    "en": "Câmara de Lobos combines panorama with proximity to urban routines. Supervision therefore has to protect not only the condition of the house but also the way appointments, access and service partners are managed so the property still feels calm and premium.",
    "fr": "Câmara de Lobos combine panorama et proximité de rythmes urbains. Le suivi doit donc protéger non seulement l'état de la maison, mais aussi la manière dont rendez-vous, accès et prestataires sont pilotés, afin que le bien reste calme et haut de gamme malgré un environnement plus vivant.",
    "pt": "Câmara de Lobos combina panorama com proximidade de rotinas urbanas. O acompanhamento tem por isso de proteger não só o estado da casa, mas também a forma como horários, acessos e parceiros são geridos, para que o imóvel continue a transmitir calma e nível premium."
  },
  "campanario": {
    "de": "Campanário braucht selten spektakuläre Eingriffe, dafür aber Konstanz. Gerade in ruhigen Wohnlagen fällt jede kleine Vernachlässigung stärker auf, weil das Gesamtbild einer gepflegten privaten Residenz von Details in Garten, Zugang und Außenwirkung lebt.",
    "en": "Campanário rarely needs dramatic intervention, but it does need consistency. In calm residential settings, every small sign of neglect stands out more because the overall impression of a well-kept private residence depends on details in garden, access and exterior presentation.",
    "fr": "Campanário a rarement besoin d'interventions spectaculaires, mais il a besoin de constance. Dans ces environnements résidentiels calmes, chaque petit signe de négligence se voit davantage, car l'image d'une résidence privée soignée dépend des détails dans le jardin, l'accès et les extérieurs.",
    "pt": "Campanário raramente precisa de intervenções espetaculares, mas precisa de constância. Em contextos residenciais tranquilos, qualquer pequeno sinal de negligência sobressai mais, porque a imagem de uma residência privada cuidada depende dos detalhes no jardim, no acesso e nos exteriores."
  },
  "canico": {
    "de": "In Caniço ist die Schnittstelle zwischen privater Einheit und gemeinsamer Infrastruktur oft entscheidend. Wer hier hochwertige Apartments oder Residenzen betreut, muss auch Aufzug, Eingangsbereich, Stellplätze oder Gemeinschaftszugänge als Teil des Qualitätsbildes mitdenken.",
    "en": "In Caniço, the interface between the private unit and the shared infrastructure is often decisive. Anyone caring for premium apartments or residences here has to think of lifts, entrances, parking and shared approaches as part of the quality experience.",
    "fr": "À Caniço, l'interface entre l'unité privée et l'infrastructure commune est souvent déterminante. Gérer des appartements ou résidences haut de gamme signifie aussi intégrer ascenseurs, halls d'entrée, stationnements et accès communs dans l'expérience de qualité.",
    "pt": "No Caniço, a interface entre a unidade privada e a infraestrutura comum é muitas vezes decisiva. Cuidar de apartamentos ou residências premium implica também considerar elevadores, entradas, estacionamento e acessos partilhados como parte da experiência de qualidade."
  },
  "curral-das-freiras": {
    "de": "Curral das Freiras ist stark von Topografie und Wetter geprägt. Deshalb zählt hier weniger ein repräsentativer Küstenauftritt als die verlässliche Kontrolle eines Hauses, das in einer abgelegenen Berglage auch nach wechselhaften Tagen sicher, trocken und geordnet bleiben soll.",
    "en": "Curral das Freiras is shaped above all by topography and weather. Here the priority is less a polished coastal presentation and more the reliable control of a house that must remain safe, dry and orderly in a remote mountain environment even after unsettled days.",
    "fr": "Curral das Freiras est avant tout marqué par la topographie et la météo. Ici, l'enjeu n'est pas tant une présentation côtière très mise en scène qu'un contrôle fiable d'une maison qui doit rester sûre, sèche et ordonnée dans un environnement montagneux isolé, même après des journées changeantes.",
    "pt": "Curral das Freiras é marcado sobretudo pela topografia e pelo tempo. Aqui, a prioridade é menos uma apresentação costeira muito polida e mais o controlo fiável de uma casa que tem de permanecer segura, seca e organizada num ambiente montanhoso remoto, mesmo após dias instáveis."
  },
  "funchal": {
    "de": "Funchal verlangt häufig einen Service, der fast hotelartig präzise wirkt, ohne seine private Qualität zu verlieren. Gerade bei Stadtapartments, Penthouses und Villen mit häufigeren Anreisen zählt jeder Ablauf von Zugang bis Vorbereitung deutlich stärker auf den ersten Eindruck ein.",
    "en": "Funchal often calls for a service style that feels almost hotel-precise without losing its private character. In city apartments, penthouses and villas with more frequent arrivals, every process from access to preparation has a stronger impact on first impression.",
    "fr": "Funchal demande souvent un service presque aussi précis qu'à l'hôtel, sans perdre son caractère privé. Dans les appartements urbains, penthouses et villas avec arrivées fréquentes, chaque processus, de l'accès à la préparation, influence fortement la première impression.",
    "pt": "O Funchal pede muitas vezes um serviço quase tão preciso como o de um hotel, sem perder o seu caráter privado. Em apartamentos urbanos, penthouses e villas com chegadas frequentes, cada processo, do acesso à preparação, influencia fortemente a primeira impressão."
  },
  "jardim-do-mar": {
    "de": "Jardim do Mar lebt von Charme, Ruhe und Küstencharakter statt von großen Gesten. Genau deshalb müssen Materialien, Möblierung und Außenwirkung stimmig bleiben, denn in dieser dichten Dorfstruktur wirkt Unordnung sofort sichtbarer und zerstört das gewünschte Gefühl von Rückzug.",
    "en": "Jardim do Mar lives from charm, silence and coastal character rather than from grand gestures. That is exactly why materials, furnishing and exterior presentation have to remain coherent, because in this dense village fabric disorder becomes visible immediately and undermines the feeling of retreat.",
    "fr": "Jardim do Mar vit du charme, du calme et d'un caractère côtier plutôt que de grands effets. C'est précisément pour cela que matériaux, mobilier et présentation extérieure doivent rester cohérents, car dans cette trame de village dense, le désordre devient immédiatement visible et détruit l'idée de refuge.",
    "pt": "Jardim do Mar vive de charme, silêncio e caráter costeiro, e não de grandes gestos. É exatamente por isso que materiais, mobiliário e apresentação exterior têm de permanecer coerentes, porque nesta malha densa de povoado a desordem torna-se visível de imediato e destrói a sensação de refúgio."
  },
  "paul-do-mar": {
    "de": "Paul do Mar wird oft mit Leichtigkeit, Sonne und Meer assoziiert. Hinter dieser entspannten Außenwirkung braucht eine hochwertige Immobilie jedoch straffe Abläufe, damit Salzeintrag, Außenabnutzung und schnelle Nutzungswechsel nicht zu einem dauernden Nacharbeiten führen.",
    "en": "Paul do Mar is often associated with ease, sun and ocean. Behind that relaxed image, however, a premium property needs disciplined routines so that salt exposure, exterior wear and quick usage changes do not turn into constant catch-up work.",
    "fr": "Paul do Mar est souvent associé à la légèreté, au soleil et à l'océan. Derrière cette image détendue, une propriété haut de gamme a pourtant besoin de routines strictes pour que le sel, l'usure extérieure et les changements rapides d'usage ne se transforment pas en corrections permanentes.",
    "pt": "Paul do Mar é muitas vezes associado a leveza, sol e oceano. Por trás dessa imagem descontraída, um imóvel premium precisa contudo de rotinas disciplinadas para que sal, desgaste exterior e mudanças rápidas de utilização não se transformem em correções constantes."
  },
  "ponta-do-pargo": {
    "de": "Ponta do Pargo verlangt einen Betreuungsstil, der auch ohne ständige Nähe funktioniert. Wenn Eigentümer Ruhe und Weite suchen, muss das Haus im Hintergrund umso stabiler organisiert sein, weil spontane Kontrollbesuche oder schnelle Korrekturen nicht immer realistisch sind.",
    "en": "Ponta do Pargo requires a supervision style that works even without constant proximity. When owners choose openness and silence, the house has to be organised all the more reliably in the background because spontaneous check-ins or quick corrections are not always realistic.",
    "fr": "Ponta do Pargo exige un style de suivi capable de fonctionner sans proximité permanente. Lorsque les propriétaires recherchent l'espace et le silence, la maison doit être d'autant plus solidement organisée en arrière-plan, car les visites spontanées ou corrections rapides ne sont pas toujours réalistes.",
    "pt": "A Ponta do Pargo exige um estilo de acompanhamento capaz de funcionar sem proximidade permanente. Quando os proprietários procuram espaço e silêncio, a casa tem de estar ainda mais solidamente organizada em segundo plano, porque visitas espontâneas ou correções rápidas nem sempre são realistas."
  },
  "ponta-do-sol": {
    "de": "In Ponta do Sol fällt die Wirkung einer Immobilie oft über Licht, Glas, Blickachsen und architektonische Ruhe. Genau diese Qualitäten sind empfindlich gegen sichtbare Gebrauchsspuren, weshalb hier nicht nur kontrolliert, sondern kuratiert und bewusst vorbereitet werden muss.",
    "en": "In Ponta do Sol, a property often works through light, glass, visual axes and architectural calm. Those qualities are highly sensitive to visible signs of use, which means supervision here must not only inspect but curate and prepare deliberately.",
    "fr": "À Ponta do Sol, l'effet d'un bien passe souvent par la lumière, le verre, les lignes de vue et la tranquillité architecturale. Ces qualités sont très sensibles aux traces visibles d'usage, ce qui signifie qu'ici le suivi doit non seulement contrôler, mais aussi préparer de manière très intentionnelle.",
    "pt": "Na Ponta do Sol, o impacto de um imóvel passa muitas vezes pela luz, pelo vidro, pelos eixos visuais e pela calma arquitetónica. Essas qualidades são muito sensíveis a marcas visíveis de uso, o que significa que aqui o acompanhamento não deve apenas verificar, mas também preparar de forma intencional."
  },
  "porto-moniz": {
    "de": "Porto Moniz fordert besonders viel Vorausschau, weil die Küstenlage spektakulär ist, aber Wetter und Distanz die Planung beeinflussen. Je höher die Qualität der Immobilie, desto wichtiger wird ein System, das nicht auf Reaktion, sondern auf vorbeugende Stabilität setzt.",
    "en": "Porto Moniz demands a high level of foresight because the coastal setting is spectacular but weather and distance influence planning. The higher the property standard, the more important a system becomes that is based on preventive stability rather than reaction alone.",
    "fr": "Porto Moniz demande beaucoup d'anticipation, car le cadre côtier est spectaculaire mais la météo et la distance influencent fortement la planification. Plus le niveau du bien est élevé, plus il devient important de s'appuyer sur un système fondé sur la stabilité préventive plutôt que sur la réaction seule.",
    "pt": "O Porto Moniz exige muita antecipação, porque o cenário costeiro é espetacular, mas o tempo e a distância influenciam fortemente o planeamento. Quanto mais elevado é o nível do imóvel, mais importante se torna um sistema baseado em estabilidade preventiva e não apenas em reação."
  },
  "ribeira-brava": {
    "de": "Ribeira Brava verbindet Zentralität mit privater Wohnqualität. Gerade diese Mischung führt dazu, dass Eigentümer häufig sowohl Flexibilität als auch Verlässlichkeit erwarten: kurze Wege im Alltag, aber gleichzeitig den ruhigen Standard einer diskret geführten Premiumresidenz.",
    "en": "Ribeira Brava combines centrality with private residential quality. That mix often means owners expect both flexibility and reliability: short practical distances in daily life and, at the same time, the calm standard of a discreetly run premium residence.",
    "fr": "Ribeira Brava combine centralité et qualité résidentielle privée. Ce mélange conduit souvent les propriétaires à attendre à la fois flexibilité et fiabilité: des distances pratiques courtes au quotidien, mais en même temps le standard calme d'une résidence premium gérée avec discrétion.",
    "pt": "A Ribeira Brava combina centralidade com qualidade residencial privada. Esta mistura faz com que os proprietários esperem muitas vezes flexibilidade e fiabilidade ao mesmo tempo: distâncias curtas no dia a dia, mas também o padrão calmo de uma residência premium gerida com discrição."
  },
  "santa-cruz": {
    "de": "Santa Cruz ist oft stärker an Bewegungsrhythmen gebunden als andere Orte. Wer nahe am Flughafen oder an schnellen Verkehrsachsen wohnt, erwartet häufig spontane Nutzbarkeit, klare Schlüsselprozesse und ein Haus, das auch bei kurzfristigen Aufenthalten sofort funktioniert.",
    "en": "Santa Cruz is often more closely tied to movement patterns than other locations. Anyone living near the airport or fast road links frequently expects spontaneous usability, clear key processes and a home that works immediately even for short-notice stays.",
    "fr": "Santa Cruz est souvent plus lié aux rythmes de déplacement que d'autres lieux. Vivre près de l'aéroport ou des axes rapides conduit fréquemment à attendre une utilisation spontanée, une gestion claire des clés et une maison immédiatement opérationnelle, même pour des séjours décidés tardivement.",
    "pt": "Santa Cruz está muitas vezes mais ligado a ritmos de deslocação do que outros locais. Quem vive perto do aeroporto ou de vias rápidas espera com frequência utilização espontânea, processos claros de chaves e uma casa imediatamente funcional, mesmo para estadias decididas à última hora."
  },
  "santana": {
    "de": "In Santana ist der Schutz der Bausubstanz oft enger mit Außenräumen verbunden als in sonnigeren Küstenlagen. Dächer, Wasserführung, Vegetation und traditionelle Materialien müssen gemeinsam gedacht werden, damit die Immobilie hochwertig wirkt und nicht schleichend an Qualität verliert.",
    "en": "In Santana, protecting the building substance is often more closely linked to exterior spaces than in sunnier coastal settings. Roofs, water flow, vegetation and traditional materials have to be considered together so the property keeps its quality instead of slowly losing it.",
    "fr": "À Santana, la protection du bâti est souvent plus étroitement liée aux espaces extérieurs que dans les zones côtières plus ensoleillées. Toitures, circulation de l'eau, végétation et matériaux traditionnels doivent être pensés ensemble afin que le bien conserve sa qualité au lieu de la perdre progressivement.",
    "pt": "Em Santana, a proteção da estrutura do edifício está muitas vezes mais ligada aos espaços exteriores do que nas zonas costeiras mais soalheiras. Coberturas, escoamento de água, vegetação e materiais tradicionais têm de ser pensados em conjunto para que o imóvel mantenha a sua qualidade em vez de a perder lentamente."
  },
  "sao-jorge": {
    "de": "São Jorge verlangt ein starkes Verständnis für Gärten, Hangstruktur und die Wirkung eines Hauses in einer grünen Nordkulisse. Hier ist Pflege nicht bloß Kosmetik, sondern ein laufendes Austarieren zwischen Naturdynamik, Erreichbarkeit und hochwertigem Wohnbild.",
    "en": "São Jorge requires a strong understanding of gardens, hillside structure and the visual effect of a house in a lush northern landscape. Care here is not mere cosmetics but a continuous balancing act between natural dynamics, accessibility and premium residential appearance.",
    "fr": "São Jorge exige une vraie compréhension des jardins, de la structure en pente et de l'effet visuel d'une maison dans un paysage nordique très vert. Ici, l'entretien n'est pas une simple cosmétique, mais un ajustement permanent entre dynamique naturelle, accessibilité et image résidentielle haut de gamme.",
    "pt": "São Jorge exige uma compreensão real dos jardins, da estrutura em encosta e do efeito visual de uma casa numa paisagem verde do norte. Aqui, o cuidado não é mera cosmética, mas um equilíbrio contínuo entre dinâmica natural, acessibilidade e imagem residencial premium."
  },
  "sao-vicente": {
    "de": "São Vicente funktioniert anders als reine Küstenorte, weil Talraum, Berghinterland und Nordklima gleichzeitig auf die Immobilie wirken. Gute Betreuung muss deshalb besonders sauber zwischen Innenraumgefühl, Außenpflege und wetterbedingter Vorsorge verzahnen.",
    "en": "São Vicente works differently from purely coastal locations because valley setting, mountain backdrop and north-coast climate affect the property at the same time. Good supervision therefore has to connect interior feel, exterior care and weather-related prevention especially cleanly.",
    "fr": "São Vicente fonctionne différemment des lieux purement côtiers, car vallée, arrière-pays montagneux et climat du nord agissent simultanément sur le bien. Un bon suivi doit donc articuler avec une grande précision la sensation intérieure, l'entretien extérieur et la prévention liée à la météo.",
    "pt": "São Vicente funciona de forma diferente dos locais puramente costeiros, porque vale, enquadramento montanhoso e clima da costa norte atuam ao mesmo tempo sobre o imóvel. Um bom acompanhamento tem por isso de articular com especial precisão sensação interior, cuidado exterior e prevenção ligada ao tempo."
  }
}

DISPLAY_NAMES = {
  "boaventura": {
    "de": "Boaventura",
    "en": "Boaventura",
    "fr": "Boaventura",
    "pt": "Boaventura"
  },
  "calheta": {
    "de": "Calheta",
    "en": "Calheta",
    "fr": "Calheta",
    "pt": "Calheta"
  },
  "camara-de-lobos": {
    "de": "Câmara de Lobos",
    "en": "Câmara de Lobos",
    "fr": "Câmara de Lobos",
    "pt": "Câmara de Lobos"
  },
  "campanario": {
    "de": "Campanário",
    "en": "Campanário",
    "fr": "Campanário",
    "pt": "Campanário"
  },
  "canico": {
    "de": "Caniço",
    "en": "Caniço",
    "fr": "Caniço",
    "pt": "Caniço"
  },
  "curral-das-freiras": {
    "de": "Curral das Freiras",
    "en": "Curral das Freiras",
    "fr": "Curral das Freiras",
    "pt": "Curral das Freiras"
  },
  "funchal": {
    "de": "Funchal",
    "en": "Funchal",
    "fr": "Funchal",
    "pt": "Funchal"
  },
  "jardim-do-mar": {
    "de": "Jardim do Mar",
    "en": "Jardim do Mar",
    "fr": "Jardim do Mar",
    "pt": "Jardim do Mar"
  },
  "paul-do-mar": {
    "de": "Paul do Mar",
    "en": "Paul do Mar",
    "fr": "Paul do Mar",
    "pt": "Paul do Mar"
  },
  "ponta-do-pargo": {
    "de": "Ponta do Pargo",
    "en": "Ponta do Pargo",
    "fr": "Ponta do Pargo",
    "pt": "Ponta do Pargo"
  },
  "ponta-do-sol": {
    "de": "Ponta do Sol",
    "en": "Ponta do Sol",
    "fr": "Ponta do Sol",
    "pt": "Ponta do Sol"
  },
  "porto-moniz": {
    "de": "Porto Moniz",
    "en": "Porto Moniz",
    "fr": "Porto Moniz",
    "pt": "Porto Moniz"
  },
  "ribeira-brava": {
    "de": "Ribeira Brava",
    "en": "Ribeira Brava",
    "fr": "Ribeira Brava",
    "pt": "Ribeira Brava"
  },
  "santa-cruz": {
    "de": "Santa Cruz",
    "en": "Santa Cruz",
    "fr": "Santa Cruz",
    "pt": "Santa Cruz"
  },
  "santana": {
    "de": "Santana",
    "en": "Santana",
    "fr": "Santana",
    "pt": "Santana"
  },
  "sao-jorge": {
    "de": "São Jorge",
    "en": "São Jorge",
    "fr": "São Jorge",
    "pt": "São Jorge"
  },
  "sao-vicente": {
    "de": "São Vicente",
    "en": "São Vicente",
    "fr": "São Vicente",
    "pt": "São Vicente"
  }
}


LANG_DIRS = {
    "de": "src/de/orte",
    "en": "src/en/locations",
    "fr": "src/fr/lieux",
    "pt": "src/pt/locais",
}


BUILD_DIRS = {
    "de": "_site/de/orte",
    "en": "_site/en/locations",
    "fr": "_site/fr/lieux",
    "pt": "_site/pt/locais",
}

PLACEHOLDER_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")

def sync_built_file(path: Path, title: str, description: str, body: str) -> None:
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", html, count=1, flags=re.DOTALL)
    html = re.sub(
        r"<meta\s+name=[\"']description[\"']\s+content=[\"'].*?[\"']\s*/?>",
        lambda m: f'<meta name="description" content="{description}">',
        html, count=1, flags=re.IGNORECASE | re.DOTALL
    )
    section_match = re.search(r"<section class=\"text-intro\">.*?</section>", html, flags=re.DOTALL)
    if section_match:
        html = html[:section_match.start()] + body + html[section_match.end():]
    path.write_text(html, encoding="utf-8")

def scan_placeholders(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return sorted(set(PLACEHOLDER_RE.findall(text)))

TOKEN_RE = re.compile(r"\b[\wÀ-ÿ'-]+\b", re.UNICODE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)

def join_list(items, lang):
    if len(items) == 1:
        return items[0]
    conj = {"de": " und ", "en": " and ", "fr": " et ", "pt": " e "}[lang]
    return ", ".join(items[:-1]) + conj + items[-1]

def strip_html(html):
    return re.sub(r"<[^>]+>", " ", html)

def word_count(html):
    return len(TOKEN_RE.findall(strip_html(html)))

def cosine_similarity(text_a, text_b):
    tokens_a = [t.lower() for t in TOKEN_RE.findall(text_a) if len(t) > 2]
    tokens_b = [t.lower() for t in TOKEN_RE.findall(text_b) if len(t) > 2]
    ca = Counter(tokens_a)
    cb = Counter(tokens_b)
    if not ca or not cb:
        return 0.0
    dot = sum(ca[k] * cb.get(k, 0) for k in ca)
    na = math.sqrt(sum(v * v for v in ca.values()))
    nb = math.sqrt(sum(v * v for v in cb.values()))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)

def replace_frontmatter_value(frontmatter: str, key: str, value: str) -> str:
    escaped = value.replace('"', '\\"')
    pattern = re.compile(r"^(\s*" + re.escape(key) + r":\s*)(.*)$", re.MULTILINE)
    if pattern.search(frontmatter):
        return pattern.sub(r'\1"' + escaped + '"', frontmatter, count=1)
    lines = frontmatter.splitlines()
    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.strip().startswith("layout:"):
            insert_at = idx
            break
    lines.insert(insert_at, f'{key}: "{escaped}"')
    return "\n".join(lines)

def make_geo(profile, lang):
    reg = REGION_PHRASE[lang][profile["region"]]
    setp = SETTING_PHRASE[lang][profile["setting"]]
    loc = profile["name"][lang]
    if lang == "de":
        return f"{loc} liegt {reg} und ist {setp}. Genau diese Kombination aus Lage, Bauweise und Nutzung macht den Ort aus Sicht der Hausbetreuung deutlich anders als die klassischen Standardlagen auf Madeira."
    if lang == "en":
        return f"{loc} sits {reg} and is {setp}. That exact combination of location, building style and usage makes the area very different from standard property-care situations in Madeira."
    if lang == "fr":
        return f"{loc} se situe {reg} et se caractérise par un cadre {setp}. Cette combinaison de situation, de typologie bâtie et d'usage distingue clairement la zone des scénarios standard de gestion résidentielle à Madère."
    return f"{loc} fica {reg} e caracteriza-se por um contexto {setp}. Essa combinação de localização, tipologia construída e uso distingue claramente a zona dos cenários residenciais padronizados na Madeira."

def make_property(profile, lang):
    mixes = [MIX_PHRASE[lang][m] for m in profile["property_mix"]]
    owners = [OWNER_PHRASE[lang][o] for o in profile["owners"]]
    loc = profile["name"][lang]
    if lang == "de":
        return f"In {loc} profitieren vor allem {join_list(mixes, lang)}. Solche Immobilien werden häufig als {join_list(owners, lang)} genutzt. Dadurch entstehen Anforderungen, die über reine Reinigung hinausgehen: Der Zustand muss über längere Leerstandsphasen stabil bleiben, Außenflächen müssen repräsentativ wirken und die Immobilie soll vor jeder Rückkehr sofort funktionieren."
    if lang == "en":
        return f"In {loc}, the greatest benefit is usually seen in {join_list(mixes, lang)}. These homes are often used as {join_list(owners, lang)}. That creates requirements that go far beyond occasional cleaning: condition has to remain stable during absence periods, exterior spaces need to stay representative, and the property should work immediately before every return."
    if lang == "fr":
        return f"À {loc}, ce sont surtout {join_list(mixes, lang)} qui profitent le plus d'un suivi structuré. Ces biens sont souvent utilisés comme {join_list(owners, lang)}. Cela crée des exigences qui dépassent largement le simple nettoyage: l'état du bien doit rester stable pendant les absences, les extérieurs doivent rester représentatifs et la maison doit être immédiatement fonctionnelle avant chaque retour."
    return f"Em {loc}, quem mais beneficia de um acompanhamento estruturado são {join_list(mixes, lang)}. Estes imóveis são frequentemente usados como {join_list(owners, lang)}. Isso cria exigências que vão muito além de uma limpeza ocasional: o estado do imóvel precisa de permanecer estável durante as ausências, os exteriores devem manter imagem representativa e a casa tem de funcionar de imediato antes de cada regresso."

def make_owners(profile, lang):
    loc = profile["name"][lang]
    if lang == "de":
        return f"Internationale Eigentümer erwarten in {loc} vor allem Klarheit. Sie möchten wissen, dass das Haus zwischen zwei Aufenthalten strukturiert betreut wird, ohne bei jeder kleinen Frage selbst operativ eingreifen zu müssen. Dazu gehören diskrete Kommunikation, dokumentierte Sichtkontrollen, saubere Priorisierung und eine Vorbereitung, die nicht erst am Anreisetag beginnt."
    if lang == "en":
        return f"International owners in {loc} primarily expect clarity. They want to know that the home is being looked after in a structured way between stays without having to step into daily operational questions themselves. That includes discreet communication, documented checks, clear prioritisation and preparation that begins well before the day of arrival."
    if lang == "fr":
        return f"Les propriétaires internationaux à {loc} attendent avant tout de la clarté. Ils veulent savoir que la maison est suivie de manière structurée entre deux séjours sans devoir gérer eux-mêmes chaque détail opérationnel. Cela implique une communication discrète, des contrôles documentés, des priorités lisibles et une préparation qui commence bien avant le jour d'arrivée."
    return f"Os proprietários internacionais em {loc} esperam acima de tudo clareza. Querem saber que a casa é acompanhada de forma estruturada entre estadias sem terem de entrar em cada detalhe operacional. Isso inclui comunicação discreta, verificações documentadas, prioridades bem definidas e uma preparação que começa muito antes do dia da chegada."

def make_nonstandard(profile, lang):
    pres = [PRESSURE_PHRASE[lang][p] for p in profile["pressures"][:2]]
    ops = [OPS_PHRASE[lang][o] for o in profile["ops"][:2]]
    loc = profile["name"][lang]
    if lang == "de":
        return f"Standardlösungen greifen in {loc} meist zu kurz. Wo {join_list(pres, lang)} den Alltag prägen, reicht es nicht, nur punktuell zu reagieren. Entscheidend ist eine Betreuungslogik, die {join_list(ops, lang)} miteinander verbindet und Veränderungen nicht erst dann bemerkt, wenn Eigentümer oder Gäste bereits vor Ort sind."
    if lang == "en":
        return f"Standard solutions are usually too shallow in {loc}. Where {join_list(pres, lang)} shape daily reality, occasional reaction is not enough. What matters is a supervision logic that links {join_list(ops, lang)} and notices change before owners or guests are already on site."
    if lang == "fr":
        return f"Les solutions standard sont généralement trop limitées à {loc}. Là où {join_list(pres, lang)} structurent le quotidien, une réaction ponctuelle ne suffit pas. Il faut une logique de suivi qui relie {join_list(ops, lang)} et qui détecte les évolutions avant même que propriétaires ou invités ne soient sur place."
    return f"As soluções standard são normalmente demasiado superficiais em {loc}. Onde {join_list(pres, lang)} moldam o dia a dia, reagir pontualmente não chega. O que conta é uma lógica de acompanhamento que liga {join_list(ops, lang)} e percebe alterações antes mesmo de proprietários ou convidados estarem no local."

def make_owner_expectations(profile, lang):
    loc = profile["name"][lang]
    if lang == "de":
        return f"Gerade bei hochwertigen Häusern in {loc} geht es Eigentümern selten nur um Schadensvermeidung. Sie erwarten vielmehr, dass Atmosphäre, Ordnung und Nutzbarkeit konstant bleiben, damit die Immobilie auch nach Wochen ohne Nutzung denselben souveränen Eindruck vermittelt wie am Tag der Abreise. Dieses Qualitätsgefühl muss in jedem Bereich nachvollziehbar bleiben."
    if lang == "en":
        return f"In high-end homes in {loc}, owners rarely care only about avoiding damage. They also expect atmosphere, order and usability to remain constant so the property conveys the same sense of control weeks later as it did on the day of departure. That feeling of quality has to remain legible in every area."
    if lang == "fr":
        return f"Dans les maisons haut de gamme à {loc}, les propriétaires ne cherchent pas seulement à éviter les dommages. Ils attendent aussi que l'atmosphère, l'ordre et l'usage restent constants afin que le bien donne, même après plusieurs semaines, la même impression qu'au jour du départ. Cette qualité doit rester perceptible partout."
    return f"Em casas premium em {loc}, os proprietários raramente procuram apenas evitar danos. Também esperam que atmosfera, ordem e usabilidade permaneçam constantes para que o imóvel transmita, mesmo após várias semanas, a mesma sensação de controlo que no dia da partida. Essa perceção de qualidade tem de ser visível em todo o conjunto."

def make_risks(profile, lang):
    pres = [PRESSURE_PHRASE[lang][p] for p in profile["pressures"]]
    if lang == "de":
        return f"Für hochwertige Immobilien sind in dieser Lage besonders {join_list(pres, lang)} relevant. Diese Faktoren wirken selten spektakulär in einem einzigen Moment, sondern schleichend über Wochen und Monate. Genau deshalb ist eine dokumentierte Routine so wichtig: Kleine Abweichungen werden früh erkannt, bevor aus optischen Details echte Folgekosten oder ein unruhiger Eindruck vor der Eigentümerankunft entstehen."
    if lang == "en":
        return f"For premium homes in this setting, the main concerns are {join_list(pres, lang)}. These factors rarely become dramatic in a single moment; they build up gradually over weeks and months. That is exactly why a documented routine matters: small changes can be identified early before visual details turn into follow-up costs or an unsettled impression before arrival."
    if lang == "fr":
        return f"Pour des biens haut de gamme dans ce contexte, les points les plus sensibles sont {join_list(pres, lang)}. Ces facteurs deviennent rarement critiques d'un seul coup; ils s'installent lentement sur plusieurs semaines ou plusieurs mois. C'est précisément pourquoi une routine documentée est essentielle: les petites variations sont détectées tôt, avant qu'un détail visuel ne se transforme en coût supplémentaire ou en mauvaise impression au retour du propriétaire."
    return f"Para imóveis premium neste contexto, os fatores mais sensíveis são {join_list(pres, lang)}. Estes elementos raramente se tornam críticos de uma vez só; acumulam-se lentamente ao longo de semanas e meses. É exatamente por isso que uma rotina documentada é essencial: pequenas alterações são detetadas cedo, antes de um detalhe visual se transformar em custo adicional ou numa má impressão no regresso do proprietário."

def make_documentation(profile, lang):
    ops = [OPS_PHRASE[lang][o] for o in profile["ops"]]
    loc = profile["name"][lang]
    if lang == "de":
        return f"Für Eigentümer ist außerdem wichtig, dass Betreuung nachvollziehbar bleibt. In {loc} bedeutet das, Beobachtungen sauber zu erfassen, Maßnahmen sinnvoll zu bündeln und aus {join_list(ops, lang)} keinen Zufallsprozess werden zu lassen. Nur so entsteht aus einzelnen Einsätzen ein belastbarer Standard, auf den man sich auch aus dem Ausland verlassen kann."
    if lang == "en":
        return f"Owners also need the process to remain understandable. In {loc}, that means recording observations cleanly, bundling actions sensibly and preventing {join_list(ops, lang)} from becoming a random sequence. Only then do individual visits become a dependable standard that can be trusted from abroad."
    if lang == "fr":
        return f"Les propriétaires ont aussi besoin d'un processus lisible. À {loc}, cela signifie documenter clairement les observations, regrouper les mesures de façon cohérente et éviter que {join_list(ops, lang)} ne se transforme en suite d'actions aléatoires. C'est la condition pour qu'une série d'interventions devienne un standard fiable, même à distance."
    return f"Os proprietários também precisam de um processo compreensível. Em {loc}, isso significa registar observações com clareza, agrupar medidas com coerência e evitar que {join_list(ops, lang)} se transforme numa sequência aleatória. Só assim visitas individuais se tornam num padrão fiável em que se pode confiar à distância."


def make_local_priorities(profile, lang):
    loc = profile["name"][lang]
    priorities = [OPS_PHRASE[lang][o] for o in profile["ops"]]
    risks = [PRESSURE_PHRASE[lang][p] for p in profile["pressures"][:2]]
    if lang == "de":
        return f"In {loc} zeigt sich Qualität vor allem daran, dass {join_list(priorities, lang)} nicht isoliert, sondern mit Blick auf {join_list(risks, lang)} organisiert werden. So entsteht ein Betreuungsstil, der lokale Bedingungen ernst nimmt und die Immobilie sichtbar stabil hält. Genau diese Konsequenz macht den Unterschied zwischen bloßer Pflege und verlässlicher Hausbetreuung."
    if lang == "en":
        return f"In {loc}, quality is visible above all when {join_list(priorities, lang)} are not handled in isolation but organised with {join_list(risks, lang)} in mind. That creates a supervision style that takes local conditions seriously and keeps the property visibly stable. This is where routine becomes a measurable standard rather than a vague promise."
    if lang == "fr":
        return f"À {loc}, la qualité se voit surtout lorsque {join_list(priorities, lang)} ne sont pas traités isolément mais organisés en tenant compte de {join_list(risks, lang)}. On obtient ainsi un style de suivi qui prend les conditions locales au sérieux et maintient le bien dans un état visiblement stable. C’est là que la routine devient un vrai standard."
    return f"Em {loc}, a qualidade torna-se visível sobretudo quando {join_list(priorities, lang)} não são tratados de forma isolada, mas organizados tendo em conta {join_list(risks, lang)}. Assim nasce um estilo de acompanhamento que leva as condições locais a sério e mantém o imóvel visivelmente estável. É aqui que a rotina passa a ser um padrão real."

def make_service(profile, lang):
    ops = [OPS_PHRASE[lang][o] for o in profile["ops"]]
    vend = VENDOR_PHRASE[lang][profile["vendors"]]
    loc = profile["name"][lang]
    if lang == "de":
        return f"Unser Ansatz in {loc} verbindet {join_list(ops, lang)}. Dadurch entsteht kein loses Sammelsurium einzelner Einsätze, sondern ein klar geführtes Betreuungsmodell mit wiederkehrenden Standards. {vend} Gerade in einer Luxusimmobilie zählt nicht nur, dass Aufgaben erledigt werden, sondern dass sie in der richtigen Reihenfolge, mit dem passenden Qualitätsniveau und ohne unnötigen Abstimmungsaufwand für den Eigentümer umgesetzt werden."
    if lang == "en":
        return f"Our approach in {loc} combines {join_list(ops, lang)}. That creates a clear supervision model with recurring standards instead of a loose collection of isolated visits. {vend} In a premium property, it is not enough that tasks get done; they have to be handled in the right sequence, at the right quality level and without unnecessary coordination effort for the owner."
    if lang == "fr":
        return f"Notre approche à {loc} combine {join_list(ops, lang)}. On obtient ainsi un modèle de suivi clair avec des standards récurrents, et non une simple succession d'interventions isolées. {vend} Dans un bien haut de gamme, il ne suffit pas que les tâches soient réalisées; elles doivent l'être dans le bon ordre, au bon niveau de qualité et sans surcharge de coordination pour le propriétaire."
    return f"A nossa abordagem em {loc} combina {join_list(ops, lang)}. Assim nasce um modelo de acompanhamento claro com padrões recorrentes, e não um conjunto solto de intervenções isoladas. {vend} Num imóvel premium, não basta que as tarefas sejam executadas; elas têm de ser realizadas na sequência certa, no nível de qualidade certo e sem esforço de coordenação desnecessário para o proprietário."

def make_arrival(profile, lang):
    loc = profile["name"][lang]
    if lang == "de":
        return f"Vor einer Anreise bedeutet das in {loc} ganz praktisch: Innenräume wirken gepflegt, sensible Bereiche sind geprüft, Außenflächen zeigen Ordnung und der Gesamteindruck entspricht dem Wert der Immobilie. Für internationale Eigentümer ist genau diese Anreisebereitschaft entscheidend. Sie möchten nicht erst nach Kontrollen, Nachbesserungen oder offenen Fragen in den Aufenthalt starten, sondern in ein Haus kommen, das Ruhe, Struktur und Souveränität ausstrahlt."
    if lang == "en":
        return f"Before an arrival, this means something very practical in {loc}: interiors feel cared for, sensitive areas have been checked, outdoor zones look orderly and the overall impression matches the value of the property. For international owners, that readiness is decisive. They do not want to begin a stay with follow-up checks, corrections or open questions, but with a home that conveys calm, structure and control."
    if lang == "fr":
        return f"Avant une arrivée, cela se traduit très concrètement à {loc}: les intérieurs paraissent soignés, les zones sensibles ont été contrôlées, les extérieurs sont ordonnés et l'impression générale correspond à la valeur du bien. Pour les propriétaires internationaux, cette disponibilité est déterminante. Ils ne veulent pas commencer leur séjour avec des vérifications supplémentaires, des ajustements ou des questions ouvertes, mais dans une maison qui exprime calme, structure et maîtrise."
    return f"Antes de uma chegada, isso traduz-se de forma muito concreta em {loc}: os interiores parecem cuidados, as zonas sensíveis foram verificadas, os exteriores apresentam ordem e a impressão geral corresponde ao valor do imóvel. Para proprietários internacionais, esta prontidão é decisiva. Não querem iniciar a estadia com controlos adicionais, correções ou dúvidas em aberto, mas sim numa casa que transmite calma, estrutura e controlo."

def make_continuity(profile, lang):
    loc = profile["name"][lang]
    if lang == "de":
        return f"Genau diese Kontinuität macht aus Hausbetreuung einen echten Werterhaltungsfaktor. Wer ein hochwertiges Objekt in {loc} besitzt, braucht nicht bloß jemanden, der Aufgaben abhakt, sondern ein System, das Übersicht schafft, Standards hält und Entscheidungen vorbereitet. So bleibt die Immobilie nicht nur nutzbar, sondern dauerhaft stimmig im Gesamtbild."
    if lang == "en":
        return f"That continuity is what turns home supervision into a real value-protection factor. Anyone who owns a high-end property in {loc} needs more than a person who completes isolated tasks; they need a system that creates oversight, maintains standards and prepares decisions. This keeps the property not merely usable but coherent in its overall quality."
    if lang == "fr":
        return f"C'est précisément cette continuité qui fait du suivi résidentiel un véritable facteur de préservation de valeur. Posséder un bien haut de gamme à {loc} exige plus qu'une personne qui coche des tâches; il faut un système qui crée de la visibilité, maintient les standards et prépare les décisions. Le bien reste ainsi non seulement utilisable, mais cohérent dans son ensemble."
    return f"É precisamente esta continuidade que transforma o acompanhamento residencial num verdadeiro fator de preservação de valor. Quem possui um imóvel premium em {loc} precisa de mais do que alguém que execute tarefas isoladas; precisa de um sistema que dê visão global, mantenha padrões e prepare decisões. Assim, o imóvel permanece não só utilizável, mas coerente no seu conjunto."

def make_value(profile, lang):
    closing = profile["signature"][lang]
    link = LANG_META[lang]["home"]
    if lang == "de":
        return f"{closing} Langfristig senkt diese Art der Betreuung das Organisationsrisiko, schützt den repräsentativen Eindruck und hilft dabei, Substanz, Außenwirkung und Nutzbarkeit dauerhaft auf hohem Niveau zu halten. Weitere Informationen zu unserem Betreuungsansatz finden Sie hier: <a class=\"cta-link\" href=\"{link}\">Mehr über Luxury Property Care</a>."
    if lang == "en":
        return f"{closing} Over time, this kind of supervision reduces organisational risk, protects the representative appearance of the property and helps maintain substance, presentation and usability at a high level. For more information about our approach, see <a class=\"cta-link\" href=\"{link}\">Learn more about Luxury Property Care</a>."
    if lang == "fr":
        return f"{closing} À long terme, ce type de suivi réduit le risque organisationnel, protège l'image représentative du bien et aide à maintenir durablement sa substance, sa présentation et sa facilité d'usage à un niveau élevé. Pour en savoir plus sur notre approche, consultez <a class=\"cta-link\" href=\"{link}\">En savoir plus sur Luxury Property Care</a>."
    return f"{closing} A longo prazo, este tipo de acompanhamento reduz o risco organizacional, protege a imagem representativa do imóvel e ajuda a manter de forma duradoura a sua substância, apresentação e usabilidade num nível elevado. Para mais informações sobre a nossa abordagem, consulte <a class=\"cta-link\" href=\"{link}\">Saber mais sobre Luxury Property Care</a>."

def build_page(slug: str, profile: dict, lang: str):
    profile["name"] = DISPLAY_NAMES[slug]
    meta = LANG_META[lang]
    loc = profile["name"][lang]
    title = meta["title_fmt"].format(loc=loc)
    description = meta["desc_fmt"].format(loc=loc)
    h1 = meta["h1_fmt"].format(loc=loc)
    section_titles = {k: v.format(loc=loc) for k, v in meta["sections"].items()}
    section_paragraphs = {
        "overview": [make_geo(profile, lang)],
        "properties": [MICRO_NOTE[slug][lang], make_property(profile, lang)],
        "owners": [make_owners(profile, lang), make_nonstandard(profile, lang), make_owner_expectations(profile, lang)],
        "risks": [make_risks(profile, lang), make_documentation(profile, lang)],
        "service": [make_local_priorities(profile, lang), make_service(profile, lang)],
        "arrival": [make_arrival(profile, lang), VENDOR_PHRASE[lang][profile["vendors"]]],
        "value": [make_continuity(profile, lang), make_value(profile, lang)],
    }

    html_parts = [
        '<section class="text-intro">\n\n  <div class="hero-logo hero-logo--small">\n    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">\n  </div>',
        f"<h1>{h1}</h1>",
        f"<p>{profile['signature'][lang]} {make_geo(profile, lang)} {make_property(profile, lang)}</p>",
    ]
    for key in ["overview", "properties", "owners", "risks", "service", "arrival", "value"]:
        html_parts.append(f"<h2>{section_titles[key]}</h2>")
        for paragraph in section_paragraphs[key]:
            html_parts.append(f"<p>{paragraph}</p>")
    html_parts.append("</section>\n")
    return title, description, "\n\n".join(html_parts)

def update_file(path: Path, title: str, description: str, body: str) -> None:
    original = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(original)
    if not match:
        raise RuntimeError(f"Frontmatter not found in {path}")
    frontmatter = match.group(1)
    frontmatter = replace_frontmatter_value(frontmatter, "title", title)
    frontmatter = replace_frontmatter_value(frontmatter, "description", description)
    new_text = f"---\n{frontmatter}\n---\n\n{body}"
    path.write_text(new_text, encoding="utf-8")

def verify(root: Path):
    per_lang = {}
    for lang, rel_dir in LANG_DIRS.items():
        items = []
        for slug in LOCATIONS:
            file_path = root / rel_dir / slug / "index.njk"
            text = file_path.read_text(encoding="utf-8")
            body = FRONTMATTER_RE.sub("", text, count=1)
            wc = word_count(body)
            items.append((slug, wc, strip_html(body)))
        per_lang[lang] = items
    return per_lang

def main():
    root = Path.cwd()
    if not (root / "src").exists():
        print("Run this script from the project root.", file=sys.stderr)
        sys.exit(1)

    for lang, rel_dir in LANG_DIRS.items():
        for slug, profile in LOCATIONS.items():
            path = root / rel_dir / slug / "index.njk"
            if not path.exists():
                raise FileNotFoundError(path)
            title, description, body = build_page(slug, profile.copy(), lang)
            update_file(path, title, description, body)
            built_path = root / BUILD_DIRS[lang] / slug / "index.html"
            sync_built_file(built_path, title, description, body)

    bad = []
    for lang, rel_dir in LANG_DIRS.items():
        for slug in LOCATIONS:
            source_path = root / rel_dir / slug / "index.njk"
            unresolved = scan_placeholders(source_path)
            if unresolved:
                bad.append((source_path, unresolved))
            built_path = root / BUILD_DIRS[lang] / slug / "index.html"
            if built_path.exists():
                unresolved = scan_placeholders(built_path)
                if unresolved:
                    bad.append((built_path, unresolved))

    if bad:
        lines = [f"{p}: {u}" for p, u in bad[:50]]
        raise RuntimeError("Unresolved placeholders found after rewrite:\n" + "\n".join(lines))

    report = verify(root)
    has_error = False
    print("\nLOCATION PAGE CONTENT REPORT")
    print("=" * 72)
    for lang, items in report.items():
        counts = [wc for _, wc, _ in items]
        print(f"\n{lang.upper()} -> min={min(counts)}, max={max(counts)}, pages={len(items)}")
        for slug, wc, _ in items:
            status = "OK" if 900 <= wc <= 1200 else "OUT"
            print(f"  {slug:20} {wc:4d} words  {status}")
            if status != "OK":
                has_error = True
        max_sim = 0.0
        pair = None
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                sim = cosine_similarity(items[i][2], items[j][2])
                if sim > max_sim:
                    max_sim = sim
                    pair = (items[i][0], items[j][0])
        print(f"  highest cosine similarity: {max_sim:.3f} between {pair[0]} and {pair[1]}")
    print("\nDone.")
    if has_error:
        sys.exit(2)

if __name__ == "__main__":
    main()
