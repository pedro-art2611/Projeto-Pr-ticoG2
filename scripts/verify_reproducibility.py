"""Refaz o pipeline e compara os hashes com a referência versionada."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.etl import ROOT, run
from src.analysis import analyze
from src.report import render

reference = json.loads((ROOT / "reproducibilidade.json").read_text(encoding="utf-8"))
render(analyze(run()))
current = json.loads((ROOT / "reproducibilidade.json").read_text(encoding="utf-8"))
differences = sorted(k for k in reference.keys() | current.keys() if reference.get(k) != current.get(k))
if differences:
    # Preserva a referência mesmo quando a reprodução falha.
    from src.etl import write_json
    write_json(ROOT / "reproducibilidade.json", reference)
    raise SystemExit("Produtos divergentes: " + ", ".join(differences))
print(f"Reprodução idêntica: {len(reference)} produtos conferidos por SHA-256.")
