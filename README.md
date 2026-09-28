# Sistema de registro de donantes

API REST para gestionar usuarios donantes con autenticación JWT y roles.

## Stack
- Python 3.12
- FastAPI
- SQLAlchemy + SQLite
- Pytest + coverage
- GitHub Actions + SonarQube + OWASP ZAP

## Requisitos

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Ejecutar la aplicación

Antes de iniciar, configura un secreto JWT de al menos 32 bytes y una
contraseña de administrador de al menos 12 caracteres. No uses valores
predeterminados ni guardes estas credenciales en el repositorio. En PowerShell:

```powershell
$env:JWT_SECRET_KEY = (& .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))")
$securePassword = Read-Host "Contraseña del administrador (mínimo 12 caracteres)" -AsSecureString
$env:ADMIN_PASSWORD = [System.Net.NetworkCredential]::new("", $securePassword).Password
```

La contraseña configurada se utiliza para crear la cuenta inicial del
administrador, cuyo correo predeterminado es `admin@bloodbank.local`.

```bash
.venv\Scripts\python -m uvicorn app.main:app --reload
```

## Probar la API

```bash
.venv\Scripts\python -m pytest
```

## Endpoints principales

- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`
- `GET /donors`
- `POST /donors`
- `GET /donors/{donor_id}`

El registro público crea cuentas con rol `user`; no acepta asignar roles.
La cuenta inicial `admin` se crea mediante las variables de entorno de
administración.

## Variables de entorno

- `JWT_SECRET_KEY` (obligatoria, mínimo 32 bytes)
- `DATABASE_URL`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD` (obligatoria, mínimo 12 caracteres)

El workflow de GitHub Actions inicia la API en un entorno temporal del runner,
ejecuta el health check y realiza un escaneo OWASP ZAP. El informe se publica
como artefacto de la ejecución. Para SonarQube Cloud, configura el secreto
`SONAR_TOKEN`, el secreto `SONAR_HOST_URL` (`https://sonarcloud.io`) y la
variable de repositorio `SONAR_ORGANIZATION` con la clave de tu organización.
Si no están configurados, el análisis Sonar se omite con una advertencia; las
pruebas y el escaneo ZAP siguen ejecutándose. Puedes iniciar el workflow
manualmente desde la pestaña **Actions** mediante **Run workflow**.
