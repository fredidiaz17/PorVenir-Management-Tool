from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.db_conn import get_bd

from src.models.marca import MarcaModel

from src.schemas.marca import Marca, MarcaPatch
    
router = APIRouter() 


@router.get("/") 
def get_marcas(db: Session = Depends(get_bd)):
    stmt = select(MarcaModel)
    result = db.execute(stmt).scalars().all() 
    return {"status": "ok", "data": result}


@router.get("/{marca_id}")
def get_marca(marca_id: int, db: Session = Depends(get_bd)):
    query_marca = db.get(MarcaModel, marca_id) # Se busca la marca por PK.
    if query_marca is None:
        return {"status": "error", "message": "Marca no encontrada"} # Si no se encuentra la marca.
    return {"status": "ok", "data": query_marca}

@router.post("/") 
def create_marca(marca: Marca, db: Session = Depends(get_bd)):
    try:
        new_marca = MarcaModel(nombre=marca.nombre, descripcion=marca.descripcion, id_compania=marca.id_compania)
        db.add(new_marca)
        db.commit()
        db.refresh(new_marca)
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Marca creada exitosamente"}
    

@router.put("/{marca_id}")
def update_marca(marca_id: int, marca: Marca, db: Session = Depends(get_bd)): 
    try:
        query_marca = db.get(MarcaModel, marca_id) # Se busca la marca por PK.
        if not query_marca: # Si no se encuentra la marca.
            return {"status": "error", "message": "Marca no encontrada"}
        
        query_marca.nombre = marca.nombre
        query_marca.descripcion = marca.descripcion
        query_marca.id_compania = marca.id_compania
        
        db.commit() # Se confirma la transacción.
        db.refresh(query_marca) # Se actualiza la instancia con los datos de la base de datos (como el id).
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.patch("/{marca_id}")
def update_marca_parcial(marca_id: int, marca: MarcaPatch, db: Session = Depends(get_bd)):
    try:
        query_marca = db.get(MarcaModel, marca_id) 
        if not query_marca: 
            return {"status": "error", "message": "Marca no encontrada"}
        
        for key, value in marca.model_dump().items():
            if value is not None:
                setattr(query_marca, key, value) 
        
        db.commit() 
        db.refresh(query_marca) 
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{marca_id}")
def delete_marca(marca_id: int, db: Session = Depends(get_bd)):
    try:
        query_marca = db.get(MarcaModel, marca_id)
        if not query_marca: 
            return {"status": "error", "message": "Marca no encontrada"}
        db.delete(query_marca)
        db.commit()
    except Exception as e:
        return {"status": "error", "message": str(e), "origin": e.orig}
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}    