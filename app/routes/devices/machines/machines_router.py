from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from utils.functions.db_check_uniqueness import db_check_uniqueness
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
    """ Rota responsável pela criação de uma nova Máquina no banco de dados """

    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "hostname": machine.hostname,
        "serial_number": machine.serial_number,
        "mac_address": machine.mac_address,
        "mac_address_wifi": machine.mac_address_wifi
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db= db,
            table_name=Machine,
            table_column=key,
            value=value
        ) 
    
    # Inserindo os novos dados no banco
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

    if not machine_db:
        raise HTTPException(404, detail={
            "message": f"Machine with ID {machine_id} not found"
        })
    
    # Verificação de Campos Unicos no Banco
    unique_fields = {
        "hostname": machine.hostname,
        "serial_number": machine.serial_number,
        "mac_address": machine.mac_address,
        "mac_address_wifi": machine.mac_address_wifi
    }

    for key, value in unique_fields.items():
        db_check_uniqueness(
            db= db,
            table_name=Machine,
            table_column=key,
            value=value
        ) 

    # Validação dos campos enviados no JSON do Front
    validation = {k: v for k, v in machine.model_dump(exclude_unset=True).items() if k in UpdateMachineSchema.model_fields}    

    if not validation:
        raise HTTPException(400, detail={
            "message": "There are no valid data"
        })

    for key, value in validation.items():
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
