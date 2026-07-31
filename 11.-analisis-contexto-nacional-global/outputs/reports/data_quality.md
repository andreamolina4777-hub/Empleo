# Calidad de datos brutos

## Alcance validado

- Fuente: banco_mundial_wdi_empleo_pib_desempleo
- Descarga (UTC): 2026-07-31T05:51:03.827869+00:00
- Cobertura esperada: 4 países × 6 años × 4 indicadores = 96 observaciones.
- Regla: los valores faltantes se reportan y no se imputan.

## Pruebas

- `SL.EMP.TOTL.SP.ZS`: integridad SHA-256 correcta; 24 registros; 0 valores nulos; 0 claves duplicadas; 0 claves país-año ausentes.
- `NY.GDP.PCAP.KD.ZG`: integridad SHA-256 correcta; 24 registros; 0 valores nulos; 0 claves duplicadas; 0 claves país-año ausentes.
- `SL.UEM.TOTL.ZS`: integridad SHA-256 correcta; 24 registros; 0 valores nulos; 0 claves duplicadas; 0 claves país-año ausentes.
- `IT.NET.USER.ZS`: integridad SHA-256 correcta; 24 registros; 4 valores nulos; 0 claves duplicadas; 0 claves país-año ausentes.

## Resultado

- Registros recibidos: 96.
- Valores nulos reportados: 4.
- Claves duplicadas: 0.
- Errores críticos: 0.
- Alertas: 1.

### Alertas

- IT.NET.USER.ZS: requiere revisión humana por faltantes antes de procesar.

## Acción requerida

- Revisión y aprobación humana del reporte antes de procesar datos.
