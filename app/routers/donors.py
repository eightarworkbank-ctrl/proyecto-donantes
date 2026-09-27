from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import Donor, User
from app.schemas import DonorCreate, DonorOut

router = APIRouter(prefix="/donors", tags=["donors"])


@router.get("", response_model=list[DonorOut])
def list_donors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Donor).offset(skip).limit(limit).all()


@router.post("", response_model=DonorOut, status_code=status.HTTP_201_CREATED)
def create_donor(
    donor_in: DonorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    donor = Donor(**donor_in.model_dump())
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("/{donor_id}", response_model=DonorOut)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donante no encontrado")
    return donor
