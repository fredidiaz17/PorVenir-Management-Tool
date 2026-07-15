from src.schemas.producto import Producto
from fastapi import APIRouter, Depends      
from src.database.db_conn import get_bd

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.schemas.producto import CreateProducto, ProductoPatch

from src.models.producto import ProductoModel

router = APIRouter()

@router.get("/")
def get_productos(db: Session = Depends(get_bd)):
    stmt = select(ProductoModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_producto}")
def get_producto(id_producto: int, db: Session = Depends(get_bd)):
    stmt = select(ProductoModel).where(ProductoModel.id_producto == id_producto)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Producto no encontrado"}
    return {"status": "ok", "data": result} 

@router.post("/")
def create_producto(producto: CreateProducto, db: Session = Depends(get_bd)):
    try:
        new_producto = ProductoModel(**producto.model_dump()) # Desenpaquetado. El schema debe tener las mismas key que el modelo para funcionar. (OJO)
        db.add(new_producto)
        db.commit()
        db.refresh(new_producto)
        
        return {"status": "ok", "message": "Producto creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_producto}")
def update_producto(id_producto: int, producto: Producto, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto) # Se busca el producto por PK.
        if not query_producto: # Si no se encuentra el producto.
            return {"status": "error", "message": "Producto no encontrado"} 
        
        # Si se encuentra el producto.
        query_producto.nombre = producto.nombre
        query_producto.cantidad_stock = producto.cantidad_stock
        query_producto.unidad_medida = producto.unidad_medida
        query_producto.precio_compra = producto.precio_compra
        query_producto.precio_venta = producto.precio_venta
        query_producto.porcentaje_iva = producto.porcentaje_iva
        query_producto.id_marca = producto.id_marca

        db.commit()
        db.refresh(query_producto)
        return {"status": "ok", "message": "Producto actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.patch("/{id_producto}")
def update_producto_parcial(id_producto: int, producto: ProductoPatch, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto) # Se busca el producto por PK.
        if not query_producto: # Si no se encuentra el producto.
            return {"status": "error", "message": "Producto no encontrado"} 
        
        # Si se encuentra el producto.
        for key, value in producto.model_dump().items():
            if value is not None:
                setattr(query_producto, key, value)

        db.commit()
        db.refresh(query_producto)
        return {"status": "ok", "message": "Producto actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_producto}")
def delete_producto(id_producto: int, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto)
        if not query_producto: # Si no se encuentra el producto.
            return {"status": "error", "message": "Producto no encontrado"} 
        db.delete(query_producto)
        db.commit()
        return {"status": "ok", "message": "Producto eliminado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 


