
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.db_conn import get_bd

from src.models.cliente import ClienteModel

from src.v1.schemas.cliente import Cliente, ClientePatch
    
router = APIRouter() 


@router.get("/") 
def get_clientes(db: Session = Depends(get_bd)):
    stmt = select(ClienteModel)
    result = db.execute(stmt).scalars().all() 
    return {"status": "ok", "data": result}


@router.get("/{cliente_id}")
def get_cliente(cliente_id: int, db: Session = Depends(get_bd)):
    query_cliente = db.get(ClienteModel, cliente_id)
    if query_cliente is None:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Cliente no encontrado"}) 
    return {"status": "ok", "data": query_cliente}

@router.post("/") 
def create_cliente(cliente: Cliente, db: Session = Depends(get_bd)):
    try:
        new_cliente = ClienteModel(nombre=cliente.nombre, telefono=cliente.telefono)
        db.add(new_cliente)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": e.orig})
    
    return {"status": "ok", "message": "Cliente creado exitosamente"}
    

@router.put("/{cliente_id}")
def update_cliente(cliente_id: int, cliente: Cliente, db: Session = Depends(get_bd)): 
    try:
        query_cliente = db.get(ClienteModel, cliente_id)
        if not query_cliente:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Cliente no encontrado"})
        
        query_cliente.nombre = cliente.nombre
        query_cliente.telefono = cliente.telefono
        
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": e.orig})
    
    return {"status": "ok", "message": "Cliente actualizado exitosamente"}

@router.patch("/{cliente_id}")
def update_cliente_parcial(cliente_id: int, cliente: ClientePatch, db: Session = Depends(get_bd)):
    try:
        query_cliente = db.get(ClienteModel, cliente_id) 
        if not query_cliente: 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Cliente no encontrado"})
        
        for key, value in cliente.model_dump().items():
            if value is not None:
                setattr(query_cliente, key, value) 
        
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": e.orig})
    
    return {"status": "ok", "message": "Cliente actualizado exitosamente"}

@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_bd)):
    try:
        query_cliente = db.get(ClienteModel, cliente_id)
        if not query_cliente: 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Cliente no encontrado"})
        db.delete(query_cliente)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": e.orig})

    return {"status": "ok", "message": "Cliente eliminado exitosamente"}

