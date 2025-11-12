from fastapi import HTTPException

def db_check_uniqueness(db, table_column, value, table_name, message=False):
    """ Verifica se os campos unicos da tabela já existem  """
    
    if value is not None:
        exist = db.query(table_name).filter(getattr(table_name, table_column) == value).first()

        if exist:
            raise HTTPException(400, detail={               
                "message": message if message else f"{str(table_column).upper()} already has a exists"
            })
        
