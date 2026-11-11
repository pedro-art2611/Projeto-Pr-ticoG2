"""Gera o notebook de exploração com UTF-8 e IDs de célula estáveis."""
from pathlib import Path
import nbformat as nb

root = Path(__file__).resolve().parents[1]
markdown = nb.v4.new_markdown_cell
code = nb.v4.new_code_cell
cells = [
    markdown("""# Ideb nas redes municipais fluminenses: análise exploratória
**Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva**<br>
Unilasalle-RJ · Sistemas de Informação · Linguagem de Programação · 6º período · 2026

Recorte: RJ, rede Municipal, anos iniciais, 2005 a 2025. A fonte é a cópia arquivada documentada em `proveniencia.json`; a comparação dos bytes com a fonte oficial permanece pendente. Não há imputação nem inferência causal.

RQ1: como evoluiu o nível central? RQ2: como variou a dispersão? RQ3: como mudaram o índice e seus componentes entre 2023 e 2025?"""),
    code('''from pathlib import Path
import sys
ROOT = Path.cwd().resolve()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.etl import run
from src.analysis import analyze
from src.report import figures
import pandas as pd
from IPython.display import display, SVG

data = run(ROOT)
results = analyze(data, ROOT)
figures(results, ROOT / "docs/assets")
display(data.head())'''),
    markdown("""## Ingestão e cobertura
As funções de `src` verificam hash e schema e preservam códigos de ausência. A linha é município × edição. As colunas `_original` retêm os marcadores, sem substituí-los por zero."""),
    code('''display(data.groupby("ano").agg(municipios=("codigo_municipio", "nunique"), ideb_validos=("ideb", "count")))
display(data.loc[data.ideb.isna(), ["codigo_municipio", "municipio", "ano", "ideb_original"]])
assert len(data) == 1012
assert data.ideb.isna().sum() == 14
assert not data.duplicated(["codigo_municipio", "rede", "etapa", "ano"]).any()'''),
    markdown("""## RQ1: Nível central e painel completo
Mediana de todos os resultados disponíveis e painel dos mesmos municípios em todas as edições. A faixa é Q1 a Q3, não intervalo de confiança. Cada município recebe igual peso."""),
    code('''display(results["summary"])
display(results["balanced"])
display(SVG(filename=str(ROOT / "docs/assets/evolucao.svg")))
m = results["metrics"]
print(f"Medianas: {m['mediana_2005']:.1f} → {m['mediana_2025']:.1f}; painel completo: {m['painel_balanceado_n']} municípios.")'''),
    markdown("""## RQ2: Dispersão e extremos
Quartis com interpolação linear; desvio-padrão populacional (ddof=0). Extremos pelo critério de 1,5 IQR são inspecionados e mantidos, não classificados automaticamente como erros."""),
    code('''display(SVG(filename=str(ROOT / "docs/assets/distribuicao.svg")))
last = data.loc[data.ano == 2025].dropna(subset=["ideb"])
q1, q3 = last.ideb.quantile([.25, .75]); iqr = q3 - q1
extremos = last.loc[(last.ideb < q1 - 1.5*iqr) | (last.ideb > q3 + 1.5*iqr), ["codigo_municipio", "municipio", "ideb"]]
display(extremos)
print(f"IQR: {m['iqr_2005']:.3f} → {m['iqr_2025']:.3f}. Nenhum extremo removido.")'''),
    markdown("""## RQ3: Pares 2023 a 2025 e identidade do índice
A junção é um a um, com 92 pares completos. A decomposição simétrica é Δ(PN) = média(N)ΔP + média(P)ΔN. É algébrica, não causal. A diferença para ΔIdeb divulgado é o residual de arredondamento."""),
    code('''paired = results["paired"]
display(paired.trajetoria.value_counts())
display(paired[["municipio", "delta_ideb", "contribuicao_rendimento", "contribuicao_nota", "residuo_arredondamento"]])
display(SVG(filename=str(ROOT / "docs/assets/comparacao.svg")))
display(SVG(filename=str(ROOT / "docs/assets/componentes.svg")))
import numpy as np
np.testing.assert_allclose(paired.contribuicao_rendimento + paired.contribuicao_nota, paired.delta_produto, atol=1e-12)
print(f"Aumentaram: {m['aumentou']}; diminuíram: {m['diminuiu']}; estáveis: {m['estavel']}.")'''),
    markdown("""## Síntese, limites e reprodução
A mediana aumentou entre os extremos; o IQR também aumentou, sem convergência uniforme. Na comparação recente predominam aumentos, com contribuições médias positivas de P e N. Essas conclusões não identificam causas nem desigualdades individuais.

2021 exige cautela; cobertura variável, arredondamento, agregação e origem em espelho limitam a interpretação. Licença dos dados e comparação dos bytes oficiais estão pendentes. Código MIT; texto e figuras autorais CC BY 4.0. Veja `data/data_dictionary.md`, `README.md`, `VALIDACAO.md` e as referências do artigo em `docs/index.html`. A execução integral usa `python -m src.report`."""),
]
book = nb.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3 (Ideb RJ)", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.14.7"}})
for index, cell in enumerate(book.cells):
    cell.id = f"ideb-{index:02d}"
(root / "notebooks/analise_exploratoria.ipynb").write_text(nb.writes(book), encoding="utf-8", newline="\n")
