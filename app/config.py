import os

APP_NAME = os.getenv("APP_NAME", "Donantes API")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if len(JWT_SECRET_KEY.encode("utf-8")) < 32:
    raise RuntimeError("JWT_SECRET_KEY debe tener al menos 32 bytes")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@bloodbank.local")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
if len(ADMIN_PASSWORD) < 12:
    raise RuntimeError("ADMIN_PASSWORD debe tener al menos 12 caracteres")
