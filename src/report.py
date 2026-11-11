"""Figuras vetoriais, versões interativas e artigo gerados das mesmas métricas."""
import hashlib
import html
import io
import json
from pathlib import Path
from string import Template

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs

from .etl import ROOT, write_csv, write_json

BLUE, TEAL, ORANGE = "#234a80", "#007f78", "#b65a24"


def figures(results: dict, assets: Path) -> None:
    assets.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "svg.hashsalt": "ideb-rj-v1"})
    d, s, b, p = (results[k] for k in ["data", "summary", "balanced", "paired"])
    plots = {}
    fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    ax.fill_between(s.ano, s.q1, s.q3, alpha=.16, color=BLUE, label="Intervalo interquartil")
    ax.plot(s.ano, s.mediana, "o-", color=BLUE, label="Mediana disponível")
    ax.plot(b.ano, b.mediana, "s--", color=TEAL, label=f"Painel completo (n={results['metrics']['painel_balanceado_n']})")
    ax.set(xlabel="Edição", ylabel="Ideb (0–10)", ylim=(0, 10), xticks=s.ano)
    ax.legend(loc="lower right", frameon=False); ax.grid(axis="y", alpha=.15)
    q = go.Figure()
    q.add_scatter(x=s.ano.tolist(), y=s.q3.tolist(), line=dict(width=0), showlegend=False, hoverinfo="skip")
    q.add_scatter(x=s.ano.tolist(), y=s.q1.tolist(), fill="tonexty", fillcolor="rgba(35,74,128,.15)", line=dict(width=0), name="Q1–Q3")
    q.add_scatter(x=s.ano.tolist(), y=s.mediana.tolist(), mode="lines+markers", name="Mediana disponível", line=dict(color=BLUE), customdata=s.n.tolist(), hovertemplate="%{x}: %{y:.2f}<br>Municípios: %{customdata}<extra></extra>")
    q.add_scatter(x=b.ano.tolist(), y=b.mediana.tolist(), mode="lines+markers", name=f"Painel completo (n={results['metrics']['painel_balanceado_n']})", line=dict(color=TEAL, dash="dash"))
    q.update_yaxes(range=[0, 10], title="Ideb (0–10)"); q.update_xaxes(title="Edição", tickvals=s.ano.tolist())
    plots["evolucao"] = fig, q

    fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    years = sorted(d.ano.unique()); groups = [d.loc[d.ano == y, "ideb"].dropna().to_numpy() for y in years]
    boxes = ax.boxplot(groups, tick_labels=years, patch_artist=True, widths=.55)
    for patch in boxes["boxes"]: patch.set(facecolor="#d7e4f2", edgecolor=BLUE)
    for line in boxes["medians"]: line.set(color=TEAL, linewidth=2)
    ax.set(xlabel="Edição", ylabel="Ideb (0–10)", ylim=(0, 10)); ax.grid(axis="y", alpha=.15)
    q = go.Figure()
    for year, group in zip(years, groups):
        q.add_trace(go.Box(y=group.tolist(), name=str(year), quartilemethod="linear", boxpoints="outliers", marker_color=BLUE, showlegend=False))
    q.update_yaxes(range=[0, 10], title="Ideb (0–10)"); q.update_xaxes(title="Edição")
    plots["distribuicao"] = fig, q

    fig, ax = plt.subplots(figsize=(8, 5.4), layout="constrained")
    colors = {"Aumentou": TEAL, "Diminuiu": ORANGE, "Estável": BLUE}
    q = go.Figure()
    for label, color in colors.items():
        group = p[p.trajetoria == label]
        ax.scatter(group.ideb_2023, group.ideb_2025, color=color, alpha=.8, s=34, label=f"{label} (n={len(group)})")
        q.add_scatter(x=group.ideb_2023.tolist(), y=group.ideb_2025.tolist(), mode="markers", name=f"{label} (n={len(group)})", text=group.municipio.tolist(), marker=dict(color=color, size=9), hovertemplate="%{text}<br>2023: %{x:.1f}<br>2025: %{y:.1f}<extra></extra>")
    ax.plot([0, 10], [0, 10], "--", color="#777777", linewidth=1)
    ax.set(xlabel="Ideb 2023 (0–10)", ylabel="Ideb 2025 (0–10)", xlim=(0, 10), ylim=(0, 10)); ax.legend(frameon=False)
    q.add_shape(type="line", x0=0, y0=0, x1=10, y1=10, line=dict(color="gray", dash="dash"))
    q.update_xaxes(range=[0, 10], title="Ideb 2023 (0–10)"); q.update_yaxes(range=[0, 10], title="Ideb 2025 (0–10)")
    plots["comparacao"] = fig, q

    fig, ax = plt.subplots(figsize=(9, 4.6), layout="constrained")
    labels = ["Rendimento (P)", "Nota padronizada (N)", "Variação do produto P×N"]
    values = [p.contribuicao_rendimento.mean(), p.contribuicao_nota.mean(), p.delta_produto.mean()]
    ax.barh(labels, values, color=[TEAL, BLUE, "#667085"])
    for i, v in enumerate(values): ax.text(v + .008, i, f"{v:.3f}".replace(".", ","), va="center")
    ax.set(xlabel="Contribuição média / variação média (pontos)", xlim=(min(0, min(values))-.02, max(values)+.09)); ax.axvline(0, color="#777777", linewidth=.7)
    q = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=[TEAL, BLUE, "#667085"], hovertemplate="%{y}: %{x:.3f}<extra></extra>"))
    q.update_xaxes(title="Contribuição média / variação média (pontos)")
    plots["componentes"] = fig, q
    for name, (static, interactive) in plots.items():
        buffer = io.StringIO()
        static.savefig(buffer, format="svg", metadata={"Date": None, "Creator": "Projeto Ideb RJ"})
        (assets / f"{name}.svg").write_text(buffer.getvalue(), encoding="utf-8", newline="\n")
        plt.close(static)
        interactive.update_layout(template="plotly_white", autosize=True, margin=dict(l=50, r=20, t=25, b=60), font=dict(family="Arial", size=13), legend=dict(orientation="h", y=-.25))
        (assets / f"{name}.json").write_text(interactive.to_json(pretty=False, remove_uids=True), encoding="utf-8", newline="\n")
    (assets / "plotly.min.js").write_text(get_plotlyjs(), encoding="utf-8", newline="\n")
    write_csv(assets / "resumo_por_edicao.csv", s)
    write_csv(assets / "comparacao_2023_2025.csv", p)


