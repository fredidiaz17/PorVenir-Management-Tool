
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from src.database.db_conn import get_bd

from src.v1.schemas.venta import Venta, VentaPatch
from src.v1.schemas.detalle_venta import CreateDetalleVenta
from src.v1.schemas.enums import MedioPago

from src.models.venta import VentaModel
from src.models import DetalleVentaModel
from src.models.producto import ProductoModel
from src.models.deuda import DeudaModel

router = APIRouter()

def update_stock(detalles: list[dict],db: Session): 
    
    for detalle in detalles: 
        id_producto = detalle.get("id_producto", None)
        cantidad = detalle.get("cantidad", None)
        
        query_producto = db.get(ProductoModel, id_producto)

        # No se puede hacer la venta si el producto no existe o si el stock es menor a la cantidad pedida
        if not query_producto or query_producto.cantidad_stock < cantidad:
            return False

        query_producto.cantidad_stock -= cantidad
    
    db.flush()
    return True

def return_stock(detalles: list[dict],db: Session):
    for detalle in detalles:
        id_producto = detalle.get("id_producto", None)
        cantidad = detalle.get("cantidad", None)
        
        query_producto = db.get(ProductoModel, id_producto)

        # Puede que el producto se haya eliminado, simplemente se elimina el detalle
        if query_producto: 
            # Se devuelve el stock del producto
            query_producto.cantidad_stock += cantidad

    db.flush()
    return True

# Retorna todas las ventas. Una "vista previa" de ellas
@router.get("/")
def get_ventas(db: Session = Depends(get_bd)):
    stmt = select(VentaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

# Retorna una venta en concreto + sus detalles
@router.get("/{id_venta}")
def get_venta(id_venta: int, db: Session = Depends(get_bd)):
    stmt = select(VentaModel).where(VentaModel.id_venta == id_venta).options(selectinload(VentaModel.detalle_venta))
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Venta no encontrada"})
    return {"status": "ok", "data": result} 

# Crea una venta con sus detalles. Debe restar stock existente
# Si es fiado, debe crear una deuda. Ver regla ER-058
@router.post("/")
def create_venta(venta: Venta, db: Session = Depends(get_bd)):
    try:
        # Se crea la venta, se crean sus detalles y se descuenta stock de los productos.
        venta_dict = venta.model_dump()
        detalles_venta = venta_dict.pop("detalles_venta", None)

        if detalles_venta is None: 
            raise HTTPException(status_code= 400, detail={"status": "error", "message": "La venta no puede estar vacia"})

        new_venta = VentaModel(**venta_dict)

        db.add(new_venta)
        db.flush()
        
        for detalle in detalles_venta:
            detalle["id_venta"] = new_venta.id_venta
            new_detalle = DetalleVentaModel(**detalle)
            db.add(new_detalle)
            db.flush()

        detalles = [CreateDetalleVenta.model_validate(detalle).model_dump() for detalle in detalles_venta]

        updated = update_stock(detalles, db)
        if not updated: 
            raise HTTPException(status_code=400, detail={"status": "error", "message": "Ha ocurrido un error durante la actualización del stock"})
        
        # Genera deuda?
        if new_venta.medio_pago == MedioPago.FIADO:
            # ¿Ya existe?
            stmt = select(DeudaModel).where(DeudaModel.id_cliente == new_venta.id_cliente)
            deuda = db.execute(stmt).scalar_one_or_none()

            if deuda:
                deuda.saldo_pendiente += new_venta.total
            
            else:
                deuda = DeudaModel(
                    id_cliente=new_venta.id_cliente,
                    saldo_pendiente=new_venta.total,
                    estado=True
                )
            db.add(deuda)
            db.flush()

        db.commit()
        db.refresh(new_venta)

        
        return {"status": "ok", "message": "Venta creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

# Una venta no se puede actualizar
# Pero si se puede anular (ver regla ER-055)
@router.post("/{id_venta}/anular")
def anular_venta(id_venta: int, db: Session = Depends(get_bd)):
    try:
        
        stmt = select(VentaModel).where(VentaModel.id_venta == id_venta).options(selectinload(VentaModel.detalle_venta))
        query_venta = db.execute(stmt).scalar_one_or_none()
        
        if not query_venta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Venta no encontrada"})

        detalles = [CreateDetalleVenta.model_validate(detalle).model_dump() for detalle in query_venta.detalle_venta]
        
        # Regresar stock
        updated = return_stock(detalles, db)
        if not updated: 
            raise HTTPException(status_code=400, detail={"status": "error", "message": "Ha ocurrido un error durante la anulación de la venta"})
        
        # Eliminar venta
        # No es necesario eliminar detalle por detalle, el on cascade se hará cargo.
        db.delete(query_venta)
        db.commit() 
        return {"status": "ok", "message": "Venta anulada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 

# On cascade eliminará los detalles de la venta
@router.delete("/{id_venta}")
def delete_venta(id_venta: int, db: Session = Depends(get_bd)):
    try:
        query_venta = db.get(VentaModel, id_venta)
        if not query_venta:
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Venta no encontrada"}) 
        db.delete(query_venta)
        db.commit()
        return {"status": "ok", "message": "Venta eliminada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)}) 
