from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.detalle_venta import CreateDetalleVenta, DetalleVentaPatch, UpdateDetalleVenta
from src.models.detalle_venta import DetalleVentaModel

router = APIRouter()

@router.get("/{id_venta}")
def get_detalles_venta(id_venta: int, db: Session = Depends(get_bd)):
    stmt = select(DetalleVentaModel).where(DetalleVentaModel.id_venta == id_venta)
    result = db.execute(stmt).scalars().all()
    if not result: 
        return {"status": "error", "message": "Detalles de venta no encontrados"}
    return {"status": "ok", "data": result} 

@router.get("/{id_venta}/{id_producto}")
def get_detalle_venta(id_venta: int, id_producto: int, db: Session = Depends(get_bd)):
    stmt = select(DetalleVentaModel).where(
        DetalleVentaModel.id_venta == id_venta,
        DetalleVentaModel.id_producto == id_producto
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Detalle de venta no encontrado"}
    return {"status": "ok", "data": result} 

@router.post("/{id_venta}")
def create_detalle_venta(id_venta: int, detalle: CreateDetalleVenta, db: Session = Depends(get_bd)):
    try:
        new_detalle = DetalleVentaModel(**detalle.model_dump(), id_venta=id_venta)
        db.add(new_detalle)
        db.commit()
        db.refresh(new_detalle)
        return {"status": "ok", "message": "Detalle de venta creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_venta}/{id_producto}")
def update_detalle_venta(id_venta: int, id_producto: int, detalle: UpdateDetalleVenta, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetalleVentaModel).where(
            DetalleVentaModel.id_venta == id_venta,
            DetalleVentaModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de venta no encontrado"} 
        
        for key, value in detalle.model_dump().items():
            setattr(query_detalle, key, value)

        db.commit()
        db.refresh(query_detalle)
        return {"status": "ok", "message": "Detalle de venta actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_venta}/{id_producto}")
def update_detalle_venta_parcial(id_venta: int, id_producto: int, detalle: DetalleVentaPatch, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetalleVentaModel).where(
            DetalleVentaModel.id_venta == id_venta,
            DetalleVentaModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de venta no encontrado"} 
        
        for key, value in detalle.model_dump().items():
            if value is not None:
                setattr(query_detalle, key, value)

        db.commit()
        db.refresh(query_detalle)
        return {"status": "ok", "message": "Detalle de venta actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_venta}/{id_producto}")
def delete_detalle_venta(id_venta: int, id_producto: int, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetalleVentaModel).where(
            DetalleVentaModel.id_venta == id_venta,
            DetalleVentaModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de venta no encontrado"} 
        db.delete(query_detalle)
        db.commit()
        return {"status": "ok", "message": "Detalle de venta eliminado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 
