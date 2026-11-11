# Registro de validação

Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva. Unilasalle-RJ,
Sistemas de Informação, Linguagem de Programação, 6º período, 2026.

## Ambiente e escopo

Validação local em 11/11/2026, Windows, Python 3.14.7, ambiente virtual exclusivo.
Versões estritas em `requirements.txt`; `pip check` sem conflitos.

## Evidências executadas

- Arquivo bruto preservado; SHA-256 verificado contra a proveniência.
- MD5 do XLSX conferido contra o manifesto interno.
- Base lida: 14.517 registros município/rede e 133 colunas.
- Recorte: 92 códigos municipais distintos, rede Municipal, RJ.
- Normalização: 1.012 linhas, 998 Idebs válidos, 14 ausentes; nenhuma imputação.
- Cobertura recalculada e compatível com a inspeção inicial da coleta.
- 998 combinações Ideb/P/N dentro da tolerância de arredondamento de 0,0501.
- Onze testes automatizados do pipeline aprovados, incluindo correlação com
  empates, rejeição de série constante e cobertura de metadados dos derivados.
- Notebook inteiro executado sem erro por `scripts/execute_notebook.py`.
- Reexecução do pipeline com hashes idênticos para os 23 produtos registrados
  em `reproducibilidade.json` (dados, tabelas, métricas, artigo e figuras).
- Resumo do artigo com 206 palavras; quatro figuras com texto alternativo;
  referências a arquivos locais e âncoras válidas.
- JavaScript verificado com `node --check docs/assets/app.js`.
- Artigo servido localmente com resposta HTTP 200.
- Quatro figuras estáticas inspecionadas visualmente a partir de renderizações
  PNG de conferência; eixos, legendas e rótulos legíveis.

## Fechamento das lacunas da revisão

- Entrada comparada byte a byte com download do endereço oficial do Inep via
  HTTP em 11/11/2026: 25.308.289 bytes iguais e SHA-256 coincidente. O protocolo
  e a ausência de autenticação TLS estão registrados em `proveniencia.json`.
- Reuso documentado em `data/LICENSE.md`: regime de livre utilização do art. 4º
  do Decreto nº 8.777/2016, conforme texto atualizado da Câmara, com atribuição
  e ressalva de direitos de terceiros. CC BY 4.0 para contribuições autorais;
  não se atribuiu uma licença CC ao ZIP original.
- Dicionário com todas as 31 colunas da tabela principal e cada variável dos
  quatro CSVs derivados e dois JSONs de métricas/validação. Tipos, unidades,
  granularidade, chaves e regras de cálculo documentados individualmente.
- Correlação dos 92 pares de Ideb 2023/2025: Pearson 0,826419 e Spearman
  0,828087, com empates tratados por postos médios e sem inferência causal.
- Conferência no Chrome em desktop e simulação móvel de 400 px: conteúdo
  responsivo, figura e interação do Plotly examinados. Simulação não equivale
  a teste físico em todos os modelos de telefone.
- Na versão final local, os gráficos de distribuição, comparação e componentes
  carregaram no Plotly. A evolução foi examinada na revisão anterior em desktop
  e em 400 px; a faixa interquartil recebeu modo de linhas explícito nesta
  revisão. O controle de interface encerrou a sessão por não conseguir confirmar
  a URL atual; não foram emitidas novas ações de navegador após esse bloqueio.

## Matriz de atendimento ao enunciado

| Item solicitado | Evidência no projeto |
|---|---|
| Repositório público e árvore de diretórios | GitHub, data, notebooks, src e docs |
| README abrangente, resumo e palavras-chave | README.md |
| Dupla, instituição, curso, disciplina e período | README, artigo e notebook; Unilasalle-RJ, 6º período, 2026 |
| Fonte primária e aquisição sem credencial paga | Catálogo Inep, ZIP preservado, src/etl.py e scripts/verify_official_source.py |
| Ambiente reproduzível e versões congeladas | Python 3.14.7, 49 dependências pinadas e workflow de validação |
| Licenças e condições de reuso | LICENSE, LICENSE-CONTENT.md e data/LICENSE.md |
| Dicionário de cada variável | data/data_dictionary.md e src/metadata.py |
| Persistência aberta dos dados tratados | CSV.gz, CSV e JSON em data/processed |
| Pipeline com tratamento de tipos e ausências | src/etl.py, marcadores originais e testes |
| Rastreabilidade e preservação da entrada | ZIP íntegro, proveniência, hashes e nenhuma imputação |
| Notebook de exploração | notebooks/analise_exploratoria.ipynb, executado integralmente |
| Estatística, dispersão, extremos e correlações | src/analysis.py, notebook e tabelas derivadas |
| Gráficos coerentes com as perguntas | Quatro SVGs e quatro versões Plotly |
| Artigo com resumo de 150 a 250 palavras e 4 a 6 palavras-chave | 206 palavras e seis palavras-chave |
| Duas a três perguntas explícitas | RQ1, RQ2 e RQ3 na introdução |
| Metodologia, fonte, granularidade e trecho de código | Seção 2 do artigo |
| Resultados e discussão respondendo às perguntas | Seção 3, tabelas e gráficos calculados |
| Conclusão, limitações e trabalhos futuros | Seção 4 |
| Declaração FAIR e comandos de reprodução | Seção 5 |
| Fontes oficiais, bibliotecas e referência científica | Seção 6, referências em estrutura ABNT |
| Deploy público e layout responsivo | GitHub Pages, branch main, pasta docs; conferência no Chrome |

## Limites metodológicos e de homologação

- PDFs metodológicos complementares não integram a coleta; as notas internas
  da planilha foram preservadas.
- Ambiente diferente de Windows/Python 3.14: não homologado.
- Autoria acadêmica identifica o ano de 2026 e o 6º período informado pela dupla.
- O estudo é descritivo e municipal; não estima efeitos causais ou desigualdade
  individual. Cumprimento dos itens não predetermina a nota atribuída pelo docente.

## Publicação

Repositório e pasta de publicação: `pedro-art2611/Projeto-Pr-ticoG2`, branch
`main`, `/docs`. GitHub Pages ativado e build confirmado como `built` em
11/11/2026; URL pública respondeu HTTP 200.

Artigo: https://pedro-art2611.github.io/Projeto-Pr-ticoG2/

O commit de implementação `3580f230318f69500ba1fc42e6a83253e5352a88` passou
também na instalação em ambiente novo do GitHub Actions (Windows/Python 3.14.7):
dependências, oito testes, reprodução por hashes, artigo e notebook.

As ampliações posteriores têm onze testes e novos produtos. O histórico do
workflow abaixo registra a validação independente da revisão vigente.

- [Validação independente no CI](https://github.com/pedro-art2611/Projeto-Pr-ticoG2/actions/runs/43079306668)
- [Publicação concluída](https://github.com/pedro-art2611/Projeto-Pr-ticoG2/actions/runs/43081572476)
- [Histórico de validação da versão vigente](https://github.com/pedro-art2611/Projeto-Pr-ticoG2/actions/workflows/validacao.yml)
