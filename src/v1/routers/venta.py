from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.venta import Venta, VentaPatch
from src.models.venta import VentaModel

router = APIRouter()

@router.get("/")
def get_ventas(db: Session = Depends(get_bd)):
    stmt = select(VentaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_venta}")
def get_venta(id_venta: int, db: Session = Depends(get_bd)):
    stmt = select(VentaModel).where(VentaModel.id_venta == id_venta)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Venta no encontrada"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_venta(venta: Venta, db: Session = Depends(get_bd)):
    try:
        new_venta = VentaModel(**venta.model_dump())
        db.add(new_venta)
        db.commit()
        db.refresh(new_venta)
        return {"status": "ok", "message": "Venta creada exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_venta}")
def update_venta(id_venta: int, venta: Venta, db: Session = Depends(get_bd)):
    try:
        query_venta = db.get(VentaModel, id_venta)
        if not query_venta:
            return {"status": "error", "message": "Venta no encontrada"} 
        
        for key, value in venta.model_dump().items():
            setattr(query_venta, key, value)

        db.commit()
        db.refresh(query_venta)
        return {"status": "ok", "message": "Venta actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_venta}")
def update_venta_parcial(id_venta: int, venta: VentaPatch, db: Session = Depends(get_bd)):
    try:
        query_venta = db.get(VentaModel, id_venta)
        if not query_venta:
            return {"status": "error", "message": "Venta no encontrada"} 
        
        for key, value in venta.model_dump().items():
            if value is not None:
                setattr(query_venta, key, value)

        db.commit()
        db.refresh(query_venta)
        return {"status": "ok", "message": "Venta actualizada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_venta}")
def delete_venta(id_venta: int, db: Session = Depends(get_bd)):
    try:
        query_venta = db.get(VentaModel, id_venta)
        if not query_venta:
            return {"status": "error", "message": "Venta no encontrada"} 
        db.delete(query_venta)
        db.commit()
        return {"status": "ok", "message": "Venta eliminada exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 
