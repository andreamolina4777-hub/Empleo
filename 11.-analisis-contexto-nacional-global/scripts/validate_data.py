"""Valida respuestas WDI en bruto sin transformar ni imputar valores."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
MANIFEST = RAW_DIR / "wdi_manifest_2020_2025.json"
REPORT = ROOT / "outputs" / "reports" / "data_quality.md"
EXPECTED_COUNTRIES = {"ECU", "VEN", "ARG", "COL"}
EXPECTED_YEARS = set(range(2020, 2026))

if not MANIFEST.exists():
    raise SystemExit("No se encontró el manifiesto de datos brutos. Ejecute download_data.py.")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
lines = ["# Calidad de datos brutos", "", "## Alcance validado", ""]
lines += [
    f"- Fuente: {manifest['source_id']}",
    f"- Descarga (UTC): {manifest['retrieved_at_utc']}",
    "- Cobertura esperada: 4 países × 6 años × 4 indicadores = 96 observaciones.",
    "- Regla: los valores faltantes se reportan y no se imputan.",
    "",
    "## Pruebas", "",
]

critical = []
warnings = []
total_rows = total_missing = total_duplicates = 0
for item in manifest["files"]:
    path = RAW_DIR / item["file"]
    if not path.exists():
        critical.append(f"No existe el archivo {item['file']}.")
        continue
    actual_hash = sha256(path.read_bytes()).hexdigest()
    if actual_hash != item["sha256"]:
        critical.append(f"La huella SHA-256 no coincide para {item['file']}.")
        continue
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload[1]
        if not isinstance(records, list):
            raise ValueError("La sección de registros no es una lista")
    except (IndexError, TypeError, ValueError, json.JSONDecodeError) as error:
        critical.append(f"Esquema inválido en {item['file']}: {error}.")
        continue

    keys = [(row.get("countryiso3code"), row.get("date")) for row in records]
    duplicates = len(keys) - len(set(keys))
    countries = {row.get("countryiso3code") for row in records}
    years = {int(row["date"]) for row in records if row.get("date", "").isdigit()}
    missing = sum(row.get("value") is None for row in records)
    out_of_scope = countries - EXPECTED_COUNTRIES or years - EXPECTED_YEARS
    expected_keys = {(country, str(year)) for country in EXPECTED_COUNTRIES for year in EXPECTED_YEARS}
    absent_keys = expected_keys - set(keys)
    total_rows += len(records)
    total_missing += missing
    total_duplicates += duplicates
    lines.append(
        f"- `{item['variable']}`: integridad SHA-256 correcta; {len(records)} registros; "
        f"{missing} valores nulos; {duplicates} claves duplicadas; {len(absent_keys)} claves país-año ausentes."
    )
    if out_of_scope:
        warnings.append(f"{item['variable']}: cobertura fuera del alcance solicitado.")
    if missing or absent_keys:
        warnings.append(f"{item['variable']}: requiere revisión humana por faltantes antes de procesar.")

lines += ["", "## Resultado", ""]
lines += [
    f"- Registros recibidos: {total_rows}.",
    f"- Valores nulos reportados: {total_missing}.",
    f"- Claves duplicadas: {total_duplicates}.",
    f"- Errores críticos: {len(critical)}.",
    f"- Alertas: {len(warnings)}.",
]
if critical:
    lines += ["", "### Errores críticos", ""] + [f"- {item}" for item in critical]
if warnings:
    lines += ["", "### Alertas", ""] + [f"- {item}" for item in warnings]
lines += ["", "## Acción requerida", "", "- Revisión y aprobación humana del reporte antes de procesar datos."]

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
if critical:
    raise SystemExit(f"Validación con errores críticos. Revise {REPORT}")
print(f"Validación finalizada con {len(warnings)} alertas. Revise {REPORT}")
