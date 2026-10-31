#!/usr/bin/env python3
"""Gera as páginas HTML do site a partir dos dados em data/.

    python3 tools/build.py

Fontes de verdade:
    data/setores.json   observatório da soberania
    data/estatuto.json  minuta do estatuto
    data/links.json     Discord, GitHub e PDF do estatuto

Só usa a biblioteca padrão. As páginas geradas funcionam sem JavaScript
(abrindo direto do disco ou no GitHub Pages); o JS só abre o menu no celular.
"""
import json
import pathlib
import html

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DADOS = RAIZ / "data"
esc = html.escape


def carregar(nome):
    return json.loads((DADOS / nome).read_text(encoding="utf-8"))


LINKS = carregar("links.json")
SETORES = carregar("setores.json")
ESTATUTO = carregar("estatuto.json")
META = SETORES["meta"]
LISTA = SETORES["setores"]


def data_br(iso):
    a, m, d = iso.split("-")
    return f"{d}/{m}/{a}"


def icone(nome):
    """Lê o <path> de um ícone em assets/icons/ e devolve um SVG inline."""
    svg = (RAIZ / "assets" / "icons" / f"{nome}.svg").read_text(encoding="utf-8")
    d = svg.split(' d="', 1)[1].split('"', 1)[0]
    return f'<svg class="icone" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{d}"/></svg>'


NAV = [("index.html", "Início"), ("soberania.html", "Soberania"), ("estatuto.html", "Estatuto"), ("participar.html", "Participar")]


# ------------------------------------------------------------------ peças reutilizáveis
def pagina(arquivo, titulo, descricao, corpo, noindex=False):
    nav = "\n".join(
        f'          <li><a href="{h}"{" aria-current=\"page\"" if h == arquivo else ""}>{t}</a></li>' for h, t in NAV)
    robots = '  <meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(titulo)}</title>
  <meta name="description" content="{esc(descricao)}">
  <meta name="theme-color" content="#0b3b3f">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Movimento Sociocientífico Brasileiro">
  <meta property="og:title" content="{esc(titulo)}">
  <meta property="og:description" content="{esc(descricao)}">
  <meta name="twitter:card" content="summary">
{robots}  <link rel="icon" type="image/png" href="assets/favicon.png">
  <link rel="preload" href="assets/fonts/roboto-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/open-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <a class="pular" href="#conteudo">Pular para o conteúdo</a>
  <header class="topo">
    <div class="contem topo-linha">
      <a class="marca" href="index.html" aria-label="Movimento Sociocientífico Brasileiro, página inicial">
        <img src="assets/logo-128.png" alt="" width="56" height="56">
        <span class="marca-nome">MSB</span>
      </a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
      <nav id="nav" class="nav" aria-label="Principal">
        <ul>
{nav}
        </ul>
        <div class="nav-acoes">
          <a class="btn btn-ouro btn-discord" href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">{icone('discord')}Entrar no Discord</a>
          <a class="btn btn-claro btn-discord" href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">{icone('github')}GitHub</a>
        </div>
      </nav>
    </div>
  </header>

  <main id="conteudo">
{corpo}
  </main>

  <footer class="rodape">
    <div class="contem rodape-grade">
      <div>
        <p class="rodape-nome">Movimento Sociocientífico Brasileiro</p>
        <p>Ciência, sociedade e soberania. Um movimento em formação, de participação aberta. O conteúdo deste site está em revisão e cada informação mostra sua fonte.</p>
      </div>
      <nav aria-label="Rodapé">
        <p class="rodape-titulo">Navegar</p>
        <ul>
{chr(10).join(f'          <li><a href="{h}">{t}</a></li>' for h, t in NAV)}
        </ul>
      </nav>
      <div>
        <p class="rodape-titulo">Fale com a gente</p>
        <ul>
          <li><a href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">Discord</a></li>
          <li><a href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">GitHub</a></li>
          <li><a href="{LINKS['estatuto_pdf']}" data-link="estatuto_pdf">Minuta do estatuto (PDF)</a></li>
        </ul>
      </div>
    </div>
  </footer>
  <script src="js/site.js" defer></script>
