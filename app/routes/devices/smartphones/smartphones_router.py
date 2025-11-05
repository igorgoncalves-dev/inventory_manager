from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.machine.machine_model import Machine
from schemas.smartphone.smartphone_schemas import UpdateSmartphoneSchema
from database import session_db
from models.smartphone.smartphone_model import Smartphone


smartphones_router = APIRouter(
    prefix="/smartphones", 
    tags=["smartphones"]
)

@smartphones_router.get("/")
def get_smartphones(db: Session = Depends(session_db)):
    
    smartphones = db.query(Smartphone).all()

    if not smartphones:
        raise HTTPException(404, detail={
            "message": "There isn't smartphones in database"
        })
    
    return smartphones

@smartphones_router.get("/{smartphone_id}")
def get_smartphone_by_id(smartphone_id: int, db: Session = Depends(session_db)):

    smartphone = db.query(Smartphone).get(smartphone_id)
    
    if not smartphone:
        raise HTTPException(404, detail={
            "message": "Smartphone was not found"
        })
    
    return smartphone


@smartphones_router.post("/create-smartphone")
def create_smartphone(smartphone: UpdateSmartphoneSchema, db: Session = Depends(session_db)):
    
    if not smartphone:
        raise HTTPException(404, detail={
            "message": "Invalid data"
        })
    
    smartphone_db = Smartphone(**smartphone.model_dump(exclude_unset=True))
    
    db.add(smartphone_db)
    db.commit()

    return {
        "message": "The Smartphone has been created!",
        "data": smartphone_db
    }


@smartphones_router.put("/update-smartphone/{smartphone_id}")
def update_smartphone(smartphone_id: int):
    pass


@smartphones_router.delete("/delete-smartphone/{smartphone_id}")
def delete_smartphone(smartphone_id: int, db: Session = Depends(session_db)):
    
    smartphone = db.query(Smartphone).get(smartphone_id)

    if not smartphone:
        raise HTTPException(404, detail={
            "message": "Smartphone was not found"
        })
    
    db.delete(smartphone)
    db.commit()
    
    return {
        "message": "Smartphone has been deleted",
        "smartphone": {
            "model": smartphone.model,
            "imei": smartphone.imei
        }
    }

