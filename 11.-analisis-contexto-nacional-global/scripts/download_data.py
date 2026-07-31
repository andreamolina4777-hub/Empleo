"""Descarga sin transformación series WDI aprobadas y registra sus huellas SHA-256."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import ssl
import yaml
import truststore
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
COUNTRIES = "ECU;VEN;ARG;COL"
YEARS = "2020:2025"
WDI_SOURCE_ID = "banco_mundial_wdi_empleo_pib_desempleo"

sources = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8"))["sources"]
wdi_source = next((item for item in sources if item["id"] == WDI_SOURCE_ID), None)
if not wdi_source or wdi_source.get("status") != "APROBADA":
    raise SystemExit("La fuente WDI no está aprobada para descarga.")

RAW_DIR.mkdir(parents=True, exist_ok=True)
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
manifest = {
    "source_id": WDI_SOURCE_ID,
    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
    "countries": COUNTRIES.split(";"),
    "requested_years": YEARS,
    "files": [],
}

for variable in wdi_source["variables"]:
    code = variable["code"]
    url = (
        f"https://api.worldbank.org/v2/country/{COUNTRIES}/indicator/{code}"
        f"?date={YEARS}&format=json&per_page=100"
    )
    request = Request(url, headers={"User-Agent": "UTC-economia-proyecto/1.0"})
    with urlopen(request, timeout=60, context=ssl_context) as response:
        content = response.read()
    target = RAW_DIR / f"wdi_{code}_ECU_VEN_ARG_COL_2020_2025.json"
    target.write_bytes(content)
    manifest["files"].append(
        {"file": target.name, "variable": code, "url": url, "sha256": sha256(content).hexdigest()}
    )

(RAW_DIR / "wdi_manifest_2020_2025.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Descargadas {len(manifest['files'])} series WDI en {RAW_DIR}")
