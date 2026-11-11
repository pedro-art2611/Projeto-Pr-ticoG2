# Dicionário de dados

Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva. Unilasalle-RJ, Sistemas de Informação, Linguagem de Programação, 6º período.

Arquivo: `processed/ideb_rj.csv.gz`. UTF-8, vírgula como separador, ponto decimal. Uma linha por município × rede × etapa × edição. Chave: `codigo_municipio, rede, etapa, ano`. 1.012 linhas. Célula numérica vazia representa ausência, nunca zero. Sem imputação.

| Variável | Significado | Tipo primitivo | Formato / unidade | Origem |
|---|---|---|---|---|
| codigo_municipio | Identificador IBGE do município | string | 7 dígitos | CO_MUNICIPIO |
| municipio | Nome na fonte | string | UTF-8 | NO_MUNICIPIO |
| uf | Unidade federativa | string | RJ | SG_UF |
| rede | Dependência administrativa | string | Municipal | REDE |
| etapa | Etapa analisada | string | Anos iniciais | arquivo selecionado |
| ano | Edição do indicador | integer | 2005 a 2025; bienal | sufixo da coluna |
| situacao_ideb | Disponibilidade do Ideb | string | divulgado ou ausente | derivada da presença numérica |
| ideb | Ideb observado | float, anulável | 0 a 10 | `VL_OBSERVADO_{year}` |
| ideb_original | Valor ou marcador antes da conversão de ideb | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| rendimento | Indicador de rendimento P | float, anulável | 0 a 1 | `VL_INDICADOR_REND_{year}` |
| rendimento_original | Valor ou marcador antes da conversão de rendimento | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| nota_padronizada | Nota média padronizada N do Saeb | float, anulável | 0 a 10 | `VL_NOTA_MEDIA_{year}` |
| nota_padronizada_original | Valor ou marcador antes da conversão de nota_padronizada | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| matematica | Proficiência em matemática | float, anulável | escala Saeb | `VL_NOTA_MATEMATICA_{year}` |
| matematica_original | Valor ou marcador antes da conversão de matematica | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| portugues | Proficiência em língua portuguesa | float, anulável | escala Saeb | `VL_NOTA_PORTUGUES_{year}` |
| portugues_original | Valor ou marcador antes da conversão de portugues | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_etapa | Aprovação agregada da etapa (SI a 4ª série) | float, anulável | % | `VL_APROVACAO_{year}_SI_4` |
| aprovacao_etapa_original | Valor ou marcador antes da conversão de aprovacao_etapa | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_si | Aprovação na série inicial (SI), conforme fonte | float, anulável | % | `VL_APROVACAO_{year}_SI` |
| aprovacao_si_original | Valor ou marcador antes da conversão de aprovacao_si | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_1 | Aprovação na 1ª série, conforme fonte | float, anulável | % | `VL_APROVACAO_{year}_1` |
| aprovacao_1_original | Valor ou marcador antes da conversão de aprovacao_1 | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_2 | Aprovação na 2ª série, conforme fonte | float, anulável | % | `VL_APROVACAO_{year}_2` |
| aprovacao_2_original | Valor ou marcador antes da conversão de aprovacao_2 | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_3 | Aprovação na 3ª série, conforme fonte | float, anulável | % | `VL_APROVACAO_{year}_3` |
| aprovacao_3_original | Valor ou marcador antes da conversão de aprovacao_3 | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| aprovacao_4 | Aprovação na 4ª série, conforme fonte | float, anulável | % | `VL_APROVACAO_{year}_4` |
| aprovacao_4_original | Valor ou marcador antes da conversão de aprovacao_4 | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |
| meta | Meta do primeiro ciclo; não existe após 2021 | float, anulável | 0 a 10 | `VL_PROJECAO_{year}` |
| meta_original | Valor ou marcador antes da conversão de meta | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |

## Interpretação e limites

`ND`: participantes insuficientes no Saeb; `ND*`: não divulgação solicitada nas portarias citadas pela fonte; `ND***`: extravio de pelo menos 20% do material e participação insuficiente. `-`: ausência sem motivo específico determinado nesta auditoria. Marcadores preservados por variável; não inferir um motivo a partir de outro componente.

As nomenclaturas SI e 1ª a 4ª série foram mantidas conforme os cabeçalhos técnicos. Não equiparar automaticamente cada sufixo a um ano escolar atual. Aprovação em % não equivale ao indicador P (proporção de rendimento). Matemática e português estão na escala Saeb, não na escala 0 a 10. N é a nota padronizada usada com P na composição do Ideb.

`meta` e `meta_original` vazios em 2005/2023/2025 significam inexistência de meta desse primeiro ciclo na planilha, não descumprimento. Não extrapolar metas.

A cópia bruta permanece em `raw/`, com SHA-256 e origem em `proveniencia.json`. A extração numérica pode mudar a representação textual de floats do Excel, preservando os valores numéricos. As colunas `_original` preservam os marcadores e a representação retornada pelo leitor, não os bytes XML internos.

Arquivos derivados: `resumo_por_edicao.csv` contém n, média municipal não ponderada, mediana, quartis Q1/Q3 (interpolação linear), IQR, mínimo/máximo e desvio-padrão populacional (ddof=0). `comparacao_2023_2025.csv` contém valores pareados, deltas e decomposição simétrica de P×N. `painel_balanceado.csv` contém os mesmos resumos apenas para municípios com Ideb em todas as edições. São estatísticas entre municípios, sem ponderação por matrículas; não são o Ideb oficial do estado.
