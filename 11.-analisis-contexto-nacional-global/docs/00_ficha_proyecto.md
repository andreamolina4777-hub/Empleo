# Ficha de definición del proyecto

## Equipo

| Integrante | Rol humano | Usuario GitHub | Responsabilidad |
|---|---|---|---|
| Andrea Nicole Molina Molina | Por definir | | Por definir |
| | Responsable de datos | | |
| | Responsable de análisis | | |
| | Responsable de dashboard | | |
| | Responsable de informe | | |

## Problema y alcance

- Problema económico: Transformación digital y empleo.
- Pregunta central: ¿Cómo se relaciona el avance de la conectividad digital con la tasa de empleo de la población de 15 años o más en Ecuador, Argentina, Venezuela y Colombia durante 2020–2024?
- Justificación para Ecuador: Analizar la asociación entre conectividad digital y empleo en Ecuador y contrastarla con tres economías latinoamericanas.
- Países o regiones de comparación: Venezuela, Argentina y Colombia.
- Periodo y frecuencia: 2020–2024; anual. Se excluye 2025 porque el indicador de uso de internet no cuenta con valores comparables para los cuatro países, y 2026 no dispone aún de observaciones anuales comparables.
- Unidad de análisis: país-año.
- Población o cobertura: población de 15 años o más para los indicadores laborales; población total para conectividad digital.

## Objetivos

- Objetivo general: Analizar la relación entre conectividad digital y empleo en Ecuador, Argentina, Venezuela y Colombia durante 2020–2024.
- Objetivo específico 1: Describir la evolución del uso de internet y del empleo en los cuatro países.
- Objetivo específico 2: Comparar los indicadores laborales y digitales de Ecuador con los países seleccionados.
- Objetivo específico 3: Estimar de forma exploratoria la asociación entre uso de internet y tasa de empleo, controlando por crecimiento real del PIB per cápita.

## Indicadores y teoría

| Indicador | Definición | Unidad | Fuente prevista | Relación teórica |
|---|---|---|---|---|
| Personas que usan internet | Proporción de personas que usaron internet desde cualquier ubicación en los últimos tres meses | % de la población | UIT DataHub | Mayor conectividad puede ampliar el acceso a información, mercados y oportunidades laborales; la relación será evaluada como asociación, no causalidad. |
| Tasa de empleo/población, 15+ | Proporción de la población de 15 años o más que está empleada | % de población 15+ | Banco Mundial, WDI (estimación modelada OIT) | Variable de resultado laboral. |
| Crecimiento anual del PIB real per cápita | Variación porcentual anual del PIB real por habitante | % anual | Banco Mundial, WDI | Controla parcialmente el ciclo y desempeño económico. |
| Tasa de desempleo total | Proporción de la fuerza laboral sin empleo, disponible y en búsqueda de trabajo | % de fuerza laboral | Banco Mundial, WDI (estimación modelada OIT) | Indicador complementario; no se incluirá simultáneamente como control de la tasa de empleo por su relación mecánica. |

## Decisiones

- Método estadístico/econométrico previsto: Análisis descriptivo de series país-año y regresión exploratoria de efectos fijos por país: Empleo_it = α_i + β Internet_it + γ CrecimientoPIBpc_it + ε_it. El resultado se interpretará como asociación, no como efecto causal.
- Riesgos de datos: Observaciones anuales incompletas o no comparables, especialmente para Venezuela; disponibilidad desigual del indicador de internet; muestra pequeña (4 países × hasta 6 años), que limita la inferencia estadística.
- Resultado mínimo viable: Base de datos trazable y validada, gráficos comparativos y estimación exploratoria con sus limitaciones documentadas.
- Criterios para declarar terminado el proyecto: Fuentes aprobadas y registradas, datos validados, productos consistentes, auditoría independiente y aprobación humana final.

## Aprobación humana

- Fecha: 2026-07-31.
- Responsable: Andrea Nicole Molina Molina.
- Decisión: Aprobado el alcance: países, periodo analítico 2020–2024, pregunta de investigación, indicadores y método econométrico exploratorio. Aprobado procesar los datos validados sin imputar los valores faltantes de 2025.
