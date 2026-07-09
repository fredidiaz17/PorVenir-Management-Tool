from fastapi import APIRouter
from src.database.db_conn import engine
from sqlalchemy import text
from src.schemas.marca import Marca, MarcaUpdate
    
router = APIRouter() 


@router.get("/") 
def get_marcas():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM marca")) 
        result = [dict(row) for row in result.mappings().fetchall()] 
    return {"status": "ok", "data": result}


@router.get("/{marca_id}")
def get_marca(marca_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM marca WHERE id_marca = :marca_id"), {"marca_id": marca_id})
        result = result.mappings().fetchone() 
    return {"status": "ok", "data": result}

@router.post("/") 
def create_marca(marca: Marca):
    try:
        marca_data = marca.model_dump() # Convertir modelo a diccionario
        with engine.begin() as conn:
            data = {
                "marca_nombre": marca_data.get("nombre"),
                "marca_descripcion": marca_data.get("descripcion"),
                "id_compania": marca_data.get("id_compania")
            }
            conn.execute(text(
                """INSERT INTO marca (nombre, descripcion, id_compania) 
                VALUES (:marca_nombre, :marca_descripcion, :id_compania)"""), data)
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia creada exitosamente"}
    

@router.put("/{marca_id}")
def update_marca(marca_id: int, marca: Marca): # TODO: Cambiar esto por un modelo que solo seleccione lo que se quiere actualizar, o mejor aún, solo aplicar los cambios que no sean nulos, por el momento funcionara con Marca Update
    try:
        marca_data = marca.model_dump()
        with engine.begin() as conn:
            data = {
                "marca_nombre": marca_data.get("nombre"),
                "marca_descripcion": marca_data.get("descripcion"),
                "id_compania": marca_data.get("id_compania"),
                "marca_id": marca_id
            }
            conn.execute(text("""UPDATE marca SET nombre = :marca_nombre, descripcion = :marca_descripcion, id_compania = :id_compania 
            WHERE id_marca = :marca_id"""), data)
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{marca_id}")
def delete_marca(marca_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM marca WHERE id_marca = :marca_id"), {"marca_id": marca_id})
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}    