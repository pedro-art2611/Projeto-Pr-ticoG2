# Ideb nas redes municipais do Rio de Janeiro: 2005 a 2025

**Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva**<br>
Unilasalle-RJ · Bacharelado em Sistemas de Informação · 6º período · 2026<br>
Linguagem de Programação: Análise e Visualização de Dados com Python

![Python 3.14](https://img.shields.io/badge/Python-3.14-blue)
![Código MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-green)
![Texto CC BY 4.0](https://img.shields.io/badge/texto-CC_BY_4.0-blue)

Estudo descritivo reproduzível do Ideb dos anos iniciais nas redes municipais dos
92 municípios fluminenses. Um pipeline Python preserva o arquivo bruto, valida
integridade e schema, normaliza 11 edições e gera tabelas, quatro figuras e um
artigo acadêmico responsivo.

**[Ler artigo no GitHub Pages](https://pedro-art2611.github.io/Projeto-Pr-ticoG2/)** ·
[Dicionário](data/data_dictionary.md) · [Validação](VALIDACAO.md) · [Proveniência](proveniencia.json)

Palavras-chave: Ideb; educação básica; Rio de Janeiro; análise exploratória;
Python; princípios FAIR.

## Perguntas e achados

1. **RQ1: Evolução:** a mediana do Ideb passou de 3,9 (2005) para 5,9 (2025).
   No painel dos mesmos 82 municípios com resultado em todas as edições, os
   extremos também são 3,9 e 5,9.
2. **RQ2: Dispersão:** o intervalo interquartil passou de 0,600 para 0,725.
   Melhora do nível central não equivale a convergência uniforme entre redes.
3. **RQ3: Mudança recente:** entre 2023 e 2025, 82 municípios aumentaram o Ideb,
   seis diminuíram e quatro mantiveram o índice divulgado. As contribuições
   médias de rendimento e nota ao produto P×N foram positivas.

São 1.012 observações município/edição, com 998 Idebs válidos e 14 ausentes.
Essas estatísticas são entre municípios, sem peso por matrículas; não são o
Ideb oficial do estado. A decomposição dos componentes é algébrica, não causal.

## Fonte e confiança

[Catálogo oficial Inep](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados/2005-2025).
Arquivo: `divulgacao_anos_iniciais_municipios_2025.zip`, aba
`IDEB_AI_MUNICÍPIOS`, cabeçalho técnico na linha 10.

O ZIP de 25,3 MB está versionado em `data/raw/`. Foi obtido de um espelho do
Transparência Política, pois o download oficial falhou. **A correspondência
com os bytes atuais do Inep ainda não foi confirmada.** O SHA-256 da entrada
e o MD5 interno do XLSX são verificados pelo pipeline. Isso confirma integridade
da versão fixada, não autenticação independente de sua origem.

SHA-256 da entrada:
`89100286327ab07a4b1318ba51974d62da90af334f663bedf6374cb67298a3e7`.

Não se preenchem resultados ausentes, não se removem outliers automaticamente
e não se extrapolam metas além de 2021. `Municipal` e `Pública` não são somadas.
As notas internas e a inspeção inicial permanecem em `data/inspection/`.

## Reprodução: Windows / PowerShell

Ambiente validado: **Python 3.14.7, Windows**, UTF-8. As versões diretas e
transitivas foram congeladas por `pip freeze` em um ambiente virtual novo.
Use Python 3.14; outros interpretadores não foram homologados.

```powershell
git clone https://github.com/pedro-art2611/Projeto-Pr-ticoG2.git
cd Projeto-Pr-ticoG2
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.report
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify_reproducibility.py
.\.venv\Scripts\python.exe scripts/check_site.py
.\.venv\Scripts\python.exe scripts/execute_notebook.py
.\.venv\Scripts\python.exe -m http.server 8000 --directory docs
```

Abra **http://localhost:8000**. A ativação do ambiente não é obrigatória, evitando
mudanças na política de execução do PowerShell. Em Linux/macOS, crie o ambiente
com `python3.14 -m venv .venv` e substitua o executável por `.venv/bin/python`.
O mesmo arquivo congelado não contém dependências exclusivas de Windows.
Validação em outra plataforma permanece pendente.

`python -m src.report` executa ETL → análise → gráficos → artigo. O notebook
reutiliza essas funções; não mantém uma segunda limpeza. Sua execução automatizada
gera uma cópia com saídas em `outputs/`, ignorada pelo Git, e registra o kernel
somente no diretório local `.jupyter/`.

O ZIP já incluído elimina a necessidade de rede na análise. Se estiver ausente,
`python -m src.etl --download` tenta a URL oficial com verificação do hash fixado.
Uma versão diferente é rejeitada e exige revisão explícita, nunca substituição
silenciosa. Nenhum código do ZIP é executado.

## Produtos e estrutura

```text
├── README.md, LICENSE, LICENSE-CONTENT.md, CITATION.cff
├── requirements.txt, .gitignore, VALIDACAO.md
├── proveniencia.json, reproducibilidade.json
├── data/
│   ├── raw/                   # ZIP integral e catálogo preservados
│   ├── inspection/            # Recorte e notas da coleta inicial
│   ├── processed/             # CSV.gz, resumos, pares e validação JSON
│   ├── data_dictionary.md     # Todas as variáveis, tipos e unidades
│   └── LICENSE.md             # Atribuição e pendência de licença dos dados
├── notebooks/analise_exploratoria.ipynb
├── src/
│   ├── __init__.py
│   ├── etl.py                 # Ingestão, integridade, schema, normalização
│   ├── analysis.py            # Estatísticas, painel e decomposição pareada
│   ├── report.py              # Figuras e geração do artigo
│   └── article.html           # Fonte editorial; index.html é gerado
├── scripts/                   # Notebook, verificação do site e reprodução
├── tests/test_pipeline.py     # Contratos de dados e integridade
└── docs/
    ├── index.html, .nojekyll
    └── assets/                # SVG, JSON, CSV, CSS, JS e Plotly local
```

Altere o conteúdo editorial em `src/article.html` e execute o pipeline para
atualizar `docs/index.html`. O resumo respeita 150 a 250 palavras. As figuras
vetoriais aparecem sem JavaScript; os gráficos interativos usam dados exportados
e carregam a biblioteca local apenas quando solicitados. Os CSVs das figuras
podem ser baixados na própria página.

## FAIR e licenças

| Pilar | Evidência |
|---|---|
| Localizável | Autoria, palavras-chave, fonte primária, CITATION.cff e proveniência |
| Acessível | Repositório público, entrada versionada, artigo estático, sem login pago |
| Interoperável | CSV UTF-8, JSON, SVG, código municipal e dicionário completo |
| Reutilizável | Código MIT, texto e figuras CC BY 4.0, versões fixadas e instruções |

O software está sob [MIT](LICENSE); texto e figuras autorais sob
[CC BY 4.0](LICENSE-CONTENT.md). Os dados e suas transformações mantêm a
atribuição ao Inep e as condições da fonte. **A licença específica da base ainda
precisa de confirmação**, conforme [data/LICENSE.md](data/LICENSE.md). Não
declaramos conformidade FAIR integral nem certificação enquanto essa questão
e a comparação oficial estiverem pendentes.

## Publicação e limites

O GitHub Pages deve servir a branch `main`, pasta `/docs`, em Settings → Pages →
Deploy from a branch. O artigo não depende de backend nem de etapas de build
no servidor. O estado efetivo da publicação é registrado em `VALIDACAO.md`.

2021 exige cautela pelo contexto da pandemia, citado nas notas originais.
Não há dados individuais, ajuste socioeconômico ou estimativa causal. O painel
completo seleciona municípios com divulgação contínua; não resolve todo viés.
Consulte as limitações e referências completas no artigo.

## Convenção de commits

Tipo semântico e descrição em português: `feat:`, `fix:`, `docs:`, `test:` e
`chore:`. Exemplo: `feat: implementa análise das redes municipais fluminenses`.
