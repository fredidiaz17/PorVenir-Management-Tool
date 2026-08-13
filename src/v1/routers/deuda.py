from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_conn import get_bd
from src.v1.schemas.deuda import DeudaAbono
from src.models.deuda import DeudaModel

router = APIRouter()

@router.get("/")
def get_deudas(db: Session = Depends(get_bd)):
    stmt = select(DeudaModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 

@router.get("/{id_deuda}")
def get_deuda(id_deuda: int, db: Session = Depends(get_bd)):
    stmt = select(DeudaModel).where(DeudaModel.id_deuda == id_deuda)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        raise HTTPException(status_code=404, detail= {"status": "error", "message": "Deuda no encontrada"})
    return {"status": "ok", "data": result} 
# No hay post de creación de deuda dado a que una deuda se debe crear en la venta. Ver regla ER-058

# PERO, si hay post para ABONAR un monto a la deuda.

@router.post("/{id_deuda}")
def abono_deuda(id_deuda: int, abono: DeudaAbono, db: Session = Depends(get_bd)):
    query_deuda = db.get(DeudaModel, id_deuda)
    if not query_deuda:
        raise HTTPException(status_code=404, detail= {"status": "error", "message": "Deuda no encontrada"})

    monto_abonado = abono.monto_abonado
    if monto_abonado <= 0:
        raise HTTPException(status_code=400, detail= {"status": "error", "message": "Monto de abono invalido"})

    query_deuda.saldo_pendiente -= monto_abonado
    
    if query_deuda.saldo_pendiente == 0:
        query_deuda.estado = False
    

    db.commit()
    return {"status": "ok", "data": "Monto abonado exitosamente"}

# No hay put ni patch, el usuario solo abona un monto, no lo edita directamente.

@router.delete("/{id_deuda}")
def delete_deuda(id_deuda: int, db: Session = Depends(get_bd)):
    try:
        query_deuda = db.get(DeudaModel, id_deuda)
        if not query_deuda:
            raise HTTPException(status_code=404, detail= {"status": "error", "message": "Deuda no encontrada"}) 
        db.delete(query_deuda)
        db.commit()
        return {"status": "ok", "message": "Deuda eliminada exitosamente"} 
    except Exception as e:
        raise HTTPException(status_code=400, detail= {"status": "error", "message": str(e), "origin": getattr(e, "orig", None)} ) 
