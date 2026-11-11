"""Metadados dos produtos derivados, com tipos, unidades e regras de cálculo."""
from pathlib import Path

SUMMARY = {
    "ano": ("Edição observada", "integer", "AAAA, de 2005 a 2025"),
    "n": ("Municípios com Ideb numérico na edição e no conjunto selecionado", "integer", "contagem"),
    "ausentes": ("Municípios do conjunto selecionado sem Ideb na edição", "integer", "contagem"),
    "media": ("Média aritmética simples entre municípios, sem peso por matrículas", "float", "pontos do Ideb"),
    "mediana": ("Percentil 50 do Ideb", "float", "pontos do Ideb"),
    "q1": ("Percentil 25, interpolação linear", "float", "pontos do Ideb"),
    "q3": ("Percentil 75, interpolação linear", "float", "pontos do Ideb"),
    "iqr": ("Intervalo interquartil: q3 menos q1", "float", "pontos do Ideb"),
    "desvio_padrao": ("Desvio-padrão populacional dos municípios observados; ddof=0", "float", "pontos do Ideb"),
    "minimo": ("Menor Ideb numérico observado", "float", "pontos do Ideb"),
    "maximo": ("Maior Ideb numérico observado", "float", "pontos do Ideb"),
}
PAIRED = {
    "codigo_municipio": ("Código IBGE; chave única da comparação pareada", "string", "7 dígitos"),
    "municipio": ("Nome municipal na fonte", "string", "UTF-8"),
}
for year in (2023, 2025):
    for name, meaning, unit in [
        ("ideb", "Ideb divulgado", "0 a 10, arredondado pela fonte"),
        ("rendimento", "Indicador P de rendimento", "proporção, 0 a 1"),
        ("nota_padronizada", "Nota média padronizada N do Saeb", "0 a 10")]:
        PAIRED[f"{name}_{year}"] = (f"{meaning} em {year}", "float", unit)
PAIRED.update({
    "delta_ideb": ("Ideb de 2025 menos Ideb de 2023", "float", "pontos do Ideb; pode ser negativo"),
    "delta_rendimento": ("P de 2025 menos P de 2023", "float", "diferença de proporções; multiplicar por 100 para pontos percentuais"),
    "delta_nota_padronizada": ("N de 2025 menos N de 2023", "float", "pontos na escala padronizada"),
    "contribuicao_rendimento": ("Média de N nos dois anos multiplicada por delta_rendimento", "float", "pontos do produto P×N"),
    "contribuicao_nota": ("Média de P nos dois anos multiplicada por delta_nota_padronizada", "float", "pontos do produto P×N"),
    "delta_produto": ("P_2025×N_2025 menos P_2023×N_2023; soma das duas contribuições", "float", "pontos do produto P×N"),
    "residuo_arredondamento": ("delta_ideb menos delta_produto; preserva a diferença em relação ao índice divulgado", "float", "pontos; tolerância absoluta de 0,1002 na comparação de dois anos"),
    "trajetoria": ("Sinal de delta_ideb com tolerância numérica de 1e-9", "string", "Aumentou, Diminuiu ou Estável"),
})
CORRELATION = {
    "variavel_x": ("Variável do primeiro ano na comparação", "string", "ideb_2023"),
    "variavel_y": ("Variável do segundo ano na comparação", "string", "ideb_2025"),
    "metodo": ("Coeficiente calculado; Spearman usa postos médios nos empates", "string", "pearson ou spearman"),
    "n_pares": ("Pares completos e finitos efetivamente utilizados", "integer", "contagem; 92 nesta versão"),
    "coeficiente": ("Associação linear (Pearson) ou monotônica (Spearman); não mede causalidade", "float", "adimensional, de -1 a 1"),
}
METRICS = {
    "municipios": ("Municípios distintos no recorte", "integer", "contagem"),
    "edicoes": ("Edições presentes na série", "integer", "contagem"),
    "observacoes": ("Linhas município/edição, incluindo resultados ausentes", "integer", "contagem"),
    "validos": ("Linhas com Ideb numérico", "integer", "contagem"),
    "ausentes": ("Linhas sem Ideb numérico", "integer", "contagem"),
    "painel_balanceado_n": ("Municípios com Ideb nas onze edições", "integer", "contagem"),
    "pares": ("Municípios completos nos dois anos recentes e nos componentes P/N", "integer", "contagem"),
    "aumentou": ("Pares com trajetória Aumentou", "integer", "contagem"),
    "diminuiu": ("Pares com trajetória Diminuiu", "integer", "contagem"),
    "estavel": ("Pares com trajetória Estável", "integer", "contagem"),
    "delta_medio": ("Média simples de delta_ideb nos pares", "float", "pontos do Ideb"),
    "delta_mediano": ("Mediana de delta_ideb nos pares", "float", "pontos do Ideb"),
    "delta_p_medio": ("Média simples de delta_rendimento", "float", "diferença de proporções"),
    "delta_n_medio": ("Média simples de delta_nota_padronizada", "float", "pontos padronizados"),
    "contribuicao_p_media": ("Média simples de contribuicao_rendimento", "float", "pontos do produto P×N"),
    "contribuicao_n_media": ("Média simples de contribuicao_nota", "float", "pontos do produto P×N"),
    "delta_produto_medio": ("Média simples de delta_produto", "float", "pontos do produto P×N"),
    "correlacao_pearson": ("Coeficiente Pearson entre Ideb 2023 e 2025", "float", "adimensional, -1 a 1"),
    "correlacao_spearman": ("Coeficiente Spearman entre Ideb 2023 e 2025", "float", "adimensional, -1 a 1"),
}
for year in (2005, 2025):
    METRICS[f"mediana_{year}"] = (f"Mediana entre resultados disponíveis de {year}", "float", "pontos do Ideb")
    METRICS[f"iqr_{year}"] = (f"Q3 menos Q1 dos resultados disponíveis de {year}", "float", "pontos do Ideb")
    METRICS[f"dp_{year}"] = (f"Desvio-padrão populacional em {year}", "float", "pontos do Ideb")
    METRICS[f"painel_mediana_{year}"] = (f"Mediana de {year} nos mesmos municípios com série completa", "float", "pontos do Ideb")
