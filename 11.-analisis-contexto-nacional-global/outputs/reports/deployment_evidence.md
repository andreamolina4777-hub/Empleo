# Evidencia de Despliegue y Publicación

- **Fecha de Registro:** 2026-07-31
- **Responsable:** Coordinación del proyecto

## 1. Verificación del Build Local

- **Framework:** Next.js (Dashboard interactivo)
- **Comando:** `npm run build`
- **Estado de Compilación:** Compilación estática/SSR limpia.
- **Archivos públicos verificados:**
  - `public/data/indicators.json` (Datos para gráficos y tablas del dashboard)
  - `public/informe_final.pdf` (Descarga pública del informe en PDF)

## 2. Configuración de Repositorios y Servicios

- **Repositorio GitHub:** Configurado localmente. Enlace a registrar en `config/project_config.yaml`.
- **Servicio de Despliegue:** Vercel / Next.js hosting.
- **Configuración de Vercel:** Archivo `vercel.json` presente en raíz.

## 3. Registro de URLs y Estado Final

| Recurso | URL | Estado |
|---|---|---|
| Repositorio de Código | (Registrar URL de GitHub) | Preparado para push |
| Dashboard Interactivo | (Registrar URL de Vercel) | Preparado para importación en Vercel |
| Informe PDF Descargable | `/informe_final.pdf` | Disponible en `public/` |

## 4. Conformidad Humana

- **Firma / Aprobación Humana:** Andrea Nicole Molina Molina
- **Decisión:** Autorizado el despliegue del dashboard y la publicación de los productos finales.
