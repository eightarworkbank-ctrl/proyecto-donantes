import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ["JWT_SECRET_KEY"] = "test-only-jwt-secret-with-at-least-32-bytes"
os.environ["ADMIN_PASSWORD"] = "test-only-admin-password"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        from app.routers.auth import seed_admin

        seed_admin(db)
    finally:
        db.close()


def test_health_endpoint():
    reset_db()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_and_login_user():
    reset_db()
    payload = {
        "name": "Ana García",
        "email": "ana@example.com",
        "password": "secret123",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "ana@example.com"
    assert body["role"] == "user"

    login = client.post("/auth/login", json={"email": "ana@example.com", "password": "secret123"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token

    me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "ana@example.com"


def test_registration_rejects_client_assigned_role():
    reset_db()
    response = client.post(
        "/auth/register",
        json={
            "name": "Eva",
            "email": "eva@example.com",
            "password": "secret123",
            "role": "admin",
        },
    )

    assert response.status_code == 422


def test_duplicate_user_is_rejected():
    reset_db()
    payload = {"name": "Maria", "email": "maria@example.com", "password": "pass123"}
    first = client.post("/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/auth/register", json=payload)
    assert second.status_code == 400
    assert "ya existe" in second.json()["detail"]


def test_admin_can_manage_donors_and_users():
    reset_db()
    admin_login = client.post(
        "/auth/login",
        json={"email": "admin@bloodbank.local", "password": os.environ["ADMIN_PASSWORD"]},
    )
    assert admin_login.status_code == 200
    token = admin_login.json()["access_token"]

    users = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert users.status_code == 200
    assert any(user["email"] == "admin@bloodbank.local" for user in users.json())

    donor = client.post(
        "/donors",
        json={
            "name": "Luis Pérez",
            "blood_type": "O+",
            "city": "Bogotá",
            "phone": "3001234567",
            "email": "luis@example.com",
            "last_donation": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert donor.status_code == 201
    donor_id = donor.json()["id"]

    donors = client.get("/donors", headers={"Authorization": f"Bearer {token}"})
    assert donors.status_code == 200
    assert any(item["id"] == donor_id for item in donors.json())

    detail = client.get(f"/donors/{donor_id}", headers={"Authorization": f"Bearer {token}"})
    assert detail.status_code == 200
    assert detail.json()["name"] == "Luis Pérez"


def test_non_admin_cannot_manage_donors():
    reset_db()
    client.post("/auth/register", json={"name": "Pepito", "email": "pepito@example.com", "password": "secret123"})
    login = client.post("/auth/login", json={"email": "pepito@example.com", "password": "secret123"})
    token = login.json()["access_token"]

    response = client.post(
        "/donors",
        json={
            "name": "Ana",
            "blood_type": "A-",
            "city": "Medellín",
            "phone": "3100000000",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "administrador" in response.json()["detail"]

    users_response = client.get("/users", headers={"Authorization": "Bearer " + token})
    assert users_response.status_code == 403


def test_invalid_token_is_rejected():
    reset_db()
    response = client.get("/users/me", headers={"Authorization": "Bearer bad-token"})
    assert response.status_code == 401
    assert "Token inválido" in response.json()["detail"]
