"""Genera resumen descriptivo y matriz del modelo desde datos procesados."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "indicators.csv"
REPORT = ROOT / "outputs" / "reports" / "economic_analysis.md"
MODEL = ROOT / "data" / "processed" / "model_data.csv"
PUBLIC_TARGETS = [ROOT / "public" / "data" / "indicators.json", ROOT / "dashboard" / "public" / "data" / "indicators.json"]

with INPUT.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
values = {(r["country"], int(r["year"]), r["indicator"]): float(r["value"]) for r in rows}
countries = sorted({r["country"] for r in rows})
years = sorted({int(r["year"]) for r in rows})
needed = ["employment_to_population_15_plus_pct", "internet_users_pct", "gdp_per_capita_growth_pct", "unemployment_total_pct"]

MODEL.parent.mkdir(parents=True, exist_ok=True)
with MODEL.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["country", "year", "y", "internet_users_pct", "gdp_per_capita_growth_pct"])
    writer.writeheader()
    for country in countries:
        for year in years:
            writer.writerow({"country": country, "year": year, "y": values[country, year, needed[0]], "internet_users_pct": values[country, year, needed[1]], "gdp_per_capita_growth_pct": values[country, year, needed[2]]})

lines = ["# Análisis económico descriptivo", "", "## Alcance", "", "- Países: Ecuador, Venezuela, Argentina y Colombia.", "- Periodo: 2020–2024; datos WDI con indicador digital de fuente primaria UIT.", "- Este análisis describe patrones; no identifica efectos causales.", "", "## Evolución 2020–2024", "", "| País | Internet 2020 | Internet 2024 | Variación (pp) | Empleo 2020 | Empleo 2024 | Variación (pp) | Crecimiento PIB pc promedio | Desempleo promedio |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for country in countries:
    internet0, internet4 = values[country, 2020, needed[1]], values[country, 2024, needed[1]]
    employment0, employment4 = values[country, 2020, needed[0]], values[country, 2024, needed[0]]
    gdp_avg = sum(values[country, year, needed[2]] for year in years) / len(years)
    unemp_avg = sum(values[country, year, needed[3]] for year in years) / len(years)
    lines.append(f"| {country} | {internet0:.2f} | {internet4:.2f} | {internet4-internet0:.2f} | {employment0:.2f} | {employment4:.2f} | {employment4-employment0:.2f} | {gdp_avg:.2f} | {unemp_avg:.2f} |")
lines += ["", "## Lectura", "", "- Las diferencias entre países y los cambios simultáneos en empleo, conectividad y actividad económica impiden atribuir causalidad a una sola variable.", "- El desempleo se conserva como indicador descriptivo y no se incluye como control del modelo por su relación contable con el empleo.", "- La interpretación econométrica debe considerar solo 20 observaciones país-año."]
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
labels = {"employment_to_population_15_plus_pct": "Empleo/población, 15+ (%)", "internet_users_pct": "Uso de internet (% de población)", "gdp_per_capita_growth_pct": "Crecimiento anual del PIB real per cápita (%)", "unemployment_total_pct": "Desempleo total (% de la fuerza laboral)"}
public_rows = [{"country": row["country"], "year": int(row["year"]), "indicator": labels[row["indicator"]], "value": float(row["value"]), "source": "Banco Mundial, WDI; uso de internet: UIT", "period": "2020–2024"} for row in rows]
for target in PUBLIC_TARGETS:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(public_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Resultados: {REPORT} y {MODEL}")
