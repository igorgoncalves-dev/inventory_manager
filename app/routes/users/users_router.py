from fastapi import APIRouter, HTTPException

users_router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

users = [
    {
        "id": 1,
        "name": "Igor Almeida",
        "mail": "igor.almeida@example.com",
        "device_id": "DEV-1001",
        "smartphone_id": "SM-5001",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Maria Santos",
        "mail": "maria.santos@example.com",
        "device_id": "DEV-1002",
        "smartphone_id": "SM-5002",
        "status": "inactive"
    },
    {
        "id": 3,
        "name": "João Oliveira",
        "mail": "joao.oliveira@example.com",
        "device_id": "DEV-1003",
        "smartphone_id": "SM-5003",
        "status": "active"
    },
    {
        "id": 4,
        "name": "Carla Souza",
        "mail": "carla.souza@example.com",
        "device_id": "DEV-1004",
        "smartphone_id": "SM-5004",
        "status": "blocked"
    },
    {
        "id": 5,
        "name": "Bruno Lima",
        "mail": "bruno.lima@example.com",
        "device_id": "DEV-1005",
        "smartphone_id": "SM-5005",
        "status": "active"
    },
    {
        "id": 6,
        "name": "Fernanda Castro",
        "mail": "fernanda.castro@example.com",
        "device_id": "DEV-1006",
        "smartphone_id": "SM-5006",
        "status": "inactive"
    },
    {
        "id": 7,
        "name": "Lucas Pereira",
        "mail": "lucas.pereira@example.com",
        "device_id": "DEV-1007",
        "smartphone_id": "SM-5007",
        "status": "active"
    },
    {
        "id": 8,
        "name": "Patrícia Gomes",
        "mail": "patricia.gomes@example.com",
        "device_id": "DEV-1008",
        "smartphone_id": "SM-5008",
        "status": "active"
    },
    {
        "id": 9,
        "name": "Ricardo Barbosa",
        "mail": "ricardo.barbosa@example.com",
        "device_id": "DEV-1009",
        "smartphone_id": "SM-5009",
        "status": "inactive"
    },
    {
        "id": 10,
        "name": "Amanda Ferreira",
        "mail": "amanda.ferreira@example.com",
        "device_id": "DEV-1010",
        "smartphone_id": "SM-5010",
        "status": "active"
    }
]

@users_router.get("/")
def get_users():
    return users

@users_router.get("/{user_id}")
def get_user_by_id(user_id: int):

    for user in users:
        if user["id"] == user_id:
            print(user["name"])
            return user
        
"""     raise HTTPException(
        status_code=404,
        detail={
            "status_code": 404,
            "message": f"O usuário com id {user_id} não foi encontrado"
        }
    ) """