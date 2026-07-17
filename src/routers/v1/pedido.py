from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.schemas.pedido import Pedido, PedidoPatch
from src.models.pedido import PedidoModel

router = APIRouter()

@router.get("/")
def get_pedidos(db: Session = Depends(get_bd)):
    stmt = select(PedidoModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_pedido}")
def get_pedido(id_pedido: int, db: Session = Depends(get_bd)):
    stmt = select(PedidoModel).where(PedidoModel.id_pedido == id_pedido)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Pedido no encontrado"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_pedido(pedido: Pedido, db: Session = Depends(get_bd)):
    try:
        new_pedido = PedidoModel(**pedido.model_dump())
        db.add(new_pedido)
        db.commit()
        db.refresh(new_pedido)
        return {"status": "ok", "message": "Pedido creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_pedido}")
def update_pedido(id_pedido: int, pedido: Pedido, db: Session = Depends(get_bd)):
    try:
        query_pedido = db.get(PedidoModel, id_pedido)
        if not query_pedido:
            return {"status": "error", "message": "Pedido no encontrado"} 
        
        for key, value in pedido.model_dump().items():
            setattr(query_pedido, key, value)

        db.commit()
        db.refresh(query_pedido)
        return {"status": "ok", "message": "Pedido actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_pedido}")
def update_pedido_parcial(id_pedido: int, pedido: PedidoPatch, db: Session = Depends(get_bd)):
    try:
        query_pedido = db.get(PedidoModel, id_pedido)
        if not query_pedido:
            return {"status": "error", "message": "Pedido no encontrado"} 
        
        for key, value in pedido.model_dump().items():
            if value is not None:
                setattr(query_pedido, key, value)

        db.commit()
        db.refresh(query_pedido)
        return {"status": "ok", "message": "Pedido actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_pedido}")
def delete_pedido(id_pedido: int, db: Session = Depends(get_bd)):
    try:
        query_pedido = db.get(PedidoModel, id_pedido)
        if not query_pedido:
            return {"status": "error", "message": "Pedido no encontrado"} 
        db.delete(query_pedido)
        db.commit()
        return {"status": "ok", "message": "Pedido eliminado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 
