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

## Dicionário dos produtos derivados

CSVs: UTF-8, vírgula separadora e ponto decimal. JSONs: objeto chave/valor UTF-8. Os resumos não são o Ideb oficial do estado. Não há valores nulos nos produtos derivados desta versão; qualquer conjunto sem variância impede o cálculo de correlação e gera erro explícito.

`resumo_por_edicao.csv` usa todos os resultados válidos de cada edição. `painel_balanceado.csv` usa somente os mesmos 82 municípios presentes em todas as edições. Ambos têm uma linha por edição. `comparacao_2023_2025.csv` tem uma linha por município com dados completos nos dois anos. `correlacoes_2023_2025.csv` tem uma linha por método. `metricas.json` agrega valores usados no artigo; `validacao.json` registra controles da ingestão. Cópias CSV em `docs/assets` seguem os mesmos schemas.

### `resumo_por_edicao.csv`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| ano | Edição observada | integer | AAAA, de 2005 a 2025 |
| n | Municípios com Ideb numérico na edição e no conjunto selecionado | integer | contagem |
| ausentes | Municípios do conjunto selecionado sem Ideb na edição | integer | contagem |
| media | Média aritmética simples entre municípios, sem peso por matrículas | float | pontos do Ideb |
| mediana | Percentil 50 do Ideb | float | pontos do Ideb |
| q1 | Percentil 25, interpolação linear | float | pontos do Ideb |
| q3 | Percentil 75, interpolação linear | float | pontos do Ideb |
| iqr | Intervalo interquartil: q3 menos q1 | float | pontos do Ideb |
| desvio_padrao | Desvio-padrão populacional dos municípios observados; ddof=0 | float | pontos do Ideb |
| minimo | Menor Ideb numérico observado | float | pontos do Ideb |
| maximo | Maior Ideb numérico observado | float | pontos do Ideb |

### `painel_balanceado.csv`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| ano | Edição observada | integer | AAAA, de 2005 a 2025 |
| n | Municípios com Ideb numérico na edição e no conjunto selecionado | integer | contagem |
| ausentes | Municípios do conjunto selecionado sem Ideb na edição | integer | contagem |
| media | Média aritmética simples entre municípios, sem peso por matrículas | float | pontos do Ideb |
| mediana | Percentil 50 do Ideb | float | pontos do Ideb |
| q1 | Percentil 25, interpolação linear | float | pontos do Ideb |
| q3 | Percentil 75, interpolação linear | float | pontos do Ideb |
| iqr | Intervalo interquartil: q3 menos q1 | float | pontos do Ideb |
| desvio_padrao | Desvio-padrão populacional dos municípios observados; ddof=0 | float | pontos do Ideb |
| minimo | Menor Ideb numérico observado | float | pontos do Ideb |
| maximo | Maior Ideb numérico observado | float | pontos do Ideb |

### `comparacao_2023_2025.csv`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| codigo_municipio | Código IBGE; chave única da comparação pareada | string | 7 dígitos |
| municipio | Nome municipal na fonte | string | UTF-8 |
| ideb_2023 | Ideb divulgado em 2023 | float | 0 a 10, arredondado pela fonte |
| rendimento_2023 | Indicador P de rendimento em 2023 | float | proporção, 0 a 1 |
| nota_padronizada_2023 | Nota média padronizada N do Saeb em 2023 | float | 0 a 10 |
| ideb_2025 | Ideb divulgado em 2025 | float | 0 a 10, arredondado pela fonte |
| rendimento_2025 | Indicador P de rendimento em 2025 | float | proporção, 0 a 1 |
| nota_padronizada_2025 | Nota média padronizada N do Saeb em 2025 | float | 0 a 10 |
| delta_ideb | Ideb de 2025 menos Ideb de 2023 | float | pontos do Ideb; pode ser negativo |
| delta_rendimento | P de 2025 menos P de 2023 | float | diferença de proporções; multiplicar por 100 para pontos percentuais |
| delta_nota_padronizada | N de 2025 menos N de 2023 | float | pontos na escala padronizada |
| contribuicao_rendimento | Média de N nos dois anos multiplicada por delta_rendimento | float | pontos do produto P×N |
| contribuicao_nota | Média de P nos dois anos multiplicada por delta_nota_padronizada | float | pontos do produto P×N |
| delta_produto | P_2025×N_2025 menos P_2023×N_2023; soma das duas contribuições | float | pontos do produto P×N |
| residuo_arredondamento | delta_ideb menos delta_produto; preserva a diferença em relação ao índice divulgado | float | pontos; tolerância absoluta de 0,1002 na comparação de dois anos |
| trajetoria | Sinal de delta_ideb com tolerância numérica de 1e-9 | string | Aumentou, Diminuiu ou Estável |

