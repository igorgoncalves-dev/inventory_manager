from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.functions.db_check_uniqueness import db_check_uniqueness
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
    
    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "imei": smartphone.imei,
        "number": smartphone.number,
        "user_id": smartphone.user_id
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db= db,
            table_name=Smartphone,
            table_column=key,
            value=value
        )

    # Inserindo os novos dados no banco
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
        
    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "imei": smartphone.imei,
        "number": smartphone.number,
        "user_id": smartphone.user_id
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db= db,
            table_name=Smartphone,
            table_column=key,
            value=value
        )

    # Validação dos campos enviados no JSON do Front
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

