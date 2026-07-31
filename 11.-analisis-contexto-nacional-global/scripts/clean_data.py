"""Construye una tabla procesada a partir de respuestas WDI en bruto aprobadas."""

from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
MANIFEST_PATH = RAW_DIR / "wdi_manifest_2020_2025.json"
CONFIG_PATH = ROOT / "config" / "project_config.yaml"
COUNTRY_NAMES = {"ECU": "Ecuador", "VEN": "Venezuela", "ARG": "Argentina", "COL": "Colombia"}
INDICATOR_NAMES = {
    "SL.EMP.TOTL.SP.ZS": "employment_to_population_15_plus_pct",
    "NY.GDP.PCAP.KD.ZG": "gdp_per_capita_growth_pct",
    "SL.UEM.TOTL.ZS": "unemployment_total_pct",
    "IT.NET.USER.ZS": "internet_users_pct",
}

if not MANIFEST_PATH.exists():
    raise SystemExit("Falta el manifiesto de datos brutos. Ejecute download_data.py.")

project = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["project"]
start_year, end_year = project["period"]["start"], project["period"]["end"]
expected_countries = set(project["countries"])
if expected_countries != set(COUNTRY_NAMES.values()):
    raise SystemExit("Los países configurados no coinciden con el mapeo WDI aprobado.")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
rows = []
for item in manifest["files"]:
    code = item["variable"]
    if code not in INDICATOR_NAMES:
        raise SystemExit(f"Indicador no reconocido: {code}")
    payload = json.loads((RAW_DIR / item["file"]).read_text(encoding="utf-8"))
    for record in payload[1]:
        year = int(record["date"])
        country_code = record["countryiso3code"]
        if start_year <= year <= end_year:
            if country_code not in COUNTRY_NAMES:
                raise SystemExit(f"País no esperado: {country_code}")
            if record["value"] is None:
                raise SystemExit(f"Valor nulo no autorizado: {code}, {country_code}, {year}")
            rows.append({
                "country": COUNTRY_NAMES[country_code],
                "country_code": country_code,
                "year": year,
                "indicator": INDICATOR_NAMES[code],
                "indicator_code": code,
                "value": record["value"],
                "source_id": manifest["source_id"],
                "source_file": item["file"],
            })

expected_rows = len(COUNTRY_NAMES) * (end_year - start_year + 1) * len(INDICATOR_NAMES)
keys = {(row["country_code"], row["year"], row["indicator_code"]) for row in rows}
if len(rows) != expected_rows or len(keys) != expected_rows:
    raise SystemExit(f"Cobertura incompleta o claves duplicadas: {len(rows)} filas, se esperaban {expected_rows}.")

rows.sort(key=lambda row: (row["indicator_code"], row["country_code"], row["year"]))
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
target = PROCESSED_DIR / "indicators.csv"
with target.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

processing_manifest = {
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "input_manifest": MANIFEST_PATH.name,
    "period": {"start": start_year, "end": end_year},
    "rows": len(rows),
    "operation": "Selección de años 2020–2024, normalización de nombres de columnas y consolidación long-form; sin imputación ni modificación de valores.",
}
(PROCESSED_DIR / "processing_manifest.json").write_text(
    json.dumps(processing_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Guardado: {target} ({len(rows)} filas)")
