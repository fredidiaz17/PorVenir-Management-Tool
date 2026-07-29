from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.deuda import Deuda, DeudaPatch
from src.models.deuda import DeudaModel

router = APIRouter()

@router.get("/")
def get_deudas(db: Session = Depends(get_bd)):
    stmt = select(DeudaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_deuda}")
def get_deuda(id_deuda: int, db: Session = Depends(get_bd)):
    stmt = select(DeudaModel).where(DeudaModel.id_deuda == id_deuda)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Deuda no encontrada"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_deuda(deuda: Deuda, db: Session = Depends(get_bd)):
    try:
        new_deuda = DeudaModel(**deuda.model_dump())
        db.add(new_deuda)
        db.commit()
        db.refresh(new_deuda)
        return {"status": "ok", "message": "Deuda creada exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_deuda}")
def update_deuda(id_deuda: int, deuda: Deuda, db: Session = Depends(get_bd)):
    try:
        query_deuda = db.get(DeudaModel, id_deuda)
        if not query_deuda:
            return {"status": "error", "message": "Deuda no encontrada"} 
        
        for key, value in deuda.model_dump().items():
            setattr(query_deuda, key, value)

        db.commit()
        db.refresh(query_deuda)
        return {"status": "ok", "message": "Deuda actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_deuda}")
def update_deuda_parcial(id_deuda: int, deuda: DeudaPatch, db: Session = Depends(get_bd)):
    try:
        query_deuda = db.get(DeudaModel, id_deuda)
        if not query_deuda:
            return {"status": "error", "message": "Deuda no encontrada"} 
        
        for key, value in deuda.model_dump().items():
            if value is not None:
                setattr(query_deuda, key, value)

        db.commit()
        db.refresh(query_deuda)
        return {"status": "ok", "message": "Deuda actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_deuda}")
def delete_deuda(id_deuda: int, db: Session = Depends(get_bd)):
    try:
        query_deuda = db.get(DeudaModel, id_deuda)
        if not query_deuda:
            return {"status": "error", "message": "Deuda no encontrada"} 
        db.delete(query_deuda)
        db.commit()
        return {"status": "ok", "message": "Deuda eliminada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 