def fmt(value, decimals=2):
    return f"{value:.{decimals}f}".replace(".", ",")


def render(results: dict, root: Path = ROOT) -> None:
    figures(results, root / "docs/assets")
    m = results["metrics"]
    values = {k: fmt(v) if isinstance(v, float) else str(v) for k, v in m.items()}
    for key in ["iqr_2005", "iqr_2025", "dp_2005", "dp_2025"]:
        values[key] = fmt(m[key], 3)
    values["delta_p_pp"] = fmt(100 * m["delta_p_medio"])
    values["aumentou_pct"] = fmt(100 * m["aumentou"] / m["pares"], 1)
    values["iqr_direcao"] = "aumentou" if m["iqr_2025"] > m["iqr_2005"] else "diminuiu" if m["iqr_2025"] < m["iqr_2005"] else "permaneceu constante"
    values["tabela"] = "\n".join("<tr>" + "".join(f"<td>{html.escape(str(int(row[k])) if k in ['ano','n','ausentes'] else fmt(row[k], 3))}</td>" for k in ["ano", "n", "ausentes", "mediana", "q1", "q3", "iqr", "desvio_padrao"]) + "</tr>" for _, row in results["summary"].iterrows())
    values["contribuicao_p_media"] = fmt(m["contribuicao_p_media"], 3)
    values["contribuicao_n_media"] = fmt(m["contribuicao_n_media"], 3)
    values["delta_produto_medio"] = fmt(m["delta_produto_medio"], 3)
    values["delta_medio"] = fmt(m["delta_medio"], 3)
    template = Template((root / "src/article.html").read_text(encoding="utf-8"))
    (root / "docs/index.html").write_text(template.substitute(values), encoding="utf-8", newline="\n")
    outputs = sorted(list((root / "data/processed").glob("*")) + [root / "docs/index.html", root / "data/data_dictionary.md"] + list((root / "docs/assets").glob("*")))
    write_json(root / "reproducibilidade.json", {str(p.relative_to(root)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs})


if __name__ == "__main__":
    from .etl import run
    from .analysis import analyze
    render(analyze(run()))
    print("Pipeline, figuras e artigo gerados.")
