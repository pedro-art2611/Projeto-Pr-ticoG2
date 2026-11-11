"""Executa o notebook com o interpretador do ambiente atual, sem kernels globais."""
import os
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_client import KernelManager

root = Path(__file__).resolve().parents[1]
local = root / ".jupyter"
os.environ["JUPYTER_DATA_DIR"] = str(local)
os.environ["JUPYTER_RUNTIME_DIR"] = str(local / "runtime")
from ipykernel.kernelspec import install
install(user=False, prefix=str(local), kernel_name="ideb-rj", display_name="Python (Ideb RJ)")
manager = KernelSpecManager(kernel_dirs=[str(local / "share/jupyter/kernels")])
book = nbformat.read(root / "notebooks/analise_exploratoria.ipynb", as_version=4)
kernel = KernelManager(kernel_name="ideb-rj", kernel_spec_manager=manager)
client = NotebookClient(book, km=kernel, timeout=240, kernel_name="ideb-rj", resources={"metadata": {"path": str(root / "notebooks")}})
client.execute()
output = root / "outputs/analise_exploratoria_executada.ipynb"
output.parent.mkdir(exist_ok=True)
nbformat.write(book, output)
print(f"Notebook executado sem erros; saída: {output}")
