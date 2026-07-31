# Análisis del contexto nacional y global

Plantilla operativa para el proyecto integrador multiagéntico de octavo semestre de la Carrera de Economía. El repositorio coordina recopilación, validación, análisis, visualización, informe y auditoría.

## Equipo y definición inicial

Complete antes de ejecutar:

- Integrantes: **POR DEFINIR**
- Problema económico: **POR DEFINIR**
- Ecuador y economías de comparación: **POR DEFINIR**
- Periodo e indicadores: **POR DEFINIR**
- Repositorio GitHub: **POR DEFINIR**
- Dashboard Vercel: **POR DEFINIR**

La ficha editable está en [docs/00_ficha_proyecto.md](docs/00_ficha_proyecto.md).

## Arquitectura

El coordinador asigna tareas a ocho agentes especializados. Los resultados pasan por validación de datos, revisión humana y auditoría antes de publicarse. Los roles se definen en `config/agents.yaml`, el flujo en `config/tasks.yaml` y la evidencia se registra en `docs/bitacora_agentes.md`.

## Inicio rápido en Visual Studio Code

Requisitos: Python 3.11+, Node.js 20+, Git y VS Code.

```bash
git init
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
npm install
npm run dev
```

Abra <http://localhost:3000>. Los datos de ejemplo están en `public/data/indicators.json`.

## Flujo reproducible

```bash
python scripts/project_cli.py status
python scripts/download_data.py
python scripts/clean_data.py
python scripts/validate_data.py
python scripts/calculate_indicators.py
python scripts/econometric_model.py
pytest
npm run build
```

Los scripts son esqueletos seguros: no inventan datos y se detienen cuando falta una fuente o configuración. Reemplace los ejemplos únicamente con datos verificables.

## Generación del informe

Edite `report/informe.qmd`. Con Quarto instalado:

```bash
quarto render report/informe.qmd
```

El PDF resultante debe copiarse a `public/informe_final.pdf` para permitir su descarga pública.

## Despliegue

1. Cree el repositorio en GitHub y suba commits frecuentes.
2. Importe el repositorio en Vercel.
3. Mantenga el directorio raíz del proyecto.
4. Use `npm run build` y publique.
5. Registre las URL en esta página y en `config/project_config.yaml`.

## Resultados, fuentes y limitaciones

Se completan después de ejecutar el análisis. Ninguna conclusión debe publicarse si no puede rastrearse hasta una fuente registrada en `config/sources.yaml`.

## Licencia

Código bajo licencia MIT. Los datos conservan las condiciones de sus instituciones de origen.
