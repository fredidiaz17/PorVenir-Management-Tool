from fastapi import APIRouter
from src.connection.db_conn import engine
from sqlalchemy import text

router = APIRouter() # El Router recibe la petición y la dirige a su respectiva ruta

# Los respectivos metodos.
@router.get("/") # Define la ruta
def get_companias():
    # engine.connect para lecturas
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM compania")) # result maneja el resultado
        
        # .mappings() devuelve un iterable de diccionarios, .fetchall() para traer todos los resultados
        result = [dict(row) for row in result.mappings().fetchall()] # Crear una lista de diccionarios con cada resultado
    return {"status": "ok", "data": result}


@router.get("/{compania_id}")
def get_compania(compania_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM compania WHERE id_compania = :compania_id"), {"compania_id": compania_id})
        result = result.mappings().fetchone() # fetchone() devuelve solo el primer resultado o None si no existe
    return {"status": "ok", "data": result}

@router.post("/{compania_nombre}")
def create_compania(compania_nombre:str):
    # engine.begin para modificaciones. Maneja conn + commit o rollback.
    try:
        with engine.begin() as conn:
            conn.execute(text("INSERT INTO compania (nombre) VALUES (:compania_nombre)"), {"compania_nombre": compania_nombre})
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia creada exitosamente"}
    

@router.put("/{compania_id}/{compania_nombre}")
def update_compania(compania_id: int, compania_nombre: str):
    try:
        with engine.begin() as conn:
            conn.execute(text("UPDATE compania SET nombre = :compania_nombre WHERE id_compania = :compania_id"), {"compania_nombre": compania_nombre, "compania_id": compania_id})
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{compania_id}")
def delete_compania(compania_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM compania WHERE id_compania = :compania_id"), {"compania_id": compania_id})
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}    