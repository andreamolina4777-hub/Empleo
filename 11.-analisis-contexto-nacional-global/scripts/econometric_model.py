"""OLS exploratorio con efectos fijos por país y errores robustos HC3."""
from pathlib import Path
import csv
from math import erfc, sqrt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "model_data.csv"
TABLE = ROOT / "outputs" / "tables" / "model_results.csv"
REPORT = ROOT / "outputs" / "reports" / "econometric_results.md"

with INPUT.open(encoding="utf-8") as f:
    data = list(csv.DictReader(f))
countries = sorted({row["country"] for row in data})
base = countries[0]
X, y = [], []
for row in data:
    country = row["country"]
    X.append([1.0] + [1.0 if country == item else 0.0 for item in countries[1:]] + [float(row["internet_users_pct"]), float(row["gdp_per_capita_growth_pct"])])
    y.append(float(row["y"]))
X, y = np.asarray(X), np.asarray(y)
beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
residuals = y - X @ beta
xtx_inv = np.linalg.inv(X.T @ X)
leverage = np.sum((X @ xtx_inv) * X, axis=1)
meat = sum(((residuals[i] / (1 - leverage[i])) ** 2) * np.outer(X[i], X[i]) for i in range(len(y)))
se = np.sqrt(np.diag(xtx_inv @ meat @ xtx_inv))
names = ["Intercepto (Ecuador)"] + [f"Efecto fijo: {item}" for item in countries[1:]] + ["Uso de internet (%)", "Crecimiento PIB real per cápita (%)"]
TABLE.parent.mkdir(parents=True, exist_ok=True)
with TABLE.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["parameter", "estimate", "robust_se_hc3", "t_stat", "normal_approx_p_value", "ci_95_low", "ci_95_high"])
    writer.writeheader()
    for name, estimate, error in zip(names, beta, se):
        t = estimate / error
        writer.writerow({"parameter": name, "estimate": estimate, "robust_se_hc3": error, "t_stat": t, "normal_approx_p_value": erfc(abs(t) / sqrt(2)), "ci_95_low": estimate - 1.96 * error, "ci_95_high": estimate + 1.96 * error})
r2 = 1 - float(np.sum(residuals ** 2) / np.sum((y - y.mean()) ** 2))
lines = ["# Resultados econométricos exploratorios", "", "## Especificación", "", "`empleo_it = α_i + β·internet_it + γ·crecimiento_PIBpc_it + ε_it`", "", f"- Observaciones: {len(y)}; países: {len(countries)}; años: 2020–2024.", f"- Efectos fijos por país; país de referencia: {base}.", "- Errores estándar HC3. Los valores p usan aproximación normal y son solo orientativos con cuatro países.", f"- R² dentro de la especificación: {r2:.3f}.", "", "## Interpretación y límites", "", "- Los coeficientes reflejan asociaciones condicionales, no efectos causales.", "- No se incluyen efectos fijos de año por el tamaño limitado de la muestra.", "- La inferencia es frágil: 20 observaciones y cuatro unidades de país no permiten conclusiones concluyentes."]
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Resultados: {TABLE} y {REPORT}")