</body>
</html>
"""


def chip(nivel_id, dim_nome=None):
    n = META["niveis"].get(nivel_id, META["niveis"]["sem_dados"])
    barras = "".join(f'<i class="{"cheia" if i <= n["barras"] else ""}"></i>' for i in range(1, 5))
    rotulo = f"<b>{esc(dim_nome)}</b> {esc(n['nome'])}" if dim_nome else esc(n["nome"])
    return f'<span class="nivel" data-nivel="{esc(nivel_id)}"><span class="barras" aria-hidden="true">{barras}</span><span>{rotulo}</span></span>'


def chips(setor):
    return "".join(chip(setor["avaliacao"][d]["nivel"], META["dimensoes"][d]["nome"]) for d in META["dimensoes"])


def atrib(url):
    return f' href="{esc(url)}"' + (' rel="noopener noreferrer"' if url.startswith("http") else "")


# ------------------------------------------------------------------ INÍCIO
# Órbitas translúcidas que cruzam o banner inteiro (decorativas, misturadas ao fundo).
ORBITAS = """<svg class="orbitas-banner" viewBox="0 0 1600 760" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
        <defs>
          <linearGradient id="g-ouro" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#f2b53d" stop-opacity="0"/><stop offset="0.45" stop-color="#f2b53d" stop-opacity="0.5"/><stop offset="1" stop-color="#f2b53d" stop-opacity="0.05"/></linearGradient>
          <linearGradient id="g-agua" x1="1" x2="0" y1="0" y2="0"><stop offset="0" stop-color="#4fc3c3" stop-opacity="0"/><stop offset="0.5" stop-color="#4fc3c3" stop-opacity="0.45"/><stop offset="1" stop-color="#4fc3c3" stop-opacity="0.04"/></linearGradient>
        </defs>
        <g class="d1"><ellipse pathLength="1" cx="1120" cy="360" rx="800" ry="250" transform="rotate(-22 1120 360)" stroke="url(#g-ouro)" stroke-width="34"/></g>
        <g class="d2"><ellipse pathLength="1" cx="1080" cy="380" rx="740" ry="190" transform="rotate(27 1080 380)" stroke="url(#g-agua)" stroke-width="22"/></g>
        <g class="d3"><ellipse pathLength="1" cx="360" cy="640" rx="980" ry="210" transform="rotate(-9 360 640)" stroke="url(#g-ouro)" stroke-width="9"/></g>
        <g class="d4"><ellipse pathLength="1" cx="760" cy="90" rx="1150" ry="250" transform="rotate(10 760 90)" stroke="url(#g-agua)" stroke-width="5"/></g>
      </svg>"""


def pagina_inicio():
    destaques = [s for s in LISTA if s["destaque"]]
    n_itens = sum(len(s["existe"]) + len(s["livres"]) for s in LISTA)
    n_lac = sum(len(s["falta"]) for s in LISTA)
    quadro = "\n".join(
        f'          <li><a href="soberania.html#{s["id"]}"><span class="quadro-nome">{esc(s["nome"])}</span><span class="chips">{chips(s)}</span></a></li>'
        for s in destaques)
    dims = "".join(
        f'<div><dt>{esc(d["nome"])}</dt><dd>{esc(d["pergunta"])}</dd></div>' for d in META["dimensoes"].values())
    return f"""    <section class="heroi">
      {ORBITAS}
      <div class="contem heroi-grade">
        <div class="heroi-texto">
          <h1>Movimento Sociocientífico Brasileiro <span class="sigla">(MSB)</span></h1>
          <p class="lema">Ciência, sociedade e soberania.</p>
          <p class="lide">Um movimento popular que reúne gente de todas as áreas para estudar os problemas do país, produzir conhecimento aberto e fazer coisas concretas com ele: ensinar, pesquisar, desenvolver e adotar software livre, e levar propostas ao debate público. Está em formação e é aberto a quem quiser participar.</p>
          <div class="acoes">
            <a class="btn btn-ouro btn-discord" href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">{icone('discord')}Entrar no Discord</a>
            <a class="btn btn-claro btn-discord" href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">{icone('github')}Ver o GitHub</a>
            <div class="acoes-links">
              <a class="link-claro" href="soberania.html">Ver o panorama da soberania</a>
              <a class="link-claro" href="estatuto.html">Ler a minuta do estatuto</a>
            </div>
          </div>
        </div>
        <div class="heroi-emblema">
          <picture>
            <source srcset="assets/logo-640.webp" type="image/webp">
            <img src="assets/logo-640.png" width="640" height="640" alt="Emblema do MSB: um lobo-guará sobre um livro aberto, diante do globo terrestre">
          </picture>
        </div>
      </div>
    </section>

    <section class="secao" id="movimento">
      <div class="contem duas-colunas">
        <p class="afirmacao">A ciência não pertence só aos laboratórios, nem entender a sociedade é tarefa só da universidade.</p>
        <div class="texto-corrido">
          <p>O Movimento Sociocientífico Brasileiro (MSB) é uma iniciativa popular voltada à educação, à circulação do conhecimento, à soberania brasileira e à participação da sociedade nas decisões que envolvem ciência e tecnologia.</p>
          <p>História, Filosofia, Sociologia, Geografia, Economia, Biologia, Física, Química, Matemática, Computação, Saúde, Engenharias e outras áreas se encontram na vida de todo dia. Por isso o movimento junta Ciências Humanas e Sociais, Ciências da Natureza e conhecimentos técnicos, sem hierarquia de prestígio entre elas.</p>
          <p>Não se exige diploma, profissão nem experiência com programação. Quem pesquisa, ensina, programa, traduz, escreve, desenha ou organiza tem lugar.</p>
        </div>
      </div>
    </section>

    <section class="secao gelo" id="por-que" aria-labelledby="t-porque">
      <div class="contem">
        <h2 id="t-porque">Por que sociocientífico e não apenas científico?</h2>
        <div class="comparacao">
          <div class="so-cientifico">
            <h3>Só “científico” costuma sugerir</h3>
            <ul>
              <li>laboratório e Ciências da Natureza;</li>
              <li>conhecimento que vai de quem sabe para quem não sabe;</li>
              <li>ciência como assunto de especialistas.</li>
            </ul>
          </div>
          <div class="sociocientifico">
            <h3>“Sociocientífico”, para o MSB, é</h3>
            <ul>
              <li><b>Ciência de todas as áreas.</b> Ciências Humanas e Sociais e Ciências da Natureza juntas, sem hierarquia de prestígio.</li>
              <li><b>Conhecimento que também vem da população.</b> Reconhecer e valorizar as experiências e as perguntas das pessoas.</li>
              <li><b>Ciência como bem social.</b> Ligada à educação, a projetos concretos e às decisões públicas, com rigor e abertura à crítica (Art. 7º).</li>
            </ul>
          </div>
        </div>
        <p><a href="estatuto.html#preambulo">Ler o preâmbulo da minuta do estatuto</a></p>
      </div>
    </section>

    <section class="secao" id="frentes" aria-labelledby="t-frentes">
      <div class="contem">
        <h2 id="t-frentes">O que o movimento faz</h2>
        <div class="frentes-grade">
          <article><h3>Educação e materiais abertos</h3><p>Apostilas, sequências didáticas, vídeos, simuladores, oficinas e cursos introdutórios, inclusive de programação e ciência de dados, com licenças que permitem reutilizar.</p></article>
          <article><h3>Pesquisa aberta e integridade científica</h3><p>Estudos reproduzíveis, ciência cidadã e cuidado com possíveis irregularidades, sem confundir erro, divergência de método e fraude comprovada.</p></article>
          <article><h3>Combate à desinformação</h3><p>Alfabetização midiática, checagem e métodos verificáveis, como educação e participação social.</p></article>
          <article><h3>Software livre, principalmente em uso</h3><p>Criar quando for preciso, mas sobretudo fazer as alternativas que já existem serem conhecidas, instaladas, traduzidas, ensinadas e mantidas.</p></article>
          <article><h3>Soberania</h3><p>Científica, tecnológica, digital, produtiva e cultural. Não é isolamento: cooperação internacional combina com capacidade brasileira.</p></article>
          <article><h3>Projetos sociais e políticas públicas</h3><p>Ações com escolas, comunidades e bibliotecas, e propostas fundamentadas para o debate público.</p></article>
        </div>
      </div>
    </section>

    <section class="secao gelo" id="observatorio">
      <div class="contem">
        <h2>Disponível não é o mesmo que usado</h2>
        <p class="medida">Muita tecnologia livre já existe e segue sem uso. Uma alternativa que ninguém conhece, ou que ninguém consegue instalar, não diminui a dependência de ninguém. Por isso o observatório do MSB olha, em cada setor, para quatro coisas:</p>
        <dl class="dimensoes">{dims}</dl>
        <ul class="quadro">
{quadro}
        </ul>
        <p class="medida">São {len(LISTA)} setores, com {n_itens} tecnologias e instituições listadas e {n_lac} lacunas apontadas, cada uma com fonte. Não há percentuais: as classificações são qualitativas, e o que ainda não foi levantado aparece como "dados insuficientes". Versão {esc(META['versao'])}, em revisão.</p>
        <div class="acoes"><a class="btn btn-ouro" href="soberania.html">Ver todos os setores</a></div>
      </div>
    </section>

    <section class="secao" id="estatuto">
      <div class="contem">
        <h2>A minuta do estatuto está aberta ao debate</h2>
        <p class="medida">Define princípios, participação aberta a qualquer pessoa e uma coordenação colegiada, sem presidência unipessoal. Ainda não é um estatuto aprovado: é uma versão de outubro de 2026 para discussão e deliberação coletiva.</p>
        <div class="acoes">
          <a class="btn btn-mar" href="estatuto.html">Ler no site</a>
          <a class="btn btn-contorno-mar" href="{LINKS['estatuto_pdf']}" data-link="estatuto_pdf">Baixar o PDF</a>
        </div>
      </div>
    </section>

    <section class="secao gelo" id="participar">
      <div class="contem">
        <h2>Dois lugares para começar</h2>
        <div class="duas-colunas separadas">
          <div>
            <h3>{icone('discord')}Discord, para conversar e organizar</h3>
            <p>Dúvidas, debates, oficinas, grupos de estudo e a articulação dos projetos. Ao entrar, leia as regras, escolha seus interesses e se apresente.</p>
            <div class="acoes"><a class="btn btn-mar btn-discord" href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">{icone('discord')}Entrar no Discord</a></div>
          </div>
          <div>
            <h3>{icone('github')}GitHub, para código, pesquisa e materiais</h3>
            <p>Software livre, estudos reproduzíveis e material didático com licença aberta. Uma primeira contribuição pode ser corrigir um trecho de documentação.</p>
            <div class="acoes"><a class="btn btn-contorno-mar btn-discord" href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">{icone('github')}Ver o GitHub</a><a class="link-escuro" href="participar.html">Como contribuir</a></div>
          </div>
        </div>
      </div>
    </section>"""


# ------------------------------------------------------------------ SOBERANIA
def tags_item(i):
    origem = META["origens"][i["origem"]]
    situ = META["situacoes"][i["situacao"]]
    return (f'<span class="tag t-{esc(i["origem"])}">{esc(origem)}</span>'
            f'<span class="tag t-situ" data-situ="{esc(i["situacao"])}">{esc(situ)}</span>'
            f'<span class="tag t-tipo">{esc(i["tipo"])}</span>')


def item(i):
    ver = META["verificacao"][i["verificacao"]]
    ref = ""
    if i.get("ref"):
        ref = f' <a class="ref"{atrib(i["ref"]["url"])}>{esc(i["ref"]["titulo"])}</a>'
    return f"""            <li class="item">
              <div class="item-topo"><a class="item-nome"{atrib(i['url'])}>{esc(i['nome'])}</a><span class="tags">{tags_item(i)}</span></div>
              <p>{esc(i['nota'])}</p>
              <p class="item-fonte" data-verif="{esc(i['verificacao'])}">{esc(ver)}.{ref}</p>
            </li>"""


def lista_itens(titulo, itens):
    if not itens:
        return ""
    return f'          <h4>{esc(titulo)}</h4>\n          <ul class="itens">\n' + "\n".join(item(i) for i in itens) + "\n          </ul>"


def bullets(titulo, textos, classe=""):
    if not textos:
        return ""
    return f'          <h4>{esc(titulo)}</h4>\n          <ul class="pontos {classe}">\n' + "\n".join(f"            <li>{esc(t)}</li>" for t in textos) + "\n          </ul>"


def setor_html(s):
    achados = "".join(
        f'<aside class="achado"><p>{esc(a["texto"])}</p><p class="item-fonte"><a class="ref"{atrib(a["ref"]["url"])}>{esc(a["ref"]["titulo"])}</a></p></aside>'
        for a in s.get("achados", []))
    indic = ""
    if s["indicadores"]:
        indic = '          <h4>Dados oficiais</h4>\n          <dl class="indicadores">\n' + "\n".join(
            f'            <div><dt>{esc(x["valor"])}</dt><dd>{esc(x["rotulo"])}<br><a class="ref"{atrib(x["url"])}>{esc(x["referencia"])}</a></dd></div>'
            for x in s["indicadores"]) + "\n          </dl>"
    just = "".join(
        f'<li>{chip(s["avaliacao"][d]["nivel"], META["dimensoes"][d]["nome"])}<span class="just">{esc(s["avaliacao"][d]["nota"])}</span></li>'
        for d in META["dimensoes"])
    fontes = "".join(f'<li><a{atrib(f["url"])}>{esc(f["titulo"])}</a></li>' for f in s["fontes"])
    esquerda = "\n".join(x for x in [
        lista_itens("Já existe no Brasil", s["existe"]),
        lista_itens("Alternativas livres disponíveis", s["livres"]),
    ] if x) or '          <h4>Já existe no Brasil</h4>\n          <p class="vazio">Ainda não levantado pelo MSB.</p>'
    direita = "\n".join(x for x in [
        bullets("Ainda não existe ou falta", s["falta"], "lacunas"),
        achados and f'          <h4>O que a pesquisa encontrou</h4>{achados}',
        bullets("Por que a adoção importa aqui", s["adocao"]),
        bullets("O que pode ser feito (em debate)", s["fazer"]),
        indic,
    ] if x)
    return f"""      <section class="setor" id="{esc(s['id'])}" aria-labelledby="h-{esc(s['id'])}">
        <header class="setor-topo">
          <h3 id="h-{esc(s['id'])}">{esc(s['nome'])}</h3>
          <div class="chips">{chips(s)}</div>
        </header>
        <p class="setor-resumo">{esc(s['resumo'])}</p>
        <div class="setor-corpo">
          <div class="col-itens">
{esquerda}
          </div>
          <div class="col-lacunas">
{direita}
          </div>
        </div>
        <details class="mais">
          <summary>Por que essa classificação, e quais as fontes</summary>
          <p>{esc(s['importancia'])}</p>
          <ul class="justificativas">{just}</ul>
          <p class="aviso">{esc(META['tipo_avaliacao'])} Avaliado em {esc(META['avaliado_em'])}.</p>
          <h4>Fontes</h4>
          <ul class="pontos">{fontes}</ul>
        </details>
      </section>"""


def pagina_soberania():
    grupos_html, indice = [], []
    for g in META["grupos"]:
        do_grupo = [s for s in LISTA if s["grupo"] == g["id"]]
        indice.append(
            f'<div><h3>{esc(g["nome"])}</h3><ul>' + "".join(f'<li><a href="#{s["id"]}">{esc(s["nome"])}</a></li>' for s in do_grupo) + "</ul></div>")
        grupos_html.append(
            f'    <section class="grupo" id="g-{g["id"]}" aria-labelledby="hg-{g["id"]}">\n      <div class="contem">\n'
            f'        <h2 id="hg-{g["id"]}">{esc(g["nome"])}</h2>\n        <p class="grupo-desc">{esc(g["descricao"])}</p>\n'
            + "\n".join(setor_html(s) for s in do_grupo) + "\n      </div>\n    </section>")
    dims = "".join(f'<div><dt>{esc(d["nome"])}</dt><dd>{esc(d["pergunta"])}</dd></div>' for d in META["dimensoes"].values())
    niveis = "".join(f'<li>{chip(k)}</li>' for k in META["niveis"])
    situ = "".join(f'<li><span class="tag t-situ" data-situ="{k}">{esc(v)}</span></li>' for k, v in META["situacoes"].items())
    return f"""    <section class="cabeca-pagina">
      <div class="contem">
        <h1>Panorama da soberania brasileira</h1>
        <p class="lide">O que o Brasil já tem, o que usa de fato e o que ainda precisa desenvolver, setor por setor. Soberania não é isolamento: envolve poder decidir, operar e evoluir as tecnologias de que dependemos. Uma tecnologia estrangeira de código aberto não passa a ser brasileira por ser usada aqui, mas pode contribuir para a nossa autonomia quando podemos usá-la, hospedá-la, adaptá-la e mantê-la.</p>
      </div>
    </section>

    <section class="como-ler">
      <div class="contem">
        <h2>Como ler</h2>
        <dl class="dimensoes">{dims}</dl>
        <div class="legendas">
          <div><h3>Classificação</h3><ul class="lista-legenda">{niveis}</ul></div>
          <div><h3>Situação de cada item</h3><ul class="lista-legenda">{situ}</ul></div>
          <div><h3>Origem</h3><ul class="lista-legenda"><li><span class="tag t-brasil">Brasileiro</span></li><li><span class="tag t-internacional">Internacional</span></li><li><span class="tag t-misto">Misto</span></li></ul></div>
        </div>
        <p class="medida">{esc(META['metodologia'])} Cada item mostra se a informação veio do README do MSB, de uma fonte citada (consultada em {esc(data_br(META['consultado_em']))}) ou se ainda não foi verificada. Para corrigir ou ampliar, abra uma Issue no <a href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">GitHub</a> ou converse no <a href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">Discord</a>. Os dados ficam em <a href="data/setores.json">data/setores.json</a>.</p>
      </div>
    </section>

    <nav class="indice-setores" aria-label="Setores">
      <div class="contem indice-grade">
        {"".join(indice)}
      </div>
    </nav>

