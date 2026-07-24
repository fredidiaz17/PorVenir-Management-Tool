from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.oferta import Oferta, OfertaPatch
from src.models.oferta import OfertaModel

router = APIRouter()

@router.get("/")
def get_ofertas(db: Session = Depends(get_bd)):
    stmt = select(OfertaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_oferta}")
def get_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Oferta no encontrada"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_oferta(oferta: Oferta, db: Session = Depends(get_bd)):
    try:
        new_oferta = OfertaModel(**oferta.model_dump())
        db.add(new_oferta)
        db.commit()
        db.refresh(new_oferta)
        return {"status": "ok", "message": "Oferta creada exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_oferta}")
def update_oferta(id_oferta: int, oferta: Oferta, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            return {"status": "error", "message": "Oferta no encontrada"} 
        
        for key, value in oferta.model_dump().items():
            setattr(query_oferta, key, value)

        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Oferta actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_oferta}")
def update_oferta_parcial(id_oferta: int, oferta: OfertaPatch, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            return {"status": "error", "message": "Oferta no encontrada"} 
        
        for key, value in oferta.model_dump().items():
            if value is not None:
                setattr(query_oferta, key, value)

        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Oferta actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_oferta}")
def delete_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            return {"status": "error", "message": "Oferta no encontrada"} 
        db.delete(query_oferta)
        db.commit()
        return {"status": "ok", "message": "Oferta eliminada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)}

# N:M de Ofertas con Productos, Marcas, Etiquetas y Companias

# GET

@router.get("/{id_oferta}/productos")
def get_productos_ofertas(id_oferta: int, db: Session = Depends(get_bd)):
    offer = db.get(OfertaModel, id_oferta)
    if offer is None:
        return {"status": "error", "message": "Oferta no encontrada"}
    return {"status": "ok", "data": offer.productos}

@router.get("/{id_oferta}/marcas")
def get_marcas_ofertas(id_oferta: int, db: Session = Depends(get_bd)):
    offer = db.get(OfertaModel, id_oferta)
    if offer is None:
        return {"status": "error", "message": "Oferta no encontrada"}
    return {"status": "ok", "data": offer.marcas}

@router.get("/{id_oferta}/etiquetas")
def get_etiquetas_ofertas(id_oferta: int, db: Session = Depends(get_bd)):
    offer = db.get(OfertaModel, id_oferta)
    if offer is None:
        return {"status": "error", "message": "Oferta no encontrada"}
    return {"status": "ok", "data": offer.etiquetas}

@router.get("/{id_oferta}/companias")
def get_companias_ofertas(id_oferta: int, db: Session = Depends(get_bd)):
    offer = db.get(OfertaModel, id_oferta)
    if offer is None:
        return {"status": "error", "message": "Oferta no encontrada"}
    return {"status": "ok", "data": offer.companias}
