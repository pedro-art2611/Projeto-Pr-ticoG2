"""Ingestão verificada, normalização e persistência sem imputação.

Autores: Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva.
Unilasalle-RJ | Sistemas de Informação | Linguagem de Programação | 6º período.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_NAME = "divulgacao_anos_iniciais_municipios_2025.zip"
SHA256 = "89100286327ab07a4b1318ba51974d62da90af334f663bedf6374cb67298a3e7"
OFFICIAL = "https://download.inep.gov.br/ideb/resultados/" + RAW_NAME
YEARS = tuple(range(2005, 2026, 2))
MISSING = {"", "-", "ND", "ND*", "ND***"}
FIELDS = {
    "ideb": ("VL_OBSERVADO_{year}", "Ideb observado", "0 a 10"),
    "rendimento": ("VL_INDICADOR_REND_{year}", "Indicador de rendimento P", "0 a 1"),
    "nota_padronizada": ("VL_NOTA_MEDIA_{year}", "Nota média padronizada N do Saeb", "0 a 10"),
    "matematica": ("VL_NOTA_MATEMATICA_{year}", "Proficiência em matemática", "escala Saeb"),
    "portugues": ("VL_NOTA_PORTUGUES_{year}", "Proficiência em língua portuguesa", "escala Saeb"),
    "aprovacao_etapa": ("VL_APROVACAO_{year}_SI_4", "Aprovação agregada da etapa (SI a 4ª série)", "%"),
    "aprovacao_si": ("VL_APROVACAO_{year}_SI", "Aprovação na série inicial (SI), conforme fonte", "%"),
    "aprovacao_1": ("VL_APROVACAO_{year}_1", "Aprovação na 1ª série, conforme fonte", "%"),
    "aprovacao_2": ("VL_APROVACAO_{year}_2", "Aprovação na 2ª série, conforme fonte", "%"),
    "aprovacao_3": ("VL_APROVACAO_{year}_3", "Aprovação na 3ª série, conforme fonte", "%"),
    "aprovacao_4": ("VL_APROVACAO_{year}_4", "Aprovação na 4ª série, conforme fonte", "%"),
    "meta": ("VL_PROJECAO_{year}", "Meta do primeiro ciclo; não existe após 2021", "0 a 10"),
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    """Gzip sem nome/caminho/data variáveis no cabeçalho."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = frame.to_csv(index=False, lineterminator="\n", float_format="%.12g").encode("utf-8")
    if path.suffix == ".gz":
        with path.open("wb") as f, gzip.GzipFile(fileobj=f, filename="", mode="wb", mtime=0) as gz:
            gz.write(content)
    else:
        path.write_bytes(content)


def acquire(path: Path, download: bool = False) -> bytes:
    if not path.exists():
        if not download:
            raise FileNotFoundError(f"Entrada ausente: {path}. Use --download para tentar a fonte oficial.")
        with urllib.request.urlopen(OFFICIAL, timeout=90) as response:
            payload = response.read()
        if hashlib.sha256(payload).hexdigest() != SHA256:
            raise ValueError("A fonte mudou: hash diferente da versão fixada. Revisão explícita necessária.")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != SHA256:
        raise ValueError("SHA-256 inválido: a entrada não corresponde à versão auditada.")
    return payload


