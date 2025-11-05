from fastapi import APIRouter, Depends, HTTPException

from schemas.user.user_schemas import CreateUserSchema, UpdateUserSchema, UserResponseSchema
from database import session_db
from sqlalchemy.orm import Session
from models.user.user_model import User

users_router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@users_router.get("/")
async def get_users(db: Session = Depends(session_db)):
    """ Rota responsável pela recuperação de todos os registros da tabela USERS """

    users = db.query(User).all()

    if not len(users) > 0:
        raise HTTPException(400, detail={
            "message": "There isn't users in database"
        })

    return users

@users_router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(session_db)):
    """ Rota responsável pela recuperação de registros específicos da tabela USERS, utilizando o ID como fonte de busca """
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, detail={
            "message": "User not found"
        })

    return {
        "user": user,
        "message": f"Users {user.email} founded!"
        }
    
@users_router.post("/create-user", response_model=UserResponseSchema)
async def create_user(user: CreateUserSchema, db: Session = Depends(session_db)):
    """ Rota responsável pela criação de novos usuários na aplicação """

    if not user:
        raise HTTPException(
            status_code=400, 
            detail={
                "message": f"Invalid data"
            }
        )
    
    new_user = User(
        name= user.name,
        surname= user.surname,
        email=user.email,
        cost_center=user.cost_center,
        machine_id=user.machine_id,
        smartphone_id=user.smartphone_id
    )

    db.add(new_user)
    db.commit()      

    return new_user

@users_router.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(session_db)):

    user_db = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, detail={
            "message": "User not found"
        })
    
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return user_db

@users_router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(session_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()

    return {"message": f"User {user.name} has removed successfully"}
