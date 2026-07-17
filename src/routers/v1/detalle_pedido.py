from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.schemas.detalle_pedido import DetallePedido, DetallePedidoPatch
from src.models.detalle_pedido import DetallePedidoModel

router = APIRouter()

@router.get("/")
def get_detalles_pedido(db: Session = Depends(get_bd)):
    stmt = select(DetallePedidoModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_pedido}/{id_producto}")
def get_detalle_pedido(id_pedido: int, id_producto: int, db: Session = Depends(get_bd)):
    stmt = select(DetallePedidoModel).where(
        DetallePedidoModel.id_pedido == id_pedido,
        DetallePedidoModel.id_producto == id_producto
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Detalle de pedido no encontrado"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_detalle_pedido(detalle: DetallePedido, db: Session = Depends(get_bd)):
    try:
        new_detalle = DetallePedidoModel(**detalle.model_dump())
        db.add(new_detalle)
        db.commit()
        db.refresh(new_detalle)
        return {"status": "ok", "message": "Detalle de pedido creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_pedido}/{id_producto}")
def update_detalle_pedido(id_pedido: int, id_producto: int, detalle: DetallePedido, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetallePedidoModel).where(
            DetallePedidoModel.id_pedido == id_pedido,
            DetallePedidoModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de pedido no encontrado"} 
        
        for key, value in detalle.model_dump().items():
            setattr(query_detalle, key, value)

        db.commit()
        db.refresh(query_detalle)
        return {"status": "ok", "message": "Detalle de pedido actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_pedido}/{id_producto}")
def update_detalle_pedido_parcial(id_pedido: int, id_producto: int, detalle: DetallePedidoPatch, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetallePedidoModel).where(
            DetallePedidoModel.id_pedido == id_pedido,
            DetallePedidoModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de pedido no encontrado"} 
        
        for key, value in detalle.model_dump().items():
            if value is not None:
                setattr(query_detalle, key, value)

        db.commit()
        db.refresh(query_detalle)
        return {"status": "ok", "message": "Detalle de pedido actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_pedido}/{id_producto}")
def delete_detalle_pedido(id_pedido: int, id_producto: int, db: Session = Depends(get_bd)):
    try:
        stmt = select(DetallePedidoModel).where(
            DetallePedidoModel.id_pedido == id_pedido,
            DetallePedidoModel.id_producto == id_producto
        )
        query_detalle = db.execute(stmt).scalar_one_or_none()
        if not query_detalle:
            return {"status": "error", "message": "Detalle de pedido no encontrado"} 
        db.delete(query_detalle)
        db.commit()
        return {"status": "ok", "message": "Detalle de pedido eliminado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 
