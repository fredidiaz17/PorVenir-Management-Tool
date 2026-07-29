from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.producto_etiqueta import ProductoEtiqueta
from src.models.producto_etiqueta import ProductoEtiquetaModel

router = APIRouter()

@router.get("/")
def get_producto_etiquetas(db: Session = Depends(get_bd)):
    stmt = select(ProductoEtiquetaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_producto}/{id_etiqueta}")
def get_producto_etiqueta(id_producto: int, id_etiqueta: int, db: Session = Depends(get_bd)):
    stmt = select(ProductoEtiquetaModel).where(
        ProductoEtiquetaModel.id_producto == id_producto,
        ProductoEtiquetaModel.id_etiqueta == id_etiqueta
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Relación no encontrada"})
    return {"status": "ok", "data": result} 

@router.post("/")
def create_producto_etiqueta(producto_etiqueta: ProductoEtiqueta, db: Session = Depends(get_bd)):
    try:
        new_relacion = ProductoEtiquetaModel(**producto_etiqueta.model_dump())
        db.add(new_relacion)
        db.commit()
        db.refresh(new_relacion)
        return {"status": "ok", "message": "Relación creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e)}) 

@router.put("/{id_producto}/{id_etiqueta}")
def update_producto_etiqueta(id_producto: int, id_etiqueta: int, producto_etiqueta: ProductoEtiqueta, db: Session = Depends(get_bd)):
    try:
        stmt = select(ProductoEtiquetaModel).where(
            ProductoEtiquetaModel.id_producto == id_producto,
            ProductoEtiquetaModel.id_etiqueta == id_etiqueta
        )
        query_relacion = db.execute(stmt).scalar_one_or_none()
        if not query_relacion:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Relación no encontrada"}) 
        
        query_relacion.estado = producto_etiqueta.estado

        db.commit()
        db.refresh(query_relacion)
        return {"status": "ok", "message": "Relación actualizada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e)}) 

@router.delete("/{id_producto}/{id_etiqueta}")
def delete_producto_etiqueta(id_producto: int, id_etiqueta: int, db: Session = Depends(get_bd)):
    try:
        stmt = select(ProductoEtiquetaModel).where(
            ProductoEtiquetaModel.id_producto == id_producto,
            ProductoEtiquetaModel.id_etiqueta == id_etiqueta
        )
        query_relacion = db.execute(stmt).scalar_one_or_none()
        if not query_relacion:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Relación no encontrada"}) 
        db.delete(query_relacion)
        db.commit()
        return {"status": "ok", "message": "Relación eliminada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e)}) 
