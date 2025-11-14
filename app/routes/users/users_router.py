from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import session_db

from models.user.user_model import User
# from schemas.user.user_schemas import CreateUserSchema, CreateUserSchemaResponse, UpdateUserSchema
from schemas.user.user_schemas import CreateUserRequest, CreateUserResponse, UpdateUserRequest, UpdateUserResponse

from utils.functions.db_check_uniqueness import db_check_uniqueness

from datetime import datetime


users_router = APIRouter(
    prefix="/users", 
    tags=["users"]
)




@users_router.get("/")
async def get_users(db: Session = Depends(session_db)):
    """ Rota responsável pela recuperação de todos os registros da tabela USERS """

    users = db.query(User).all()

    return users




@users_router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(session_db)):
    """ Rota responsável pela recuperação de registros específicos da tabela USERS, utilizando o ID como fonte de busca """
    
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(404, detail={
            "message": f"User with ID {user_id} not found"
        })

    return user
    



@users_router.post("/create-user", response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, db: Session = Depends(session_db)):
    """ Rota responsável pela criação de novos usuários na aplicação """
    
    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "email": user.email,
        "machine_id": user.machine_id,
        "smartphone_id": user.smartphone_id
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db=db,
            table_column=key,
            table_name=User,
            value=value
        )

    # Inserindo os novos dados no banco
    new_user = User(**user.model_dump(exclude_unset=True))

    try:
        db.add(new_user)
        db.commit()

    except Exception as e:
        db.rollback()

        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })      

    return new_user, {
        "timestamp": datetime.now() 
    }





@users_router.put("/update-user/{user_id}", response_model=UpdateUserResponse)
def update_user(user_id: int, user: UpdateUserRequest, db: Session = Depends(session_db)):

    user_db = db.get(User, user_id)

    if not user_db:
        raise HTTPException(404, detail={
            "message": f"User with ID {user_id} not found"
        })
    

    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "email": user.email,
        "machine_id": user.machine_id,
        "smartphone_id": user.smartphone_id
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db=db,
            table_column=key,
            table_name=User,
            value=value
        )

    validation = {k: v for k, v in user.model_dump(exclude_unset=True).items() if k in UpdateUserRequest.model_fields}

    if not validation:
        raise HTTPException(400, detail={
            "message": "There are no valid data"
        })
    
    for key, value in validation.items():
        setattr(user_db, key, value)

    try:
        db.commit()
        db.refresh(user_db)
    
    except Exception as e:
        db.rollback()

        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return user_db, {"timestamp": datetime.now()}





@users_router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(session_db)):

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    
    try:
        db.delete(user)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return {
        "message": "User has been deleted",
        "user": {
            "email": user.email,
        }
    }
