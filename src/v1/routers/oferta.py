
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.oferta import Oferta, OfertaPatch
from src.models import OfertaModel, ProductoModel, CompaniaModel, EtiquetaModel, MarcaModel

router = APIRouter()

@router.get("/")
def get_ofertas(db: Session = Depends(get_bd)):
    stmt = select(OfertaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_oferta}")
def get_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta).options(
        selectinload(OfertaModel.productos),
        selectinload(OfertaModel.companias),
        selectinload(OfertaModel.etiquetas),
        selectinload(OfertaModel.marcas)
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"})
    return {"status": "ok", "data": result} 

@router.post("/")
def create_oferta(oferta: Oferta, db: Session = Depends(get_bd)):
    try:
        new_oferta = OfertaModel(**oferta.model_dump())
        db.add(new_oferta)
        db.commit()
        db.refresh(new_oferta)
        return {"status": "ok", "message": "Oferta creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.put("/{id_oferta}")
def update_oferta(id_oferta: int, oferta: Oferta, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        
        for key, value in oferta.model_dump().items():
            setattr(query_oferta, key, value)

        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Oferta actualizada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.patch("/{id_oferta}")
def update_oferta_parcial(id_oferta: int, oferta: OfertaPatch, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        
        for key, value in oferta.model_dump().items():
            if value is not None:
                setattr(query_oferta, key, value)

        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Oferta actualizada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/{id_oferta}")
def delete_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    try:
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        db.delete(query_oferta)
        db.commit()
        return {"status": "ok", "message": "Oferta eliminada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})


# Vinculación y Desvinculación de Ofertas

# Vinculaciones

@router.post("/vinculacion/Producto/{id_producto}/Oferta/{id_oferta}")
def vincular_producto_oferta(id_oferta: int, id_producto: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_producto = db.get(ProductoModel, id_producto)
        if not query_producto:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"})
        query_oferta.productos.append(query_producto) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Producto vinculado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.post("/vinculacion/Compania/{id_compania}/Oferta/{id_oferta}")
def vincular_compania_oferta(id_oferta: int, id_compania: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_compania = db.get(CompaniaModel, id_compania)
        if not query_compania:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Compania no encontrada"})
        
        query_oferta.companias.append(query_compania) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Compania vinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.post("/vinculacion/Etiqueta/{id_etiqueta}/Oferta/{id_oferta}")
def vincular_etiqueta_oferta(id_oferta: int, id_etiqueta: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_etiqueta = db.get(EtiquetaModel, id_etiqueta)
        if not query_etiqueta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"})
        
        query_oferta.etiquetas.append(query_etiqueta) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Etiqueta vinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.post("/vinculacion/Marca/{id_marca}/Oferta/{id_oferta}")
def vincular_marca_oferta(id_oferta: int, id_marca: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_marca = db.get(MarcaModel, id_marca)
        if not query_marca:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})
        
        query_oferta.marcas.append(query_marca) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Marca vinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 


# Desvinculaciones

@router.delete("/desvinculacion/Producto/{id_producto}/Oferta/{id_oferta}")
def desvincular_producto_oferta(id_oferta: int, id_producto: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_producto = db.get(ProductoModel, id_producto)
        if not query_producto:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Producto no encontrado"})

        query_oferta.productos.remove(query_producto) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Producto desvinculado exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/desvinculacion/Compania/{id_compania}/Oferta/{id_oferta}")
def desvincular_compania_oferta(id_oferta: int, id_compania: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_compania = db.get(CompaniaModel, id_compania)
        if not query_compania:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Compania no encontrada"})

        query_oferta.companias.remove(query_compania) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Compania desvinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/desvinculacion/Etiqueta/{id_etiqueta}/Oferta/{id_oferta}")
def desvincular_etiqueta_oferta(id_oferta: int, id_etiqueta: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_etiqueta = db.get(EtiquetaModel, id_etiqueta)
        if not query_etiqueta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Etiqueta no encontrada"})

        query_oferta.etiquetas.remove(query_etiqueta) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Etiqueta desvinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

@router.delete("/desvinculacion/Marca/{id_marca}/Oferta/{id_oferta}")
def desvincular_marca_oferta(id_oferta: int, id_marca: int, db: Session = Depends(get_bd)):
    try: 
        query_oferta = db.get(OfertaModel, id_oferta)
        if not query_oferta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"}) 
        query_marca = db.get(MarcaModel, id_marca)
        if not query_marca:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Marca no encontrada"})

        query_oferta.marcas.remove(query_marca) 
        db.commit()
        db.refresh(query_oferta)
        return {"status": "ok", "message": "Marca desvinculada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})


# Listados de vinculaciones

@router.get("/{id_oferta}/productos")
def get_productos_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta).options(
        selectinload(OfertaModel.productos)
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"})
    return {"status": "ok", "data": result.productos}

@router.get("/{id_oferta}/companias")
def get_companias_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta).options(
        selectinload(OfertaModel.companias)
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"})
    return {"status": "ok", "data": result.companias}

@router.get("/{id_oferta}/etiquetas")
def get_etiquetas_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta).options(
        selectinload(OfertaModel.etiquetas)
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"})
    return {"status": "ok", "data": result.etiquetas}

@router.get("/{id_oferta}/marcas")
def get_marcas_oferta(id_oferta: int, db: Session = Depends(get_bd)):
    stmt = select(OfertaModel).where(OfertaModel.id_oferta == id_oferta).options(
        selectinload(OfertaModel.marcas)
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no encontrada"})
    return {"status": "ok", "data": result.marcas}