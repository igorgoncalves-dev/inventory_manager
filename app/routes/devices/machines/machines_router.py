from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import session_db
from models.machine.machine_model import Machine
from schemas.machine.machine_schemas import CreateMachineSchema, UpdateMachineSchema

machines_router = APIRouter(
    prefix="/machines", 
    tags=["machines"]
)

@machines_router.get("/")
def get_machines(db: Session = Depends(session_db)):
    """ Rota responsável por retornar todas as máquinas cadastradas no banco """

    machine = db.query(Machine).all()

    return machine

@machines_router.get("/{machine_id}")
def get_machine_by_id(machine_id: int, db: Session = Depends(session_db)):
    """ Rota responsável por retornar uma máquina específica, utilizando o ID como parâmetro"""

    machine = db.query(Machine).filter(Machine.id == machine_id).first()

    if not machine:
        raise HTTPException(404, detail={
            "message": f"Machine with ID {machine_id} not found"
        })

    return machine

@machines_router.post("/create-machine")
def create_machine(machine: CreateMachineSchema, db: Session = Depends(session_db)):

    hostname_exist = db.query(Machine).filter(Machine.hostname == machine.hostname).first()
    if hostname_exist:
        raise HTTPException(400, detail={
            "message": "HOSTNAME already exist in the database"
        })

    serial_number_exist = db.query(Machine).filter(Machine.serial_number == machine.serial_number).first()
    if serial_number_exist:
        raise HTTPException(400, detail={
            "message": "SERIAL NUMBER already exist in the database"
        })
    
    if machine.mac_address is not None:
        mac_address_exist = db.query(Machine).filter(Machine.mac_address == machine.mac_address).first()
        if mac_address_exist:
            raise HTTPException(400, detail={
                "message": "MAC ADDRESS already exist in the database"
            })
    
    if machine.mac_address_wifi is not None:
        mac_address_wifi_exist = db.query(Machine).filter(Machine.mac_address_wifi == machine.mac_address_wifi).first()
        if mac_address_wifi_exist:
            raise HTTPException(400, detail={
                "message": "WIFI MAC ADRESS already exist in the database"
            }) 
    
    new_machine = Machine(**machine.model_dump(exclude_unset=True))

    try:
        db.add(new_machine)
        db.commit()
        db.refresh(new_machine)

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return new_machine


@machines_router.put("/update-machine/{machine_id}")
def update_machine(machine_id: int, machine: UpdateMachineSchema, db: Session = Depends(session_db)):
    """ Rota responsável por atualizar uma máquina utilizando o ID como parâmetro """

    machine_db = db.get(Machine, machine_id)

    if not machine:
        raise HTTPException(404, detail={
            "message": f"Machine with ID {machine_id} not found"
        })
    
    for key, value in machine.model_dump(exclude_unset=True).items():
        setattr(machine_db, key, value)

    try:
        db.commit()
        db.refresh(machine_db)
    
    except Exception as e:
        db.rollback()

        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })

    return {
        "message": "The machine has been updated",
        "data": machine_db
    }



@machines_router.delete("/delete-machine/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(session_db)):
    """ Rota responsável por deletar uma máquina utilizando o ID como parâmetro """

    machine = db.get(Machine, machine_id)

    if not machine:
        raise HTTPException(404, detail={
            "message": f"Machine with ID {machine_id} not found"
        })
    
    try:
        db.delete(machine)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail={
            "message": f"Database error: {e}"
        })
    
    return {
        "message": "Machine has been deleted",
        "machine": {
            "hostname": machine.hostname,
            "serial_number": machine.serial_number
        }
    }
