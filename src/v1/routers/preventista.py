from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.preventista import Preventista, PreventistaPatch
from src.models.preventista import PreventistaModel

router = APIRouter()

@router.get("/")
def get_preventistas(db: Session = Depends(get_bd)):
    stmt = select(PreventistaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_preventista}")
def get_preventista(id_preventista: int, db: Session = Depends(get_bd)):
    stmt = select(PreventistaModel).where(PreventistaModel.id_preventista == id_preventista)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Preventista no encontrado"})
    return {"status": "ok", "data": result} 

@router.post("/")
def create_preventista(preventista: Preventista, db: Session = Depends(get_bd)):
    try:
        new_preventista = PreventistaModel(**preventista.model_dump())
        db.add(new_preventista)
        db.commit()
        db.refresh(new_preventista)
        return {"status": "ok", "message": "Preventista creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.put("/{id_preventista}")
def update_preventista(id_preventista: int, preventista: Preventista, db: Session = Depends(get_bd)):
    try:
        query_preventista = db.get(PreventistaModel, id_preventista)
        if not query_preventista:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Preventista no encontrado"}) 
        
        for key, value in preventista.model_dump().items():
            setattr(query_preventista, key, value)

        db.commit()
        db.refresh(query_preventista)
        return {"status": "ok", "message": "Preventista actualizado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.patch("/{id_preventista}")
def update_preventista_parcial(id_preventista: int, preventista: PreventistaPatch, db: Session = Depends(get_bd)):
    try:
        query_preventista = db.get(PreventistaModel, id_preventista)
        if not query_preventista:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Preventista no encontrado"}) 
        
        for key, value in preventista.model_dump().items():
            if value is not None:
                setattr(query_preventista, key, value)

        db.commit()
        db.refresh(query_preventista)
        return {"status": "ok", "message": "Preventista actualizado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/{id_preventista}")
def delete_preventista(id_preventista: int, db: Session = Depends(get_bd)):
    try:
        query_preventista = db.get(PreventistaModel, id_preventista)
        if not query_preventista:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Preventista no encontrado"}) 
        db.delete(query_preventista)
        db.commit()
        return {"status": "ok", "message": "Preventista eliminado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 
