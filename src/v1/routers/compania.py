
from fastapi import APIRouter, Depends, HTTPException # Depends es para el manejo de dependencias. Reutilizar codigo mas limpio.
from sqlalchemy.orm import Session
from sqlalchemy import select

# Modelos
from src.models.compania import CompaniaModel
from src.models.oferta import OfertaModel

# Schemas
from src.v1.schemas.compania import Compania

from src.database.db_conn import get_bd # Para obtener la sesión de la bd

router = APIRouter() # El Router recibe la petición y la dirige a su respectiva ruta

# Los respectivos metodos.
@router.get("/") # Define la ruta
def get_companias(db: Session = Depends(get_bd)): # Se define la dependencia. Es decir, se ejecuta la funcion get_bd() y se pasa su resultado a la funcion get_companias().
    stmt = select(CompaniaModel) # Se define el statement a ejecutar
    #  select es mas flexible que db.get()

    # Se ejecuta la consulta. 
    result = db.execute(stmt).scalars().all() # Scalars permite que result sea una lista de instancias del modelo. all devuelve todos los resultados
    return {"status": "ok", "data": result} # Se devuelve el resultado.


@router.get("/{compania_id}")
def get_compania(compania_id: int, db: Session = Depends(get_bd)):
    query_compania = db.get(CompaniaModel, compania_id) # db.get solo sirve si se sabe la PK. 

    if not query_compania: # Si no se encuentra la compañia. 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Compañia no encontrada"})
    # if result is None:
        # raise HTTPException(status_code=404, detail="Compania no encontrada") 
    return {"status": "ok", "data": query_compania}# Se devuelve el resultado.

@router.post("/")
def create_compania(compania:Compania, db: Session = Depends(get_bd)):
    try:
        new_company = CompaniaModel(nombre=compania.nombre) # Se crea una instancia del modelo.
    
        db.add(new_company) # Se agrega la instancia (compania) a la sesión.
        db.commit() # Se confirma la transacción.
        db.refresh(new_company) # Se actualiza la instancia con los datos de la base de datos (como el id).

    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia creada exitosamente"}
    

@router.put("/{compania_id}")
def update_compania(compania_id: int, compania:Compania, db: Session = Depends(get_bd)):
    try:
        query_compania = db.get(CompaniaModel, compania_id) # Se busca la compañia por PK.
        if not query_compania: # Si no se encuentra la compañia. 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Compañia no encontrada"})
            
        query_compania.nombre = compania.nombre # Se actualiza el nombre de la compañia.

        db.commit() # Se confirma la transacción.
         
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia actualizada exitosamente"}

@router.delete("/{compania_id}")
def delete_compania(compania_id: int, db: Session = Depends(get_bd)):
    try:
        query_compania = db.get(CompaniaModel, compania_id) # Se ejecuta la consulta y se devuelve el primer resultado.
        if not query_compania: # Si no se encuentra la compañia. 
            raise HTTPException(status_code=404, detail={"status": "error", "message": "Compañia no encontrada"})

        db.delete(query_compania) # Se elimina la instancia.
        db.commit() # Se confirma la transacción.    
         
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "origin": getattr(e, "orig", None)})
    
    return {"status": "ok", "message": "Compañia eliminada exitosamente"}    

# N:M con Oferta

# Todas las ofertas que se aplican a la compania dada.
@router.get("/{compania_id}/ofertas")
def get_ofertas_compania(compania_id: int, db: Session = Depends(get_bd)):
    compania = db.get(CompaniaModel, compania_id)
    if compania is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Compañia no encontrada"})

    return {"status": "ok", "data": compania.ofertas}


@router.post("/{compania_id}/ofertas/{id_oferta}")
def post_oferta_compania(compania_id: int, id_oferta: int, db: Session = Depends(get_bd)):
    compania = db.get(CompaniaModel, compania_id)
    offer = db.get(OfertaModel, id_oferta)
    if compania is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o compañia no encontrada"})
    
    offer.companias.append(compania)
    db.commit()
    return {"status": "ok", "message": "Oferta aplicada a compañia exitosamente"}


@router.delete("/{compania_id}/ofertas/{id_oferta}")
def delete_oferta_compania(compania_id: int, id_oferta: int, db: Session = Depends(get_bd)):
    compania = db.get(CompaniaModel, compania_id)
    offer = db.get(OfertaModel, id_oferta)

    if compania is None or offer is None: 
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta o compañia no encontrada"})

    if offer not in compania.ofertas:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Oferta no aplicada a compañia"})

    compania.ofertas.remove(offer)
    db.commit()
    return {"status": "ok", "message": "Oferta eliminada de compañia exitosamente"}
