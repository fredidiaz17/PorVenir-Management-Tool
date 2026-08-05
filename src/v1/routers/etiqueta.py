from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.etiqueta import Etiqueta, EtiquetaPatch
from src.models.etiqueta import EtiquetaModel
from src.models.oferta import OfertaModel

router = APIRouter()

@router.get("/")
def get_etiquetas(db: Session = Depends(get_bd)):
    stmt = select(EtiquetaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_etiqueta}")
def get_etiqueta(id_etiqueta: int, db: Session = Depends(get_bd)):
    stmt = select(EtiquetaModel).where(EtiquetaModel.id_etiqueta == id_etiqueta)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"})
    return {"status": "ok", "data": result} 

@router.post("/")
def create_etiqueta(etiqueta: Etiqueta, db: Session = Depends(get_bd)):
    try:
        new_etiqueta = EtiquetaModel(**etiqueta.model_dump())
        db.add(new_etiqueta)
        db.commit()
        db.refresh(new_etiqueta)
        return {"status": "ok", "message": "Etiqueta creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})

@router.put("/{id_etiqueta}")
def update_etiqueta(id_etiqueta: int, etiqueta: Etiqueta, db: Session = Depends(get_bd)):
    try:
        query_etiqueta = db.get(EtiquetaModel, id_etiqueta)
        if not query_etiqueta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"}) 
        
        query_etiqueta.nombre_etiqueta = etiqueta.nombre_etiqueta
        query_etiqueta.descripcion_etiqueta = etiqueta.descripcion_etiqueta
        query_etiqueta.color_hex = etiqueta.color_hex

        db.commit()
        db.refresh(query_etiqueta)
        return {"status": "ok", "message": "Etiqueta actualizada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.patch("/{id_etiqueta}")
def update_etiqueta_parcial(id_etiqueta: int, etiqueta: EtiquetaPatch, db: Session = Depends(get_bd)):
    try:
        query_etiqueta = db.get(EtiquetaModel, id_etiqueta)
        if not query_etiqueta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"}) 
        
        for key, value in etiqueta.model_dump().items():
            if value is not None:
                setattr(query_etiqueta, key, value)

        db.commit()
        db.refresh(query_etiqueta)
        return {"status": "ok", "message": "Etiqueta actualizada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/{id_etiqueta}")
def delete_etiqueta(id_etiqueta: int, db: Session = Depends(get_bd)):
    try:
        query_etiqueta = db.get(EtiquetaModel, id_etiqueta)
        if not query_etiqueta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"}) 
        db.delete(query_etiqueta)
        db.commit()
        return {"status": "ok", "message": "Etiqueta eliminada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

# N:M con Oferta

# Todas las ofertas que se aplican a la etiqueta dada.
@router.get("/{id_etiqueta}/ofertas")
def get_ofertas_etiqueta(id_etiqueta: int, db: Session = Depends(get_bd)):
    etiqueta = db.get(EtiquetaModel, id_etiqueta)
    if etiqueta is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"})

    return {"status": "ok", "data": etiqueta.ofertas}

@router.post("/{id_etiqueta}/ofertas/{id_oferta}")
def post_oferta_etiqueta(id_etiqueta: int, id_oferta: int, db: Session = Depends(get_bd)):
    etiqueta = db.get(EtiquetaModel, id_etiqueta)
    offer = db.get(OfertaModel, id_oferta)
    if etiqueta is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o etiqueta no encontrada"})
    
    offer.etiquetas.append(etiqueta)
    db.commit()
    return {"status": "ok", "message": "Oferta aplicada a etiqueta exitosamente"}


@router.delete("/{id_etiqueta}/ofertas/{id_oferta}")
def delete_oferta_etiqueta(id_etiqueta: int, id_oferta: int, db: Session = Depends(get_bd)):
    etiqueta = db.get(EtiquetaModel, id_etiqueta)
    offer = db.get(OfertaModel, id_oferta)

    if etiqueta is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o etiqueta no encontrada"})

    if offer not in etiqueta.ofertas:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no aplicada a etiqueta"})

    etiqueta.ofertas.remove(offer)
    db.commit()
    return {"status": "ok", "message": "Oferta eliminada de etiqueta exitosamente"}
