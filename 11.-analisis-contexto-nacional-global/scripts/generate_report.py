from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
if not shutil.which("quarto"):
    raise SystemExit("Quarto no está instalado. Instálelo desde https://quarto.org/")
subprocess.run(["quarto", "render", str(ROOT / "report/informe.qmd")], check=True)
print("Informe generado. Revise visualmente el PDF antes de publicar.")
