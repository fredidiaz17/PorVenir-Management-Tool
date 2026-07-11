from fastapi import APIRouter, Depends # Depends es para el manejo de dependencias. Reutilizar codigo mas limpio.
from sqlalchemy.orm import Session

# Modelos
from src.models.compania import CompaniaModel

# Schemas
from src.schemas.compania import Compania

from src.database.db_conn import get_bd # Para obtener la sesión de la bd

router = APIRouter() # El Router recibe la petición y la dirige a su respectiva ruta

# Los respectivos metodos.
@router.get("/") # Define la ruta
def get_companias(db: Session = Depends(get_bd)): # Se define la dependencia. Es decir, se ejecuta la funcion get_bd() y se pasa su resultado a la funcion get_companias().
    result = db.query(CompaniaModel).all() # Se ejecuta la consulta.
    return {"status": "ok", "data": result} # Se devuelve el resultado.


@router.get("/{compania_id}")
def get_compania(compania_id: int, db: Session = Depends(get_bd)):
    result = db.query(CompaniaModel).filter(CompaniaModel.id_compania == compania_id).first() # Se ejecuta la consulta.
    # if result is None:
        # raise HTTPException(status_code=404, detail="Compania no encontrada") # Se devuelve el resultado.
    return {"status": "ok", "data": result}

@router.post("/")
def create_compania(compania:Compania, db: Session = Depends(get_bd)):
    try:
        new_company = CompaniaModel(nombre=compania.nombre) # Se crea una instancia del modelo.

        db.add(new_company) # Se agrega la instancia (compania) a la sesión.
        db.commit() # Se confirma la transacción.
        db.refresh(new_company) # Se actualiza la instancia con los datos de la base de datos (como el id).

    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia creada exitosamente"}
    

@router.put("/{compania_id}")
def update_compania(compania_id: int, compania:Compania, db: Session = Depends(get_bd)):
    try:
         query_compania = db.query(CompaniaModel).filter(CompaniaModel.id_compania == compania_id).first()

         query_compania.nombre = compania.nombre # Se actualiza el nombre de la compañia.

         db.commit() # Se confirma la transacción.
         
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{compania_id}")
def delete_compania(compania_id: int, db: Session = Depends(get_bd)):
    try:
        query_compania = db.query(CompaniaModel).filter(CompaniaModel.id_compania == compania_id).first()

        db.delete(query_compania) # Se elimina la instancia.
        db.commit() # Se confirma la transacción.    
         
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}    