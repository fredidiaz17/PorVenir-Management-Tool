
from fastapi import APIRouter, Depends, HTTPException  
from src.database.db_conn import get_bd

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.v1.schemas.producto import Producto, ProductoPatch

from src.models.producto import ProductoModel
from src.models.oferta import OfertaModel

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
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"})
    return {"status": "ok", "data": result} 

@router.post("/")
def create_producto(producto: Producto, db: Session = Depends(get_bd)):
    try:
        new_producto = ProductoModel(**producto.model_dump()) # Desenpaquetado. El schema debe tener las mismas key que el modelo para funcionar. (OJO)
        db.add(new_producto)
        db.commit()
        db.refresh(new_producto)
        
        return {"status": "ok", "message": "Producto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.put("/{id_producto}")
def update_producto(id_producto: int, producto: Producto, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto) # Se busca el producto por PK.
        if not query_producto: # Si no se encuentra el producto.
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"}) 
        
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
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.patch("/{id_producto}")
def update_producto_parcial(id_producto: int, producto: ProductoPatch, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto) # Se busca el producto por PK.
        if not query_producto: # Si no se encuentra el producto.
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"}) 
        
        # Si se encuentra el producto.
        for key, value in producto.model_dump().items():
            if value is not None:
                setattr(query_producto, key, value)

        db.commit()
        db.refresh(query_producto)
        return {"status": "ok", "message": "Producto actualizado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/{id_producto}")
def delete_producto(id_producto: int, db: Session = Depends(get_bd)):
    try:
        query_producto = db.get(ProductoModel, id_producto)
        if not query_producto: # Si no se encuentra el producto.
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"}) 
        db.delete(query_producto)
        db.commit()
        return {"status": "ok", "message": "Producto eliminado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 



# N:M con Oferta

# Todas las ofertas que se aplican al producto dado.
@router.get("/{id_producto}/ofertas")
def get_ofertas_productos(id_producto: int, db: Session = Depends(get_bd)):
    product = db.get(ProductoModel, id_producto)
    if product is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"})

    return {"status": "ok", "data": product.ofertas} # SQLAlchemy hace el Join automaticamente.


@router.post("/{id_producto}/ofertas/{id_oferta}")
def post_oferta_producto(id_producto: int,id_oferta: int, db: Session = Depends(get_bd)):
    
    product = db.get(ProductoModel, id_producto)
    offer = db.get(OfertaModel, id_oferta)
    if product is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o producto no encontrado"})
    
    # Se asigna el producto a la oferta por medio de la relación que ya tenia definida.
    offer.productos.append(product)
    db.commit()
    return {"status": "ok", "message": "Oferta aplicada a producto exitosamente"}


@router.delete("/{id_producto}/ofertas/{id_oferta}")
def delete_oferta_producto(id_producto: int,id_oferta: int, db: Session = Depends(get_bd)):
    product = db.get(ProductoModel, id_producto)
    offer = db.get(OfertaModel, id_oferta)

    if product is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o producto no encontrado"})

    if offer not in product.ofertas:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no aplicada a producto"})

    product.ofertas.remove(offer)
    db.commit()
    return {"status": "ok", "message": "Oferta eliminada de producto exitosamente"}
