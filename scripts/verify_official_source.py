"""Refaz a comparação com o endereço oficial, sem alterar a entrada fixada.

HTTP é explícito porque HTTPS falhou na coleta. O hash identifica a versão
fixada; HTTP não oferece autenticação TLS do transporte.
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.etl import ROOT, RAW_NAME, SHA256

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--https", action="store_true", help="Usa HTTPS em vez do HTTP explicitamente documentado.")
args = parser.parse_args()
scheme = "https" if args.https else "http"
url = f"{scheme}://download.inep.gov.br/ideb/resultados/{RAW_NAME}"
with urllib.request.urlopen(url, timeout=90) as response:
    payload = response.read()
    effective_url = response.geturl()
digest = hashlib.sha256(payload).hexdigest()
equal = payload == (ROOT / "data/raw" / RAW_NAME).read_bytes()
print(json.dumps({"requested_url": url, "effective_url": effective_url,
                  "bytes": len(payload), "sha256": digest, "byte_equal": equal}, indent=2))
if digest != SHA256 or not equal:
    raise SystemExit("A entrada oficial difere da versão fixada: revisão necessária.")