{chr(10).join(grupos_html)}"""


# ------------------------------------------------------------------ ESTATUTO
def pagina_estatuto():
    indice = '<li><a href="#preambulo">Preâmbulo</a></li>' + "".join(
        f'<li><a href="#{c["id"]}">{esc(c["numero"])} — {esc(c["titulo"])}</a></li>' for c in ESTATUTO["capitulos"])
    corpo = ['<h2 id="preambulo">Preâmbulo</h2>', '<div class="preambulo">' + "".join(f"<p>{esc(p)}</p>" for p in ESTATUTO["preambulo"]) + "</div>"]
    for c in ESTATUTO["capitulos"]:
        corpo.append(f'<h2 id="{c["id"]}">{esc(c["numero"])} — {esc(c["titulo"])}</h2>')
        corpo += [f'<p class="artigo" id="art-{a["n"]}"><b>Art. {a["n"]}º</b> {esc(a["texto"])}</p>' for a in c["artigos"]]
    return f"""    <section class="cabeca-pagina">
      <div class="contem">
        <h1>{esc(ESTATUTO['titulo'])}</h1>
        <div class="faixa-minuta" role="note">
          <strong>Esta é uma minuta em revisão, não um estatuto aprovado.</strong>
          <p>Versão de outubro de 2026, aberta ao debate e à deliberação coletiva. O próprio texto prevê que pode ser discutido e alterado (Art. 31) e que o MSB ainda não é uma associação civil registrada (Art. 32).</p>
          <div class="acoes">
            <a class="btn btn-mar" href="{LINKS['estatuto_pdf']}" data-link="estatuto_pdf">Baixar o PDF (7 páginas)</a>
            <a class="btn btn-contorno-mar btn-discord" href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">{icone('discord')}Debater no Discord</a>
          </div>
        </div>
      </div>
    </section>
    <section class="secao estatuto">
      <div class="contem">
        <p class="medida">O texto abaixo reproduz a minuta em PDF. Se houver diferença, vale o PDF. Cada artigo tem um endereço próprio, como <a href="#art-12">Art. 12</a>, que pode ser compartilhado.</p>
        <nav aria-label="Índice da minuta"><ul class="indice">{indice}</ul></nav>
{chr(10).join(corpo)}
      </div>
    </section>"""


# ------------------------------------------------------------------ PARTICIPAR
def pagina_participar():
    return f"""    <section class="cabeca-pagina">
      <div class="contem">
        <h1>Como participar</h1>
        <p class="lide">A participação é aberta a quem se interessa pelos princípios do movimento, independentemente de escolaridade, profissão, origem ou experiência. Escolha por onde começar.</p>
      </div>
    </section>
    <section class="secao">
      <div class="contem duas-colunas separadas">
        <div>
          <h2>{icone('discord')}Discord</h2>
          <p>É onde a conversa acontece: dúvidas de qualquer área, debates, oficinas, grupos de estudo, apresentação de propostas e a organização dos projetos. Ao entrar:</p>
          <ol class="pontos">
            <li>leia as regras e aceite;</li>
            <li>escolha seus interesses em "Canais e Cargos";</li>
            <li>apresente-se e procure um projeto com a tag "Busca colaboradores".</li>
          </ol>
          <div class="acoes"><a class="btn btn-mar btn-discord" href="{LINKS['discord']}" data-link="discord" rel="noopener noreferrer">{icone('discord')}Entrar no Discord</a></div>
          <p class="suave">Suspeita de irregularidade em pesquisa? Há um canal reservado no Discord para relatos. Eles são analisados com evidências, com direito de resposta, e encaminhados às instâncias competentes antes de qualquer parecer público.</p>
        </div>
        <div>
          <h2>{icone('github')}GitHub</h2>
          <p>Software livre, pesquisas reproduzíveis, materiais didáticos abertos e documentação, sempre com licença identificada. Procure uma Issue pequena, como <code>good first issue</code>, ou descreva um problema e proponha uma solução.</p>
          <div class="acoes"><a class="btn btn-contorno-mar btn-discord" href="{LINKS['github']}" data-link="github" rel="noopener noreferrer">{icone('github')}Ver o GitHub do MSB</a></div>
          <p class="suave">Mudanças entram por Pull Request. O guia de contribuição, o código de conduta e os padrões de pesquisa aberta estão nos documentos da organização.</p>
        </div>
      </div>
    </section>
    <section class="secao gelo">
      <div class="contem">
        <h2>O que dá para fazer, com ou sem programar</h2>
        <ul class="pontos medida">
          <li><b>Software:</b> funcionalidades, correção de erros, testes, documentação, acessibilidade, tradução e desempenho.</li>
          <li><b>Pesquisa:</b> revisão de literatura, replicação de resultados, análise de dados, ferramentas científicas e visualizações.</li>
          <li><b>Educação:</b> tutoriais, roteiros de oficinas, exemplos reproduzíveis e materiais de Ciências Humanas e Naturais.</li>
          <li><b>Adoção:</b> guias de instalação e migração, relatos de implantação em escolas e organizações, treinamento de quem vai usar.</li>
          <li><b>Observatório:</b> ajudar a levantar os setores ainda sem dados, como energia, saúde e medicamentos, indústria e agricultura.</li>
        </ul>
        <p class="medida">Português é o idioma padrão de acolhimento. Pergunta de iniciante é bem-vinda, e contribuição é avaliada pelo conteúdo, não por diploma.</p>
        <div class="acoes"><a class="btn btn-mar" href="soberania.html">Ver o observatório</a><a class="link-escuro" href="estatuto.html">Ler a minuta do estatuto</a></div>
      </div>
    </section>"""


def pagina_404():
    return """    <section class="cabeca-pagina">
      <div class="contem">
        <h1>Página não encontrada</h1>
        <p class="lide">O endereço não existe ou mudou de lugar.</p>
        <div class="acoes"><a class="btn btn-mar" href="index.html">Voltar ao início</a></div>
      </div>
    </section>"""


PAGINAS = {
    "index.html": pagina("index.html", "Movimento Sociocientífico Brasileiro", "Ciência, sociedade e soberania. Um movimento popular que reúne gente de todas as áreas para produzir conhecimento aberto, ensinar, pesquisar e adotar software livre.", pagina_inicio()),
    "soberania.html": pagina("soberania.html", "Panorama da soberania brasileira, Movimento Sociocientífico Brasileiro", "O que o Brasil já tem, o que usa de fato e o que ainda precisa desenvolver em infraestrutura e plataformas digitais, setor por setor, com fontes.", pagina_soberania()),
    "estatuto.html": pagina("estatuto.html", "Minuta de Estatuto (em debate), Movimento Sociocientífico Brasileiro", "Minuta de estatuto do Movimento Sociocientífico Brasileiro, versão de outubro de 2026, em debate e deliberação coletiva. Não é um documento aprovado.", pagina_estatuto()),
    "participar.html": pagina("participar.html", "Como participar, Movimento Sociocientífico Brasileiro", "Entre no Discord, contribua no GitHub e ajude a construir o observatório da soberania. Participação aberta, com ou sem diploma.", pagina_participar()),
    "404.html": pagina("404.html", "Página não encontrada, Movimento Sociocientífico Brasileiro", "Página não encontrada.", pagina_404(), noindex=True),
}

if __name__ == "__main__":
    for nome, conteudo in PAGINAS.items():
        (RAIZ / nome).write_text(conteudo, encoding="utf-8")
        print("gerado", nome, f"{len(conteudo) // 1024} KB")