### `correlacoes_2023_2025.csv`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| variavel_x | Variável do primeiro ano na comparação | string | ideb_2023 |
| variavel_y | Variável do segundo ano na comparação | string | ideb_2025 |
| metodo | Coeficiente calculado; Spearman usa postos médios nos empates | string | pearson ou spearman |
| n_pares | Pares completos e finitos efetivamente utilizados | integer | contagem; 92 nesta versão |
| coeficiente | Associação linear (Pearson) ou monotônica (Spearman); não mede causalidade | float | adimensional, de -1 a 1 |

### `metricas.json`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| municipios | Municípios distintos no recorte | integer | contagem |
| edicoes | Edições presentes na série | integer | contagem |
| observacoes | Linhas município/edição, incluindo resultados ausentes | integer | contagem |
| validos | Linhas com Ideb numérico | integer | contagem |
| ausentes | Linhas sem Ideb numérico | integer | contagem |
| painel_balanceado_n | Municípios com Ideb nas onze edições | integer | contagem |
| pares | Municípios completos nos dois anos recentes e nos componentes P/N | integer | contagem |
| aumentou | Pares com trajetória Aumentou | integer | contagem |
| diminuiu | Pares com trajetória Diminuiu | integer | contagem |
| estavel | Pares com trajetória Estável | integer | contagem |
| delta_medio | Média simples de delta_ideb nos pares | float | pontos do Ideb |
| delta_mediano | Mediana de delta_ideb nos pares | float | pontos do Ideb |
| delta_p_medio | Média simples de delta_rendimento | float | diferença de proporções |
| delta_n_medio | Média simples de delta_nota_padronizada | float | pontos padronizados |
| contribuicao_p_media | Média simples de contribuicao_rendimento | float | pontos do produto P×N |
| contribuicao_n_media | Média simples de contribuicao_nota | float | pontos do produto P×N |
| delta_produto_medio | Média simples de delta_produto | float | pontos do produto P×N |
| correlacao_pearson | Coeficiente Pearson entre Ideb 2023 e 2025 | float | adimensional, -1 a 1 |
| correlacao_spearman | Coeficiente Spearman entre Ideb 2023 e 2025 | float | adimensional, -1 a 1 |
| mediana_2005 | Mediana entre resultados disponíveis de 2005 | float | pontos do Ideb |
| iqr_2005 | Q3 menos Q1 dos resultados disponíveis de 2005 | float | pontos do Ideb |
| dp_2005 | Desvio-padrão populacional em 2005 | float | pontos do Ideb |
| painel_mediana_2005 | Mediana de 2005 nos mesmos municípios com série completa | float | pontos do Ideb |
| mediana_2025 | Mediana entre resultados disponíveis de 2025 | float | pontos do Ideb |
| iqr_2025 | Q3 menos Q1 dos resultados disponíveis de 2025 | float | pontos do Ideb |
| dp_2025 | Desvio-padrão populacional em 2025 | float | pontos do Ideb |
| painel_mediana_2025 | Mediana de 2025 nos mesmos municípios com série completa | float | pontos do Ideb |

### `validacao.json`

| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |
|---|---|---|---|
| sha256_entrada | Resumo criptográfico do ZIP de entrada | string | 64 dígitos hexadecimais |
| linhas_origem | Registros válidos município/rede na planilha nacional | integer | contagem |
| municipios | Municípios distintos do recorte | integer | contagem |
| linhas_normalizadas | Observações município/edição | integer | contagem |
| ideb_validos | Observações com Ideb numérico | integer | contagem |
| ideb_ausentes | Observações com Ideb ausente | integer | contagem |
| imputacoes | Valores imputados pelo ETL | integer | zero nesta metodologia |
| chaves_duplicadas | Duplicações após validação | integer | zero; a execução falha se houver duplicação |
| autenticidade_fonte_oficial | Estado da comparação binária registrada na proveniência | string | descrição do download oficial e do protocolo usado |