def read_source(payload: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        xlsx = [n for n in z.namelist() if n.endswith(".xlsx")]
        if len(xlsx) != 1:
            raise ValueError("Esperada uma única planilha XLSX no ZIP.")
        name = xlsx[0]
        data = z.read(name)
        manifests = [n for n in z.namelist() if n.endswith(".txt") and "md5" in n.lower()]
        if len(manifests) != 1:
            raise ValueError("Manifesto MD5 ausente ou ambíguo.")
        expected = re.search(r"([0-9a-fA-F]{32})\s+\*?" + re.escape(Path(name).name), z.read(manifests[0]).decode("utf-8-sig"))
        if not expected or hashlib.md5(data).hexdigest() != expected[1].lower():
            raise ValueError("MD5 do XLSX não confere com o manifesto interno.")
    frame = pd.read_excel(io.BytesIO(data), sheet_name="IDEB_AI_MUNICÍPIOS", header=9,
                          dtype=object, keep_default_na=False, engine="openpyxl")
    required = {"SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "REDE"}
    required |= {pattern.format(year=y) for pattern, _, _ in FIELDS.values() for y in YEARS
                 if not (pattern.startswith("VL_PROJECAO") and (y < 2007 or y > 2021))}
    if set(frame.columns) != required:
        raise ValueError(f"Schema alterado: ausentes={required - set(frame.columns)}; extras={set(frame.columns) - required}")
    # Notas de rodapé nunca entram como observações.
    frame = frame[frame.CO_MUNICIPIO.astype(str).str.fullmatch(r"\d{7}")].copy()
    frame["CO_MUNICIPIO"] = frame.CO_MUNICIPIO.astype(str)
    if frame.duplicated(["CO_MUNICIPIO", "REDE"]).any():
        raise ValueError("Chave município/rede duplicada na origem.")
    return frame


def parse_numbers(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.strip()
    values = pd.to_numeric(text.str.replace(",", ".", regex=False), errors="coerce")
    unexpected = text[values.isna() & ~text.isin(MISSING)].unique()
    if len(unexpected):
        raise ValueError(f"Valores não reconhecidos: {unexpected.tolist()}")
    return values.astype(float)


def normalize(source: pd.DataFrame) -> pd.DataFrame:
    subset = source[(source.SG_UF == "RJ") & (source.REDE == "Municipal")].copy()
    if len(subset) != 92 or subset.CO_MUNICIPIO.nunique() != 92:
        raise ValueError("O recorte não contém exatamente 92 municípios distintos.")
    frames = []
    for year in YEARS:
        part = subset[["CO_MUNICIPIO", "NO_MUNICIPIO", "SG_UF", "REDE"]].rename(columns={
            "CO_MUNICIPIO": "codigo_municipio", "NO_MUNICIPIO": "municipio", "SG_UF": "uf", "REDE": "rede"})
        part = part.assign(etapa="Anos iniciais", ano=year)
        for field, (pattern, _, unit) in FIELDS.items():
            column = pattern.format(year=year)
            if field == "meta" and (year < 2007 or year > 2021):
                raw = pd.Series("", index=subset.index)
            else:
                raw = subset[column].astype(str).str.strip()
            part[field + "_original"] = raw
            part[field] = parse_numbers(raw)
            high = 100 if unit == "%" else 1 if unit == "0 a 1" else 10 if unit == "0 a 10" else None
            valid = part[field].dropna()
            if (valid < 0).any() or (high is not None and (valid > high).any()):
                raise ValueError(f"Valores fora de faixa: {field}/{year}")
        part["situacao_ideb"] = np.where(part.ideb.notna(), "divulgado", "ausente")
        frames.append(part)
    tidy = pd.concat(frames, ignore_index=True).sort_values(["codigo_municipio", "ano"]).reset_index(drop=True)
    if tidy.duplicated(["codigo_municipio", "rede", "etapa", "ano"]).any():
        raise ValueError("Duplicação após normalização.")
    complete = tidy.dropna(subset=["ideb", "rendimento", "nota_padronizada"])
    residual = (complete.ideb - complete.rendimento * complete.nota_padronizada).abs()
    if (residual > 0.0501).any():
        raise ValueError("Ideb incompatível com P × N e arredondamento da fonte.")
    return tidy


def dictionary(path: Path) -> None:
    lines = ["# Dicionário de dados", "",
             "Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva. Unilasalle-RJ, Sistemas de Informação, Linguagem de Programação, 6º período.", "",
             "Arquivo: `processed/ideb_rj.csv.gz`. UTF-8, vírgula como separador, ponto decimal. Uma linha por município × rede × etapa × edição. Chave: `codigo_municipio, rede, etapa, ano`. 1.012 linhas. Célula numérica vazia representa ausência, nunca zero. Sem imputação.", "",
             "| Variável | Significado | Tipo primitivo | Formato / unidade | Origem |",
             "|---|---|---|---|---|"]
    for field, meaning, kind, fmt, origin in [
        ("codigo_municipio", "Identificador IBGE do município", "string", "7 dígitos", "CO_MUNICIPIO"),
        ("municipio", "Nome na fonte", "string", "UTF-8", "NO_MUNICIPIO"),
        ("uf", "Unidade federativa", "string", "RJ", "SG_UF"),
        ("rede", "Dependência administrativa", "string", "Municipal", "REDE"),
        ("etapa", "Etapa analisada", "string", "Anos iniciais", "arquivo selecionado"),
        ("ano", "Edição do indicador", "integer", "2005 a 2025; bienal", "sufixo da coluna"),
        ("situacao_ideb", "Disponibilidade do Ideb", "string", "divulgado ou ausente", "derivada da presença numérica")]:
        lines.append(f"| {field} | {meaning} | {kind} | {fmt} | {origin} |")
    for field, (pattern, meaning, unit) in FIELDS.items():
        lines.append(f"| {field} | {meaning} | float, anulável | {unit} | `{pattern}` |")
        lines.append(f"| {field}_original | Valor ou marcador antes da conversão de {field} | string | número textual, `-`, `ND`, `ND*`, `ND***` ou vazio | mesma coluna |")
    lines += ["", "## Interpretação e limites", "",
              "`ND`: participantes insuficientes no Saeb; `ND*`: não divulgação solicitada nas portarias citadas pela fonte; `ND***`: extravio de pelo menos 20% do material e participação insuficiente. `-`: ausência sem motivo específico determinado nesta auditoria. Marcadores preservados por variável; não inferir um motivo a partir de outro componente.", "",
              "As nomenclaturas SI e 1ª–4ª série foram mantidas conforme os cabeçalhos técnicos. Não equiparar automaticamente cada sufixo a um ano escolar atual. Aprovação em % não equivale ao indicador P (proporção de rendimento). Matemática e português estão na escala Saeb, não na escala 0–10. N é a nota padronizada usada com P na composição do Ideb.", "",
              "`meta` e `meta_original` vazios em 2005/2023/2025 significam inexistência de meta desse primeiro ciclo na planilha, não descumprimento. Não extrapolar metas.", "",
              "A cópia bruta permanece em `raw/`, com SHA-256 e origem em `proveniencia.json`. A extração numérica pode mudar a representação textual de floats do Excel, preservando os valores numéricos. As colunas `_original` preservam os marcadores e a representação retornada pelo leitor, não os bytes XML internos.", "",
              "Arquivos derivados: `resumo_por_edicao.csv` contém n, média municipal não ponderada, mediana, quartis Q1/Q3 (interpolação linear), IQR, mínimo/máximo e desvio-padrão populacional (ddof=0). `comparacao_2023_2025.csv` contém valores pareados, deltas e decomposição simétrica de P×N. `painel_balanceado.csv` contém os mesmos resumos apenas para municípios com Ideb em todas as edições. São estatísticas entre municípios, sem ponderação por matrículas; não são o Ideb oficial do estado.", ""]
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run(root: Path = ROOT, download: bool = False) -> pd.DataFrame:
    raw = root / "data/raw" / RAW_NAME
    source = read_source(acquire(raw, download))
    tidy = normalize(source)
    write_csv(root / "data/processed/ideb_rj.csv.gz", tidy)
    dictionary(root / "data/data_dictionary.md")
    write_json(root / "data/processed/validacao.json", {
        "sha256_entrada": SHA256, "linhas_origem": len(source), "municipios": 92,
        "linhas_normalizadas": len(tidy), "ideb_validos": int(tidy.ideb.notna().sum()),
        "ideb_ausentes": int(tidy.ideb.isna().sum()), "imputacoes": 0,
        "chaves_duplicadas": 0, "autenticidade_fonte_oficial": "comparacao de bytes pendente"})
    return tidy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Tenta obter entrada ausente da fonte oficial; exige hash fixado.")
    args = parser.parse_args()
    result = run(download=args.download)
    print(f"ETL concluído: {len(result)} linhas; {result.ideb.notna().sum()} Idebs válidos.")
