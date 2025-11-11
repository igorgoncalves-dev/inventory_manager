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
    



@users_router.post("/create-user", response_model=UserResponseSchema)
async def create_user(user: CreateUserSchema, db: Session = Depends(session_db)):
    """ Rota responsável pela criação de novos usuários na aplicação """
    
    email_exist = db.query(User).filter(User.email == user.email).first()
    if email_exist:
        raise HTTPException(400, detail={
            "message": "The EMAIL already exist in database"
        })
    
    if user.machine_id is not None:
        machine_id_exist = db.query(User).filter(User.machine_id == user.machine_id).first()
        if machine_id_exist:
            raise HTTPException(400, detail={
                "message": "The MACHINE already has an owner in database"
            })

    if user.smartphone_id is not None:
        smartphone_id_exist = db.query(User).filter(User.smartphone_id == user.smartphone_id).first()
        if smartphone_id_exist:
            raise HTTPException(400, detail={
                "message": "The SMARTPHONE already has an owner in database"
            })
    
    new_user = User(**user.model_dump(exclude_unset=True))

    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })      

    return new_user





@users_router.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(session_db)):

    user_db = db.get(User, user_id)

    if not user:
        raise HTTPException(404, detail={
            "message": f"User with ID {user_id} not found"
        })
    
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_db, key, value)

    try:
        db.commit()
        db.refresh(user_db)
    
    except Exception as e:
        db.rollback()

        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return user_db





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
