
[Regresar al README](../../README-es.md)
---
# 📘 Estructura de la BD del proyecto PorvenirMGT

---
## ÍNDICE.
1. [Entidades principales identificadas](#1-entidades-principales-identificadas)
2. [Relaciones entre entidades](#2-relaciones-entre-entidades)
3. [Entidades asociativas](#3-entidades-asociativas)
4. [Atributos principales (Resumen general)](#4-atributos-principales-resumen-general)
5. [Reglas o decisiones de diseño](#5-reglas-o-decisiones-de-diseño)
---

## 1. Entidades principales identificadas

| Entidad           | Descripción breve                                               |
| ----------------- | --------------------------------------------------------------- |
| **Producto**      | Bien o artículo que se vende o se pide.                         |
| **Etiqueta**      | Clasificación del producto (hogar, limpieza, comestible, etc.). |
| **Marca**         | Identifica la marca del producto.                               |
| **Compañía**      | Empresa dueña de una o más marcas.                              |
| **Preventista**   | Persona que atiende a la tienda por parte de una compañía.      |
| **Pedido**        | Solicitud de compra realizada a un preventista.                 |
| **Cliente**       | Persona que compra en la tienda.                                |
| **Venta**         | Transacción de venta a un cliente.                              |
| **Deuda**         | Registro de pagos pendientes del cliente.                       |
| **Oferta**        | Promoción o descuento temporal que se aplica a uno o varios productos.         |


---

## 2. Relaciones entre entidades

### Compañía - Marca
- Una **compañía** puede tener varias **marcas** (1:N).


### Marca - Producto
- Una **marca** puede tener varios **productos** (1:N). 


### Producto - Etiqueta
- Un **producto** puede tener varias **etiquetas**, y una **etiqueta** puede aplicar a varios **productos** (N:M)

**Notas:** Esta relación presenta una entidad asociativa **ProductoEtiqueta**.
Las etiquetas inactivas mantiene su vinculo con los productos, pero no se muestran en estos.

### Oferta - Producto
- Una **oferta** puede aplicarse a uno o varios **productos**, varios **productos** pueden tener aplicadas una o varias **ofertas** (N:M)

### Oferta - Etiqueta
- Una **oferta** puede aplicarse a una o varias **etiquetas**, las **etiquetas** pueden tener una o varias **ofertas** (N:M)

### Oferta - Marca
- Una **oferta** puede aplicarse a una o varias **marcas**, las **marcas** pueden tener una o varias **etiquetas** (N:M)

### Oferta - Compañía
- Una **oferta** puede aplicarse a una o varias **compañias**, las **compañias** pueden tener una o varias **ofertas** (N:M)


### Compañía - Preventista
- Una **compañía** cuenta con varios preventistas (1:N)

### Preventista - Pedido
- Un **preventista** puede recibir uno o muchos pedidos

### Pedido - Producto
- Un **pedido** puede contener uno o varios **productos**, un **producto** puede aparecer en varios **pedidos** (N:M)
**Notas:** Esta relación tiene una entidad asociativa: **DetallePedido**.

### Cliente - Venta
- Un **cliente** puede comprar (generar **venta**) varias veces. (1:N)

### Venta - Producto
- Una **venta** puede registrar uno o varios **productos**, un **producto** puede ser **vendido** varias veces. (N:M)
**Notas:** La entidad asociativa **DetalleVenta** contempla esta relación, tienendo *cantidad*, *precio_uni* y *descuento_manual* como atributos.

### Cliente - Deuda
- Un **cliente** puede contraer una **deuda** solo si no paga el monto completo de la compra, mientras que cada **deuda** pertenece a un solo **cliente**. (0:1)

**Notas generales:** Las relaciones N:M se representarán como **entidades asociativas** siempre y cuando tengan atributos adicionales. 
De lo contrario, se interpreta que hay una tabla intermedia en la relación sin atributos adicionales.
---

## 3. Entidades asociativas:

| Entidad           | Descripción breve                                               |
| ----------------- | --------------------------------------------------------------- |
| **DetallePedido** | Asociación entre Pedido y Producto. |
| **ProductoEtiqueta** | Entidad asociativa entre Producto y Etiqueta.|
| **DetalleVenta** | Relación entre las Ventas y sus Productos.|

## 4. Atributos principales (resumen general)

**Compañía:** id_compañia, nombre <br>
**Marca:** id_marca, nombre, descripcion, id_compañia <br>
**Producto:** id_producto, nombre, cantidad_stock, unidad_medida, precio_compra, precio_venta, porcentaje_iva, id_marca. <br>
**Etiqueta:** id_etiqueta, nombre_etiqueta, descricion_etiqueta, color_hex. <br>
**ProductoEtiqueta:** id_producto, id_etiqueta, estado. <br>
**Oferta:** id_oferta, nombre, descripcion, tipo_oferta, valor_descuento, cantidad_minima, producto_regalo, fecha_inicio, fecha_fin, estado.<br>
**Preventista:** id_preventista, nombre, telefono, id_compañia <br>
**Pedido:** id_pedido, fecha_pedido, estado, subtotal, impuestos, total, id_preventista <br>
**DetallePedido:** id_pedido, id_producto, cantidad, precio_unitario,  iva_porcentaje, iva_valor, subtotal_linea, total_linea. <br>
**Cliente:** id_cliente, nombre, telefono <br>
**Venta:** id_venta, fecha, medio_pago, total, id_cliente <br>
**DetalleVenta:** id_venta, id_producto, precio_venta, cantidad, subtotal, descuento_manual. <br>
**Deuda:** id_deuda, id_cliente, saldo_pendiente, estado <br>


---

## 5. Reglas o decisiones de diseño

* Las relaciones N:M se convierten en **entidades asociativas** cuando guardan datos propios (por ejemplo, DetallePedido).
* Las relaciones 1:N permiten `NULL` cuando el registro puede ser opcional (por ejemplo, producto sin marca).
* Si el usuario no selecciona marca o compañía, el sistema mostrará “Desconocido”.
* Se aplica `ON DELETE CASCADE` y `ON UPDATE CASCADE` en claves foráneas para mantener la integridad referencial.
