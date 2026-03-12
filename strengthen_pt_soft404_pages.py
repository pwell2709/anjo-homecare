from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

PAGES = {
    "src/pt/locais/santana/index.njk": """
<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Luxury Property Care para imóveis de luxo em Santana</h1>

  <p>Santana situa-se na costa norte da Madeira e destaca-se por uma paisagem verde, encostas marcantes e uma atmosfera muito mais calma do que nas zonas urbanas da ilha. Para proprietários internacionais de moradias e segundas residências, esta localização oferece privacidade, autenticidade e um enquadramento natural muito especial.</p>

  <p>Ao mesmo tempo, a distância face às zonas mais movimentadas exige uma supervisão particularmente fiável. Quando o proprietário não está presente, a casa deve manter-se controlada, preparada e visualmente cuidada, independentemente das condições exteriores.</p>

  <h2>Características residenciais em Santana</h2>
  <p>Em Santana encontram-se moradias modernas, casas em terrenos amplos e propriedades com vistas abertas sobre o mar e a montanha. Muitas destas casas são usadas apenas em determinadas épocas do ano, o que aumenta a importância de um acompanhamento regular.</p>

  <p>Imóveis com baixa ocupação não devem transmitir a sensação de ausência prolongada. O objetivo do Property Care é preservar ordem, aparência e segurança operacional, para que a propriedade esteja sempre pronta para utilização pelos proprietários ou pelos seus convidados.</p>

  <h2>Microclima do norte da Madeira</h2>
  <p>A costa norte apresenta maior humidade, mudanças meteorológicas rápidas e uma pressão mais forte sobre superfícies exteriores, zonas de entrada, caixilharias e áreas expostas. Em casas de padrão elevado, estas condições exigem atenção constante.</p>

  <p>Um acompanhamento profissional ajuda a identificar cedo sinais visuais de desgaste, humidade, acumulação de sujidade ou necessidade de intervenção. Isso reduz o risco de pequenos problemas se tornarem questões maiores durante períodos sem presença do proprietário.</p>

  <h2>Property Care para proprietários internacionais</h2>
  <p>Muitos proprietários em Santana utilizam o imóvel como segunda residência ou casa de férias premium. Nesses casos, a expectativa não é apenas encontrar a casa fechada, mas sim encontrar a propriedade em estado cuidado, organizado e pronto para receber a próxima estadia.</p>

  <p>É precisamente aqui que um serviço estruturado se torna importante: supervisão visual, controlo geral do imóvel, verificação do estado aparente e uma base fiável para decisões rápidas quando algo exige atenção.</p>

  <h2>Serviço discreto e padrão premium</h2>
  <p>O nosso trabalho em Santana é orientado para discrição, clareza e consistência. Não se trata de gestão de arrendamento nem de administração imobiliária clássica, mas de um acompanhamento de qualidade para casas privadas de valor elevado.</p>

  <p>Para mais informações visite a página Property Care. <a class="cta-link" href="/pt/home/">Saiba mais sobre Luxury Property Care</a>.</p>
</section>
""".strip(),

    "src/pt/locais/sao-jorge/index.njk": """
<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Luxury Property Care para imóveis de luxo em São Jorge</h1>

  <p>São Jorge localiza-se na costa norte da Madeira, entre Santana e São Vicente, e combina tranquilidade, vegetação intensa e vistas abertas sobre o Atlântico. Para proprietários que procuram discrição e uma experiência residencial mais reservada, esta é uma zona muito atrativa.</p>

  <p>Ao mesmo tempo, casas em localizações menos centrais precisam de acompanhamento particularmente estável. Quando o imóvel é usado apenas em certas épocas, a supervisão regular ajuda a preservar a aparência, a funcionalidade geral e a sensação de cuidado permanente.</p>

  <h2>Perfil dos imóveis em São Jorge</h2>
  <p>Na região existem moradias modernas, casas em encosta e propriedades com forte ligação à paisagem natural. Muitas destas residências são escolhidas precisamente pela calma, pela privacidade e pela relação direta com a natureza da costa norte.</p>

  <p>Para imóveis deste tipo, o objetivo não é apenas manter um estado básico, mas assegurar que a propriedade continue visualmente preparada e coerente com um padrão residencial premium.</p>

  <h2>Condições climáticas e manutenção visual</h2>
  <p>O clima da costa norte é mais húmido e variável do que no sul da ilha. Isso influencia superfícies exteriores, acessos, zonas técnicas visíveis e a perceção geral do estado do imóvel. Em propriedades de valor elevado, pequenos sinais de deterioração visual não devem permanecer sem acompanhamento.</p>

  <p>Uma supervisão estruturada ajuda a identificar cedo alterações visíveis, necessidade de limpeza complementar, pontos que exigem atenção e situações que podem afetar a apresentação da casa ao longo do tempo.</p>

  <h2>Importância para proprietários ausentes</h2>
  <p>Muitos proprietários internacionais usam a casa apenas durante parte do ano. Nestes casos, é essencial saber que o imóvel continua acompanhado entre estadias e que a propriedade não fica simplesmente fechada sem controlo regular.</p>

  <p>Luxury Property Care oferece precisamente esta base: controlo visual, acompanhamento consistente e um ponto de contacto fiável para manter o imóvel num estado adequado entre períodos de utilização.</p>

  <h2>Abordagem premium e discreta</h2>
  <p>O foco está na discrição, na regularidade e no respeito pelo carácter privado do imóvel. Não se trata de uma gestão de hóspedes nem de operação turística, mas de um serviço orientado para proprietários de casas privadas e segundas residências na Madeira.</p>

  <p>Para mais informações visite a página Property Care. <a class="cta-link" href="/pt/home/">Saiba mais sobre Luxury Property Care</a>.</p>
</section>
""".strip(),

    "src/pt/locais/porto-moniz/index.njk": """
<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Luxury Property Care para imóveis de luxo em Porto Moniz</h1>

  <p>Porto Moniz situa-se no extremo noroeste da Madeira e é conhecido pelas suas piscinas naturais, pela costa dramática e por uma atmosfera mais tranquila e exclusiva. Para proprietários internacionais, esta região representa privacidade, paisagem marcante e um enquadramento muito distinto dentro da ilha.</p>

  <p>Imóveis nesta zona beneficiam de um acompanhamento profissional, especialmente quando são usados como segunda residência ou casa sazonal. A distância face a zonas mais centrais torna ainda mais importante um controlo fiável quando o proprietário está ausente.</p>

  <h2>Imóveis premium numa zona costeira exposta</h2>
  <p>Em Porto Moniz encontram-se moradias modernas, casas com vistas abertas e propriedades posicionadas para tirar partido máximo do oceano e da paisagem envolvente. Em imóveis de nível elevado, o padrão visual da casa deve manter-se consistente durante todo o ano.</p>

  <p>Isso exige mais do que simples encerramento do imóvel. Exige supervisão contínua, atenção à apresentação geral e um acompanhamento capaz de detetar cedo sinais visíveis que mereçam ação.</p>

  <h2>Condições da costa noroeste</h2>
  <p>A zona noroeste está mais exposta a vento atlântico, humidade e mudanças rápidas de tempo. Estas condições podem influenciar áreas exteriores, entradas, fachadas, elementos aparentes e o estado geral percebido da propriedade.</p>

  <p>Um serviço de Property Care ajuda a reduzir riscos, porque permite identificar cedo alterações visuais, necessidade de limpeza complementar, pontos sensíveis e pequenas irregularidades antes que se transformem em problemas maiores.</p>

  <h2>Segundas residências e casas de férias privadas</h2>
  <p>Muitos proprietários em Porto Moniz não ocupam a casa de forma contínua. Quando a utilização é sazonal, torna-se decisivo que a propriedade continue acompanhada entre estadias e que a chegada futura não comece com correções ou surpresas desnecessárias.</p>

  <p>O objetivo é simples: encontrar a casa organizada, controlada e compatível com o padrão esperado de uma residência premium na Madeira.</p>

  <h2>Discrição, estrutura e fiabilidade</h2>
  <p>Luxury Property Care em Porto Moniz é orientado para discrição, processos claros e acompanhamento consistente. Não substitui administração imobiliária, mas oferece a segurança operacional e visual que muitos proprietários internacionais procuram.</p>

  <p>Para mais informações visite a página Property Care. <a class="cta-link" href="/pt/home/">Saiba mais sobre Luxury Property Care</a>.</p>
</section>
""".strip(),

    "src/pt/locais/sao-vicente/index.njk": """
<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Luxury Property Care para imóveis de luxo em São Vicente</h1>

  <p>São Vicente combina costa norte, paisagem montanhosa e um ambiente mais reservado, muito procurado por proprietários que valorizam tranquilidade, autenticidade e privacidade. Para casas privadas de valor elevado, esta região oferece um contexto residencial muito especial dentro da Madeira.</p>

  <p>Ao mesmo tempo, propriedades nesta zona beneficiam de acompanhamento regular, sobretudo quando os proprietários não residem permanentemente na ilha. Uma casa premium não deve simplesmente permanecer fechada; deve manter-se supervisionada e visualmente cuidada.</p>

  <h2>Perfil das propriedades em São Vicente</h2>
  <p>Na região existem moradias contemporâneas, casas em encosta e imóveis com forte relação com a natureza circundante. Muitas destas propriedades são utilizadas apenas em determinados períodos, o que torna a continuidade do acompanhamento particularmente importante.</p>

  <p>O Property Care ajuda a preservar o estado geral da casa, a perceção de ordem e o nível de preparação esperado numa residência de padrão elevado.</p>

  <h2>Clima, humidade e acompanhamento visual</h2>
  <p>A costa norte da Madeira apresenta humidade superior, maior variabilidade meteorológica e influência mais forte do Atlântico. Em imóveis de luxo, estas condições exigem observação regular de acessos, superfícies, zonas exteriores e aspetos visíveis do imóvel.</p>

  <p>Uma supervisão consistente permite reconhecer cedo necessidades de intervenção, prevenir deterioração visual e manter a propriedade num nível adequado ao seu posicionamento.</p>

  <h2>Utilização sazonal e segunda residência</h2>
  <p>Muitos proprietários internacionais usam a casa em São Vicente como residência secundária ou local de estadias prolongadas em períodos específicos do ano. Entre essas utilizações, é essencial que a propriedade não fique sem controlo.</p>

  <p>O acompanhamento regular oferece segurança, clareza e uma base fiável para decisões rápidas sempre que surja algum ponto que exija atenção.</p>

  <h2>Serviço discreto para proprietários exigentes</h2>
  <p>Luxury Property Care em São Vicente é pensado para proprietários que valorizam discrição, fiabilidade e processos claros. O foco não está em gestão turística, mas sim na manutenção de um padrão residencial premium para imóveis privados na Madeira.</p>

  <p>Para mais informações visite a página Property Care. <a class="cta-link" href="/pt/home/">Saiba mais sobre Luxury Property Care</a>.</p>
</section>
""".strip(),

    "src/pt/locais/ribeira-brava/index.njk": """
<section class="text-intro">

  <div class="hero-logo hero-logo--small">
    <img src="/assets/images/logo.svg" alt="Anjo Cleaning Logo" width="720" height="220" loading="eager" decoding="async">
  </div>
  <h1>Luxury Property Care para imóveis de luxo em Ribeira Brava</h1>

  <p>Ribeira Brava ocupa uma posição estratégica na costa sul da Madeira e combina acessibilidade, clima mais estável e proximidade a várias zonas residenciais premium da ilha. Para proprietários internacionais, é uma localização particularmente prática para moradias e segundas residências.</p>

  <p>Ao mesmo tempo, também aqui a ausência prolongada do proprietário exige acompanhamento estruturado. Um imóvel de alto padrão deve manter apresentação, ordem e supervisão regular, mesmo quando não está ocupado.</p>

  <h2>Imóveis residenciais e padrão de uso</h2>
  <p>Em Ribeira Brava existem moradias modernas, casas com boa exposição solar e propriedades usadas tanto para estadias privadas como para presença sazonal ao longo do ano. Isso cria necessidades claras de continuidade entre períodos de utilização.</p>

  <p>O Property Care ajuda a garantir que a casa permaneça num estado compatível com o nível do imóvel e com as expectativas dos seus proprietários.</p>

  <h2>Vantagens e exigências da localização</h2>
  <p>A costa sul oferece maior previsibilidade climática do que o norte, mas isso não elimina a necessidade de controlo. Em casas premium, entradas, zonas exteriores, apresentação geral e detalhes visíveis continuam a exigir atenção regular.</p>

  <p>Uma abordagem estruturada permite identificar cedo pontos a observar, necessidade de apoio complementar e aspetos que devem ser tratados antes da próxima chegada dos proprietários.</p>

  <h2>Segurança operacional entre estadias</h2>
  <p>Quando a propriedade não é usada continuamente, torna-se importante haver um acompanhamento fiável e uma noção clara do estado geral do imóvel. Isso reduz incertezas e permite ao proprietário planear cada estadia com maior tranquilidade.</p>

  <p>Luxury Property Care oferece precisamente essa estabilidade: supervisão visual, estrutura e acompanhamento coerente para imóveis privados de nível elevado.</p>

  <h2>Serviço discreto para propriedades privadas</h2>
  <p>O nosso serviço em Ribeira Brava é orientado para discrição, consistência e respeito pelo carácter privado do imóvel. Não se trata de administração turística, mas de um padrão de acompanhamento pensado para residências premium na Madeira.</p>

  <p>Para mais informações visite a página Property Care. <a class="cta-link" href="/pt/home/">Saiba mais sobre Luxury Property Care</a>.</p>
</section>
""".strip(),
}

SECTION_RE = re.compile(
    r'<section class="text-intro">.*?</section>',
    re.DOTALL
)

def patch_file(rel_path: str, new_section: str) -> None:
    path = ROOT / rel_path
    if not path.exists():
        print(f"FEHLT: {rel_path}")
        return

    text = path.read_text(encoding="utf-8")

    if not SECTION_RE.search(text):
        print(f"KEIN text-intro BLOCK: {rel_path}")
        return

    new_text = SECTION_RE.sub(new_section, text, count=1)

    if new_text == text:
        print(f"SKIP: {rel_path}")
        return

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"OK: {rel_path}")

def main():
    for rel_path, new_section in PAGES.items():
        patch_file(rel_path, new_section)
    print("\\nFertig.")

if __name__ == "__main__":
    main()