from email import message
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import session_db
from models.machine.machine_model import Machine
from schemas.machine.machine_schemas import CreateMachineSchema, ResponseMachineSchema, UpdateMachineSchema

machines_router = APIRouter(
    prefix="/machines", 
    tags=["machines"]
)

@machines_router.get("/")
def get_machines(db: Session = Depends(session_db)):
    """ Rota responsável por retornar todas as máquinas cadastradas no banco """

    machine = db.query(Machine).all()

    if not machine:
        raise HTTPException(404, detail={
            "message": "There isn't machines in database"
        })

    return machine

@machines_router.get("/{machine_id}")
def get_machine_by_id(machine_id: int, db: Session = Depends(session_db)):
    """ Rota responsável por retornar uma máquina específica, utilizando o ID como parâmetro"""

    machine = db.query(Machine).filter(Machine.id == machine_id).first()

    if not machine:
        raise HTTPException(404, detail={
            "message": "Machine not found"
        })

    return machine

@machines_router.post("/create-machine", response_model=ResponseMachineSchema)
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

    return {
        "message": "Machine has been created!",
        "data": new_machine
    }


@machines_router.put("/update-machine/{machine_id}")
def update_machine(machine_id: int, machine: UpdateMachineSchema, db: Session = Depends(session_db)):
    """ Rota responsável por atualizar uma máquina utilizando o ID como parâmetro """

    machine_db = db.query(Machine).get(machine_id)

    if not machine:
        raise HTTPException(404, detail={
            "message": "The selected machine was not found"
        })
    
    for key, value in machine.model_dump(exclude_unset=True).items():
        setattr(machine_db, key, value)

    db.commit()
    db.refresh(machine_db)

    return {
        "message": "The machine has been updated",
        "data": machine_db
    }



@machines_router.delete("/delete-machine/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(session_db)):
    """ Rota responsável por deletar uma máquina utilizando o ID como parâmetro """

    machine = db.query(Machine).get(machine_id)

    if not machine:
        raise HTTPException(404, detail={
            "message": "The selected machine was not found"
        })
    
    db.delete(machine)
    db.commit()
    
    return {
        "message": "Machine has been deleted",
        "machine": {
            "hostname": machine.hostname,
            "serial_number": machine.serial_number
        }
    }
