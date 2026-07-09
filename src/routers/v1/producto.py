from fastapi import APIRouter
from src.database.db_conn import engine 
from sqlalchemy import text
from src.schemas.productos import Producto

router = APIRouter()

@router.get("/")
def get_productos():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM producto"))
        result = [dict(row) for row in result.mappings().fetchall()]
    return {"status": "ok", "data": result} 

@router.get("/{id_producto}")
def get_producto(id_producto: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM producto WHERE id_producto = :id_producto"), {"id_producto": id_producto})
        result =  result.mappings().fetchone()
    return {"status": "ok", "data": result} 

@router.post("/")
def create_producto(producto: Producto):
    try:
        product_data = producto.model_dump()
        with engine.begin() as conn:
            data = {
                "nombre": product_data.get("nombre"),
                "stock": product_data.get("stock"),
                "unidad_medida": product_data.get("unidad_medida"),
                "precio_compra": product_data.get("precio_compra"),
                "precio_venta": product_data.get("precio_venta"),
                "iva": product_data.get("iva"),
                "id_marca": product_data.get("id_marca")
            }
            conn.execute(text("""
            INSERT INTO producto (nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca) 
            VALUES (:nombre, :stock, :unidad_medida, :precio_compra, :precio_venta, :iva, :id_marca)"""), 
            data)
        return {"status": "ok", "message": "Producto creado exitosamente"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.put("/{id_producto}")
def update_producto(id_producto: int, producto: Producto):
    try:
        product_data = producto.model_dump()
        with engine.begin() as conn:
            data = {
                "nombre": product_data.get("nombre"),
                "stock": product_data.get("stock"),
                "unidad_medida": product_data.get("unidad_medida"),
                "precio_compra": product_data.get("precio_compra"),
                "precio_venta": product_data.get("precio_venta"),
                "iva": product_data.get("iva"),
                "id_marca": product_data.get("id_marca"),
                "id_producto": id_producto
            }
            conn.execute(text("""
            UPDATE producto SET nombre = :nombre, cantidad_stock = :stock, unidad_medida=:unidad_medida, precio_compra = :precio_compra, precio_venta = :precio_venta, porcentaje_iva = :iva, id_marca = :id_marca 
            WHERE id_producto = :id_producto"""), data)
            return {"status": "ok", "message": "Producto actualizado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.delete("/{id_producto}")
def delete_producto(id_producto: int):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM producto WHERE id_producto = :id_producto"), {"id_producto": id_producto})
            return {"status": "ok", "message": "Producto eliminado exitosamente"} 
    except Exception as e:
        return {"status": "error", "message": str(e)} 