VALIDATION = {
    "sha256_entrada": ("Resumo criptográfico do ZIP de entrada", "string", "64 dígitos hexadecimais"),
    "linhas_origem": ("Registros válidos município/rede na planilha nacional", "integer", "contagem"),
    "municipios": ("Municípios distintos do recorte", "integer", "contagem"),
    "linhas_normalizadas": ("Observações município/edição", "integer", "contagem"),
    "ideb_validos": ("Observações com Ideb numérico", "integer", "contagem"),
    "ideb_ausentes": ("Observações com Ideb ausente", "integer", "contagem"),
    "imputacoes": ("Valores imputados pelo ETL", "integer", "zero nesta metodologia"),
    "chaves_duplicadas": ("Duplicações após validação", "integer", "zero; a execução falha se houver duplicação"),
    "autenticidade_fonte_oficial": ("Estado da comparação binária registrada na proveniência", "string", "descrição do download oficial e do protocolo usado"),
}

DERIVED_SCHEMAS = {
    "resumo_por_edicao.csv": SUMMARY,
    "painel_balanceado.csv": SUMMARY,
    "comparacao_2023_2025.csv": PAIRED,
    "correlacoes_2023_2025.csv": CORRELATION,
    "metricas.json": METRICS,
    "validacao.json": VALIDATION,
}


def append_derived_dictionary(path: Path) -> None:
    lines = ["", "## Dicionário dos produtos derivados", "",
             "CSVs: UTF-8, vírgula separadora e ponto decimal. JSONs: objeto chave/valor UTF-8. Os resumos não são o Ideb oficial do estado. Não há valores nulos nos produtos derivados desta versão; qualquer conjunto sem variância impede o cálculo de correlação e gera erro explícito.", "",
             "`resumo_por_edicao.csv` usa todos os resultados válidos de cada edição. `painel_balanceado.csv` usa somente os mesmos 82 municípios presentes em todas as edições. Ambos têm uma linha por edição. `comparacao_2023_2025.csv` tem uma linha por município com dados completos nos dois anos. `correlacoes_2023_2025.csv` tem uma linha por método. `metricas.json` agrega valores usados no artigo; `validacao.json` registra controles da ingestão. Cópias CSV em `docs/assets` seguem os mesmos schemas.", ""]
    for filename, fields in DERIVED_SCHEMAS.items():
        lines += [f"### `{filename}`", "", "| Variável | Significado / cálculo | Tipo primitivo | Formato / unidade |", "|---|---|---|---|"]
        lines.extend(f"| {key} | {meaning} | {kind} | {unit} |" for key, (meaning, kind, unit) in fields.items())
        lines.append("")
    with path.open("a", encoding="utf-8", newline="\n") as output:
        output.write("\n".join(lines))
