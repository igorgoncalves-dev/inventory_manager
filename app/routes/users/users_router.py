from fastapi import APIRouter, Depends, HTTPException
from sentry_sdk import HttpTransport

from schemas.user.create_user_schema import CreateUser, CreateUserResponse
from database import get_db
from sqlalchemy.orm import Session
from models.user.user_model import User

users_router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@users_router.get("/")
def get_users(db: Session = Depends(get_db)):
    """ Rota responsável pela recuperação de todos os registros da tabela USERS """

    users = db.query(User).all()

    return users

@users_router.get("/{user_id}")
def get_user_by_id(user_id: int):
    """ Rota responsável pela recuperação de registros específicos da tabela USERS, utilizando o ID como fonte de busca """
    pass

@users_router.post("/create-user", response_model=CreateUserResponse)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):


    if not user:
        raise HTTPException(
            status_code=403, 
            detail={
                "message": f"Invalid data"
            }
        )
    
    new_user = User(
        name= user.name,
        surname= user.surname,
        email=user.email,
        cost_center=user.cost_center,
    )

    db.add(new_user)
    db.commit()

    response = CreateUserResponse(
        display_name= f"{new_user.name} {new_user.surname}",
        email= new_user.email
    )      

    return response

@users_router.put("/update-user/{user_id}")
def update_user(user_id: int):
    pass

@users_router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HttpTransport(
            status_code=404,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()

    return {"message": f"User {user.name} removido com sucesso"}
