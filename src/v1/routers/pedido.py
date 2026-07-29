
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from src.database.db_conn import get_bd

from src.v1.schemas.pedido import Pedido, PedidoPatch
from src.v1.schemas.enums import EstadoPedido

from src.models.pedido import PedidoModel
from src.models.detalle_pedido import DetallePedidoModel
from src.models.producto import ProductoModel

router = APIRouter()

def update_stock(id_pedido: int, db: Session):
    stmt = db.select(DetallePedidoModel).where(DetallePedidoModel.id_pedido == id_pedido)
    query_detalle = db.execute(stmt).scalars().all()

    # Se iteran por cada detalle del pedido
    for detalle in query_detalle:
        id_producto = detalle.id_producto
        cantidad = detalle.cantidad
        
        # Se obtiene el producto
        query_producto = db.get(ProductoModel, id_producto)

        if not query_producto:
            return False

        # Se suma la cantidad del pedido al stock del producto
        query_producto.cantidad_stock += cantidad

    return True


def update_details(id_pedido: int, detalles: list[dict], db: Session, put = True):

    stmt = db.select(DetallePedidoModel).where(DetallePedidoModel.id_pedido == id_pedido)
    detalles_existentes = db.execute(stmt).scalars().all()

    if not detalles_existentes:
        return False

    # Creamos un set de tuplas (id_pedido, id_producto) de los detalles que existen en la base de datos
    existentes_ids = {
        (d.id_pedido, d.id_producto) for d in detalles_existentes
    }

    detalles_ids = set()
    try:
        for detalle in detalles:
            # Se obtiene el id del producto
            id_prod = detalle.get("id_producto", None)
            
            # Si los IDs de detalle (id pedido e id producto) están en detalles existentes, se actualiza.
            if (id_pedido, id_prod) in existentes_ids:
                query_detalle = db.get(DetallePedidoModel, (id_pedido, id_prod))
                for key, value in detalle.items():
                    setattr(query_detalle, key, value)
                
            else:
                # No está, por lo que se debe crear un nuevo detalle
                detalle["id_pedido"] = id_pedido 
                new_detalle = DetallePedidoModel(**detalle)
                db.add(new_detalle)

            # Se crea un set de tuplas de los detalles enviados simultaneamente
            detalles_ids.add((id_pedido, id_prod))
    except Exception as e:
        return False
    
    # Solo se ejecuta si es PUT, no patch
    if put:
        # Si el ID de existentes no se encuentra en detalles, se elimina
        for id_tuple in existentes_ids:
            if id_tuple not in detalles_ids:
                db.delete(db.get(DetallePedidoModel, id_tuple))

    return True


# --- READ --- 

# Retornar todos los pedidos. Seria como la "vista previa". Sin detalles del pedido
@router.get("/")
def get_pedidos(db: Session = Depends(get_bd)):
    stmt = select(PedidoModel)
    result = db.execute(stmt).scalars().all()
    return {"status": "ok", "data": result} 


# Retorna un pedido en concreto, y por ende tambien sus detalles
@router.get("/{id_pedido}")
def get_pedido(id_pedido: int, db: Session = Depends(get_bd)):
    
    # Stmt para buscar el pedido junto con sus detalles. Con esto evitamos hacer otro "select"
    stmt = (
        select(PedidoModel)
        .where(PedidoModel.id_pedido == id_pedido)
        .options(selectinload(PedidoModel.detalles)) # Asegurarse que la relación se llama "detalles" en el modelo de pedido
    )
    result = db.execute(stmt).scalar_one_or_none()
    if result is None: 
        return {"status": "error", "message": "Pedido no encontrado"}
    
    return {"status": "ok", "data": result} 



# --- CREATE ---

# Pedido y detalles_pedido van de la mano: Si no se puede crear uno, tampoco el otro.
@router.post("/")
def create_pedido(pedido: Pedido, db: Session = Depends(get_bd)):
    try:
        
        new_pedido = pedido.model_dump()
        detalles_pedido = new_pedido.pop("detalles_pedido", None)

        if detalles_pedido is None:
            return {"status": "error", "message": "El pedido no puede estar vacio"}

        # Se crea el pedido
        new_pedido = PedidoModel(**new_pedido)

        db.add(new_pedido)
        db.flush()

        # Se necesita el id del pedido para enlazar los detalles 
        id_pedido = new_pedido.id_pedido

        for detalle in detalles_pedido:
            detalle["id_pedido"] = id_pedido
            new_detalle = DetallePedidoModel(**detalle)
            db.add(new_detalle)
            db.flush()


        db.commit()
        return {"status": "ok", "message": "Pedido creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 


# --- UPDATE ---

# Se puede actualizar todo el pedido, incluyendo sus detalles.
# La actualización de detalles implica crear nuevos detalles, cambiar los existentes o eliminarlos.
# En resumen: Reemplaza los detalles antiguos por unos nuevos. 

@router.put("/{id_pedido}")
def update_pedido(id_pedido: int, pedido: Pedido, db: Session = Depends(get_bd)):
    try:
        query_pedido = db.get(PedidoModel, id_pedido)
        if not query_pedido:
            return {"status": "error", "message": "Pedido no encontrado"} 
        
        pedido_dict = pedido.model_dump()
        detalles_pedido = pedido_dict.pop("detalles_pedido", None)

        if detalles_pedido is None:
            return {"status": "error", "message": "El pedido a actualizar no puede estar vacío"}
        
        try:
            for key, value in pedido_dict.items():
                setattr(query_pedido, key, value)
        except Exception:
            return {"status": "error", "message": "Error al actualizar el pedido"} 
        
        
        # Si el estado cambia a "Recibido", se debe aumentar el stock
        
        if query_pedido.estado == EstadoPedido.RECIBIDO:
            updated = update_stock(id_pedido, db=db)
            if not updated:
                return {"status": "error", "message": "No se pudo actualizar el stock"} 

        # Se reemplazan los detalles (detalles_pedido)

        updated = update_details(id_pedido, detalles_pedido, db)
        if not updated:
            return {"status": "error", "message": "No se pudo actualizar los detalles"} 

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
        
        pedido_dict = pedido.model_dump()
        
        detalles = None
        if hasattr(pedido_dict, "detalles_pedido"):
            detalles = pedido_dict.pop("detalles_pedido", None)

        for key, value in pedido_dict.items():
            if value is not None:
                setattr(query_pedido, key, value)

        if query_pedido.estado == EstadoPedido.RECIBIDO:
            updated = update_stock(id_pedido=id_pedido, db=db)
            if not updated:
                return {"status": "error", "message": "No se pudo actualizar el stock"}
        
        if detalles is not None:
            updated = update_details(id_pedido=id_pedido, detalles=detalles, db=db, put = False)
            if not updated:
                return {"status": "error", "message": "No se pudo actualizar los detalles"} 

        db.commit()
        db.refresh(query_pedido)
        return {"status": "ok", "message": "Pedido actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

# --- DELETE ---
# Si no existe pedido, tampoco sus detalles. El On delete Cascade se encargara de esto.
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
