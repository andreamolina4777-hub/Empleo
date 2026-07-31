from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_tasks():
    with (ROOT / "config/tasks.yaml").open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)["tasks"]

def status():
    print("ESTADO DEL PROYECTO")
    for task in load_tasks():
        target = ROOT / task["output"]
        if target.is_dir():
            done = any(p.name != ".gitkeep" for p in target.iterdir())
        elif target.is_file():
            text = target.read_text(encoding="utf-8", errors="ignore")
            markers = ("POR DEFINIR", "Pendiente", "PENDIENTE", "EJEMPLO_NO_USAR", "demostración")
            done = bool(text.strip()) and not any(marker in text for marker in markers)
        else:
            done = False
        gate = " · aprobación humana" if task.get("human_gate") else ""
        print(f"[{'x' if done else ' '}] {task['id']} → {task['output']}{gate}")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "status":
        status()
    else:
        raise SystemExit("Uso: python scripts/project_cli.py status")
