from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.dependencies import get_current_user, require_admin
from app.models import User
from app.routers import auth, donors

app = FastAPI(title="Donantes API", version="1.0.0")

app.include_router(auth.router)
app.include_router(donors.router)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = next(get_db())
    auth.seed_admin(db)
    db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict[str, object]:
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role}


@app.get("/users", dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return [
        {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
        for user in db.query(User).all()
    ]
