"""Estatística descritiva e comparações pareadas, sem inferência causal."""
from pathlib import Path
import numpy as np
import pandas as pd
from .etl import ROOT, write_csv, write_json


def summarize(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, group in data.groupby("ano", sort=True):
        x = group.ideb.dropna()
        q1, q3 = x.quantile([0.25, 0.75])
        rows.append(dict(ano=int(year), n=len(x), ausentes=int(group.ideb.isna().sum()),
                         media=x.mean(), mediana=x.median(), q1=q1, q3=q3, iqr=q3-q1,
                         desvio_padrao=x.std(ddof=0), minimo=x.min(), maximo=x.max()))
    return pd.DataFrame(rows)


def analyze(data: pd.DataFrame, root: Path = ROOT) -> dict:
    summary = summarize(data)
    panel_ids = data.groupby("codigo_municipio").ideb.count().loc[lambda s: s == 11].index
    balanced = summarize(data[data.codigo_municipio.isin(panel_ids)])
    cols = ["codigo_municipio", "municipio", "ideb", "rendimento", "nota_padronizada"]
    before, after = (data.loc[data.ano == year, cols] for year in [2023, 2025])
    paired = before.merge(after, on=["codigo_municipio", "municipio"], suffixes=("_2023", "_2025"), validate="one_to_one")
    paired = paired.dropna(subset=["ideb_2023", "ideb_2025", "rendimento_2023", "rendimento_2025", "nota_padronizada_2023", "nota_padronizada_2025"]).copy()
    for metric in ["ideb", "rendimento", "nota_padronizada"]:
        paired["delta_" + metric] = paired[metric + "_2025"] - paired[metric + "_2023"]
    paired["contribuicao_rendimento"] = (paired.nota_padronizada_2023 + paired.nota_padronizada_2025) / 2 * paired.delta_rendimento
    paired["contribuicao_nota"] = (paired.rendimento_2023 + paired.rendimento_2025) / 2 * paired.delta_nota_padronizada
    paired["delta_produto"] = paired.rendimento_2025 * paired.nota_padronizada_2025 - paired.rendimento_2023 * paired.nota_padronizada_2023
    paired["residuo_arredondamento"] = paired.delta_ideb - paired.delta_produto
    paired["trajetoria"] = np.select([paired.delta_ideb > 1e-9, paired.delta_ideb < -1e-9], ["Aumentou", "Diminuiu"], default="Estável")
    for name, frame in [("resumo_por_edicao", summary), ("painel_balanceado", balanced), ("comparacao_2023_2025", paired)]:
        write_csv(root / f"data/processed/{name}.csv", frame)
    s = summary.set_index("ano")
    metrics = {
        "municipios": 92, "edicoes": 11, "observacoes": len(data), "validos": int(data.ideb.count()),
        "ausentes": int(data.ideb.isna().sum()), "painel_balanceado_n": len(panel_ids),
        "mediana_2005": float(s.loc[2005, "mediana"]), "mediana_2025": float(s.loc[2025, "mediana"]),
        "iqr_2005": float(s.loc[2005, "iqr"]), "iqr_2025": float(s.loc[2025, "iqr"]),
        "dp_2005": float(s.loc[2005, "desvio_padrao"]), "dp_2025": float(s.loc[2025, "desvio_padrao"]),
        "pares": len(paired), "aumentou": int((paired.trajetoria == "Aumentou").sum()),
        "diminuiu": int((paired.trajetoria == "Diminuiu").sum()), "estavel": int((paired.trajetoria == "Estável").sum()),
        "delta_medio": float(paired.delta_ideb.mean()), "delta_mediano": float(paired.delta_ideb.median()),
        "delta_p_medio": float(paired.delta_rendimento.mean()),
        "delta_n_medio": float(paired.delta_nota_padronizada.mean()),
        "contribuicao_p_media": float(paired.contribuicao_rendimento.mean()),
        "contribuicao_n_media": float(paired.contribuicao_nota.mean()),
        "delta_produto_medio": float(paired.delta_produto.mean()),
        "painel_mediana_2005": float(balanced.iloc[0].mediana),
        "painel_mediana_2025": float(balanced.iloc[-1].mediana),
    }
    write_json(root / "data/processed/metricas.json", metrics)
    return {"data": data, "summary": summary, "balanced": balanced, "paired": paired, "metrics": metrics}
