from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import engine, Base

from models.user import user_model
from models.machine import machine_model
from models.smartphone import smartphone_model


# Lifecycle control
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Application started: {app}")
    Base.metadata.create_all(bind=engine)

    yield
    print(f"Application closed: {app}")


# Creating a new API instance
app = FastAPI(
    title="Inventory Manager",
    version="0.2.4",
    lifespan=lifespan
)

# Importing Routes
from routes.users.users_router import users_router
app.include_router(users_router)

from routes.devices.devices_router import devices_router
app.include_router(devices_router)

# Initialising Application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=5000,
        reload=True
    )