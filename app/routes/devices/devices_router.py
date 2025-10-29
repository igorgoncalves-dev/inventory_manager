from fastapi import APIRouter

from .machines.machines_router import machines_router

devices_router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

devices_router.include_router(machines_router)