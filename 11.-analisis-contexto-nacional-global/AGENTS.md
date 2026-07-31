# Instrucciones para asistentes de IA

## Propósito

Apoyar un análisis económico reproducible, trazable y validado por el equipo humano.

## Reglas obligatorias

1. Leer `config/project_config.yaml`, `config/tasks.yaml` y el archivo del agente correspondiente antes de actuar.
2. No inventar datos, fuentes, DOI, resultados, fechas ni citas.
3. Registrar toda fuente en `config/sources.yaml`.
4. Conservar datos originales en `data/raw/`; escribir transformaciones en `data/processed/`.
5. Documentar cada ejecución material en `docs/bitacora_agentes.md`.
6. Señalar supuestos, incertidumbre y limitaciones.
7. No publicar resultados sin revisión humana y auditoría.
8. No guardar secretos. Utilizar variables definidas en `.env.example`.
9. Ejecutar las pruebas proporcionales al cambio.
10. Mantener coherencia entre datos, dashboard, informe y presentación.

## Criterio de finalización

Una tarea termina solo si existe el archivo de salida, evidencia de validación, trazabilidad de fuentes y aprobación humana registrada.
