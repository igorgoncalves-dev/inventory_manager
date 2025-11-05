from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import session_db
from models.machine.machine_model import Machine
from schemas.machine.machine_schemas import CreateMachineSchema, MachineBaseSchema, MachineResponseSchema

machines_router = APIRouter(
    prefix="/machines", 
    tags=["machines"]
)

@machines_router.get("/")
def get_machines():
    pass

@machines_router.get("/{machine_id}")
def get_machine_by_id(machine_id: int):
    pass

@machines_router.post("/create-machine", response_model=MachineResponseSchema)
def create_machine(machine: CreateMachineSchema, db: Session = Depends(session_db)):

    if not machine:
        raise HTTPException(400, detail={
            "message": "Invalid data"
        })

    new_machine = Machine(
        hostname= machine.hostname,
        type= machine.type,
        brand= machine.brand,
        model= machine.model,
        mac_address= machine.mac_address,
        mac_address_wifi= machine.mac_address_wifi,
        serial_number= machine.serial_number,
        cpu= machine.cpu,
        ram= machine.ram,
        storage_1= machine.storage_1,
        storage_2= machine.storage_2,
        location= machine.location,
        user_id= machine.user_id,
        status= machine.status
    )

    db.add(new_machine)
    db.commit()

    return new_machine

