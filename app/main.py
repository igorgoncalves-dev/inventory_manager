from fastapi import FastAPI
import uvicorn

# Creating a new API instance
app = FastAPI(
    title="Inventory Manager",
    version="0.1.0"
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