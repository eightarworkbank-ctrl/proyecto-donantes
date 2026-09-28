# Informe final del proyecto

## 1. Objetivo
Implementar una API para registrar personas donantes con autenticación JWT, gestión de roles y pruebas de calidad.

## 2. Comparación entre planificación e implementación

| Área | Planificación | Implementación |
|---|---|---|
| Arquitectura | FastAPI + SQLAlchemy + SQLite | FastAPI + SQLAlchemy + SQLite |
| Seguridad | JWT y control de permisos | JWT con `Bearer`, registro público limitado al rol `user` y permisos de administrador verificados |
| Pruebas | Pytest + cobertura > 80% | Pytest + cobertura superior al 80% |
| CI/CD | GitHub Actions con pruebas y análisis | API levantada en un entorno temporal del runner para health check y análisis de seguridad |
| Calidad y seguridad | Aikido y OWASP ZAP | Aikido integrado con el repositorio para análisis de seguridad; GitHub Actions ejecuta ZAP y conserva su informe como artefacto |

## 3. Lecciones aprendidas
- La separación de modelos, esquemas y dependencias facilita la escalabilidad.
- Las pruebas automatizadas permiten detectar regresiones antes del despliegue.
- La autenticación basada en JWT requiere validación estricta de expiración y roles.
- La documentación y la automatización reducen el riesgo de errores operativos.

## 4. Plan de mejora
- Añadir persistencia real con PostgreSQL.
- Mejorar validaciones y permisos por recurso.
- Integrar un entorno de despliegue real y monitorización.
- Añadir pruebas E2E y análisis de seguridad más completo.

## 5. Conclusión
El proyecto queda estructurado desde cero con una base funcional, automatización y evidencia de calidad, preparada para ampliarse en fases posteriores.
