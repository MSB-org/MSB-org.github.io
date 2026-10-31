# Site do Movimento Sociocientífico Brasileiro (MSB)

Site de apresentação do MSB. HTML, CSS e um único script de menu, sem etapa de build obrigatória no navegador e sem serviços externos (as fontes são hospedadas aqui). Pronto para o GitHub Pages e também funciona abrindo os arquivos direto do disco.

## Páginas

- **Início**: nome completo do movimento, o que faz, prévia do observatório, estatuto e como participar.
- **Soberania**: quadro com 19 setores (15 digitais e 4 ainda em levantamento), cada um com o que já existe no Brasil, alternativas livres, o que falta, obstáculos de adoção, o que pode ser feito e fontes.
- **Estatuto**: a minuta de outubro de 2026, em texto e em PDF, com aviso de que está em debate.
- **Participar**: Discord, GitHub e formas de contribuir.

## Como atualizar

As páginas são **geradas** a partir de arquivos em `data/`. Edite os dados e rode o gerador:

```bash
python3 tools/build.py      # só usa a biblioteca padrão do Python
```

| O que | Onde |
|---|---|
| Setores, itens, lacunas, classificações e fontes | `data/setores.json` |
| Texto da minuta do estatuto | `data/estatuto.json` |
| Links do Discord, GitHub e PDF | `data/links.json` |
| Textos da página inicial, de participar e modelos de página | `tools/build.py` |
| Aparência | `css/style.css` |

Os arquivos `.html` na raiz são resultado do gerador; não edite à mão, pois serão sobrescritos. Para ver o site: `python3 -m http.server 8000` ou abra `index.html` direto.

## Regras do observatório

- Classificações **qualitativas** (Consolidado, Funcional, Em desenvolvimento, Lacuna importante, Dados insuficientes) em quatro dimensões: disponibilidade, maturidade, adoção e autonomia. **Não há percentuais.** Só entrarão com metodologia, critérios e dados publicados.
- Avaliação editorial do MSB e estatística oficial ficam separadas ("Dados oficiais", com fonte e ano).
- Cada item informa **origem** (brasileiro, internacional ou misto), **situação** (em operação, em estruturação, em revisão, substituído, não verificada) e **de onde veio a informação**: README do MSB, fonte citada (com data de consulta) ou "ainda não verificado pelo MSB".
- Pesquisa de 31/10/2026. Os endereços foram testados nessa data; alguns sites (IBGE, OCDE, Moodle) recusam acesso automatizado e não puderam ser testados por script.
- Itens "ainda não verificados" (licenças de Linux, LibreOffice, Nextcloud, Matrix, Moodle etc., e o endereço do VLibras e do OpenStreetMap) precisam de conferência antes de a marca sair.

## Publicar no GitHub Pages

Todos os caminhos são relativos. Em Settings, Pages, escolha a branch `main` e a pasta `/ (root)`.

## Pendências

- **Licença**: ainda não definida. Pelo `LICENSING.md` da organização, código costuma usar MIT, GPL, AGPL ou Apache, e texto usa CC BY ou CC BY-SA. O texto do estatuto é do movimento e não deve receber licença sem decisão coletiva.
- **Endereço do site**: definir o domínio para acrescentar `og:image`, `canonical` e `sitemap.xml`.
- **Próximas versões**: catálogo de tecnologias com filtros, gráficos da educação, área de projetos ligada ao GitHub e materiais didáticos.

## Créditos

Fontes: Roboto (títulos), Open Sans (texto) e Carlito (interface; é a versão livre, com as mesmas métricas, do Calibri, que é proprietário e por isso não está incluído). Todas sob SIL Open Font License 1.1, com os textos em `assets/fonts/`. Ícones do Discord e do GitHub: Simple Icons (CC0). Emblema do MSB: original da organização.
