from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.smartphone.smartphone_schemas import CreateSmartphoneSchema, ResponseSmartphoneSchema, UpdateSmartphoneSchema
from database import session_db
from models.smartphone.smartphone_model import Smartphone


smartphones_router = APIRouter(
    prefix="/smartphones", 
    tags=["smartphones"]
)

@smartphones_router.get("/")
def get_smartphones(db: Session = Depends(session_db)):
    """ Rota responsável por retornar todos os Smartphones cadastrados no banco de dados """
    
    smartphones = db.query(Smartphone).all()
    
    return smartphones

@smartphones_router.get("/{smartphone_id}")
def get_smartphone_by_id(smartphone_id: int, db: Session = Depends(session_db)):
    """ Rota responsável por retornar um smartphone específico utilizando o ID como parâmetro """

    smartphone = db.get(Smartphone, smartphone_id)
    
    if not smartphone:
        raise HTTPException(404, detail={
            "message": f"Smartphone with ID {smartphone_id} not found"
        })
    
    return smartphone


@smartphones_router.post("/create-smartphone", response_model=ResponseSmartphoneSchema)
def create_smartphone(smartphone: CreateSmartphoneSchema, db: Session = Depends(session_db)):
    """ Rota responsável pela criação de um novo Smartphone no banco de dados """
    
    # Verificar IMEI
    exist_imei = db.query(Smartphone).filter(Smartphone.imei == smartphone.imei).first()
    if exist_imei:
        raise HTTPException(status_code=400, detail={"message": "IMEI already exists"})

    # Verificar número
    exist_number = db.query(Smartphone).filter(Smartphone.number == smartphone.number).first()
    if exist_number:
        raise HTTPException(status_code=400, detail={"message": "Number already exists"})

        # Verificar user_id
    if smartphone.user_id is not None:
        exist_user_id = db.query(Smartphone).filter(Smartphone.user_id == smartphone.user_id).first()
        if exist_user_id:
            raise HTTPException(status_code=400, detail={"message": "User already has a smartphone"})

    smartphone_db = Smartphone(**smartphone.model_dump(exclude_unset=True))

    try:
        db.add(smartphone_db)
        db.commit()

    except Exception as e:
        db.rollback()
        
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })  

    return smartphone_db


@smartphones_router.put("/update-smartphone/{smartphone_id}")
def update_smartphone(smartphone_id: int, smartphone: UpdateSmartphoneSchema, db: Session = Depends(session_db)):
    
    # Verificando se o objeto existe no banco
    smartphone_db = db.get(Smartphone, smartphone_id)

    if not smartphone_db:
        raise HTTPException(404, detail={
            "message": f"Smartphone with ID {smartphone_id} not found"
        })
    
    # Validação do JSON recebido
    validation = {k: v for k, v in smartphone.model_dump(exclude_unset=True).items() if k in UpdateSmartphoneSchema.model_fields}

    if not validation:
        raise HTTPException(400, detail={
            "message": "There are no valid data"
        })
    
    for key, value in validation.items():
        setattr(smartphone_db, key, value)
        
    try:
        db.commit()
        db.refresh(smartphone_db)

    except Exception as e:
        db.rollback()

        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return {
        "message": "The smartphone has been updated",
        "data": smartphone_db
    }


@smartphones_router.delete("/delete-smartphone/{smartphone_id}")
def delete_smartphone(smartphone_id: int, db: Session = Depends(session_db)):
    
    smartphone = db.get(Smartphone, smartphone_id)

    if not smartphone:
        raise HTTPException(404, detail={
            "message": f"Smartphone with ID {smartphone_id} not found"
        })

    try:
        db.delete(smartphone)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })
    
    return {
        "message": "Smartphone has been deleted",
        "smartphone": {
            "model": smartphone.model,
            "imei": smartphone.imei
        }
    }

