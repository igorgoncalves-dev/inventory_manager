from fastapi import APIRouter

from .smartphones.smartphones_router import smartphones_router
from .machines.machines_router import machines_router

devices_router = APIRouter(
    prefix="/devices",
)

devices_router.include_router(machines_router)
devices_router.include_router(smartphones_router)