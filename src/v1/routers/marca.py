
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.db_conn import get_bd

from src.models.marca import MarcaModel
from src.models.oferta import OfertaModel

from src.v1.schemas.marca import Marca, MarcaPatch
    
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
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"}) # Si no se encuentra la marca.
    return {"status": "ok", "data": query_marca}

@router.post("/") 
def create_marca(marca: Marca, db: Session = Depends(get_bd)):
    try:
        new_marca = MarcaModel(nombre=marca.nombre, descripcion=marca.descripcion, id_compania=marca.id_compania)
        db.add(new_marca)
        db.commit()
        db.refresh(new_marca)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Marca creada exitosamente"}
    

@router.put("/{marca_id}")
def update_marca(marca_id: int, marca: Marca, db: Session = Depends(get_bd)): 
    try:
        query_marca = db.get(MarcaModel, marca_id) # Se busca la marca por PK.
        if not query_marca: # Si no se encuentra la marca.
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})
        
        query_marca.nombre = marca.nombre
        query_marca.descripcion = marca.descripcion
        query_marca.id_compania = marca.id_compania
        
        db.commit() # Se confirma la transacción.
        db.refresh(query_marca) # Se actualiza la instancia con los datos de la base de datos (como el id).
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.patch("/{marca_id}")
def update_marca_parcial(marca_id: int, marca: MarcaPatch, db: Session = Depends(get_bd)):
    try:
        query_marca = db.get(MarcaModel, marca_id) 
        if not query_marca: 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})
        
        for key, value in marca.model_dump().items():
            if value is not None:
                setattr(query_marca, key, value) 
        
        db.commit() 
        db.refresh(query_marca) 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{marca_id}")
def delete_marca(marca_id: int, db: Session = Depends(get_bd)):
    try:
        query_marca = db.get(MarcaModel, marca_id)
        if not query_marca: 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})
        db.delete(query_marca)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}


# N:M con Oferta

# Todas las ofertas que se aplican a la marca dada.
@router.get("/{marca_id}/ofertas")
def get_ofertas_marca(marca_id: int, db: Session = Depends(get_bd)):
    marca = db.get(MarcaModel, marca_id)
    if marca is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})

    return {"status": "ok", "data": marca.ofertas}


@router.post("/{marca_id}/ofertas/{id_oferta}")
def post_oferta_marca(marca_id: int, id_oferta: int, db: Session = Depends(get_bd)):
    marca = db.get(MarcaModel, marca_id)
    offer = db.get(OfertaModel, id_oferta)
    if marca is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o marca no encontrada"})
    
    offer.marcas.append(marca)
    db.commit()
    return {"status": "ok", "message": "Oferta aplicada a marca exitosamente"}


@router.delete("/{marca_id}/ofertas/{id_oferta}")
def delete_oferta_marca(marca_id: int, id_oferta: int, db: Session = Depends(get_bd)):
    marca = db.get(MarcaModel, marca_id)
    offer = db.get(OfertaModel, id_oferta)

    if marca is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o marca no encontrada"})

    if offer not in marca.ofertas:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no aplicada a marca"})

    marca.ofertas.remove(offer) # Elimina la relación oferta_marca respectiva
    db.commit()
    return {"status": "ok", "message": "Oferta eliminada de marca exitosamente"}
