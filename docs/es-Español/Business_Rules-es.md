# Índice
1. [Introducción](#1-introducción)
2. [Reglas generales](#2-reglas-generales)
3. [Reglas por entidad](#3-reglas-por-entidad)
4. [Reglas transversales](#4-reglas-transversales)
5. [Casos especiales](#5-casos-especiales)
6. [Futuras reglas](#6-futuras-reglas)

---

## 1. Introducción

Este documento describe las reglas funcionales que rigen el comportamiento del sistema. Estas reglas representan la lógica del negocio y son independientes de la tecnología utilizada para implementarlas.

---

## 2. Reglas generales

Reglas que aplican a todo el sistema.

Ejemplos:

* Todos los precios se almacenan en moneda local.

### Por pensar.
* Los registros eliminados físicamente deben evitarse cuando exista información histórica relacionada.
* Las fechas se registran en la zona horaria configurada por el sistema.
* Las operaciones críticas deben quedar registradas.

---



## 3. Reglas por entidad

### Compañía 

Entidad que representa a la empresa proveedora de productos. Puede tener varias [marcas](#marca) y [preventistas](#preventista) a su servicio.

#### Reglas
* El nombre debe ser único

>***Nota para la versión en español:** Dado a que los motores de bases de datos y otras tecnologias suelen tener problemas con el manejo de la "Ñ", la entidad **"Compañía"** se ha escrito como **"Compania"** en el código, aunque en el presente documento puede variar entre usar o no la ñ.*

---

### Marca         
Representa un conjunto de productos que pertenecen a una misma marca.
Pertenece a una sola [compania](#compania) y puede tener varios [productos](#producto) asociados.

#### Reglas
* El nombre debe ser único.
* La descripción puede ser opcional.
* Debe pertenecer a una **Compania**

---
### Producto

Representa un producto físico que es solicitado a un proveedor y vendido en la tienda. Pertenece a una sola [marca](#marca) y puede tener varias [etiquetas](#etiqueta) asociadas.

#### Reglas 
* El nombre debe ser único.
* El stock nunca puede ser negativo.
* Un producto con stock en cero no puede venderse.
* La unidad de medida es obligatoria, pero por defecto se le asigna **Unidades**.
* El precio de compra es obligatorio.
* El precio de venta es obligatorio, pero por defecto es 10% mayor al precio de compra.
* El porcentaje de IVA es opcional, pero no puede ser negativo.
* Debe pertenecer a una **marca**

---

### Preventista  

Una persona que trabaja para una empresa (**Compañia**) y que se dedica a vender los productos de la empresa a la que pertence.

#### Reglas
* El nombre es obligatorio.
* El telefono es opcional.
* Debe pertenecer a una **Compania**

---

### Pedido 

Solicitud que se realiza al [preventista](#preventista) para la compra de productos. A nivel fisico, seria equivalente a una Factura o una nota de remisión.


#### Reglas

* La fecha del pedido por defecto es la fecha actual, pero puede ser modificada.
* El estado inicial del pedido es **Pendiente**.

> El estado del pedido puede ser:
>* Pendiente por hacer: Registrado en el sistema, pero aun no se le ha hecho el pedido al preventista.
>* En camino: Se le ha hecho el pedido al preventista.
>* Recibido: El pedido llegó exitosamente a la tienda.
>* Rechazado: El pedido ha sido rechazado por el tendero (usuario).
>* No entregado: El pedido nunca llegó a la tienda. 

* El subtotal es la suma del total de cada linea (Productos) antes de impuestos.
* impuestos es opcional es opcional, pero no puede ser negativo.
* El total se calcula automaticamente como la suma del subtotal y los impuestos.
* Debe pertenecer a un **Preventista**

### Detalle Pedido

Representa una linea de [producto](#producto) dentro de un [pedido](#pedido). 

#### Reglas
* Debe estar asociado a un **pedido**
* Debe estar asociado a un **producto**
* cantidad no puede ser negativa.
* El precio unitario por defecto es el **precio de compra** del producto, pero puede ser modificado.
* El subtotal es el resultado de multiplicar la cantidad por el precio unitario, se calcula automaticamente.
* porcentaje de iva es opcional, pero no puede ser negativo.
* El valor del iva es el resultado de aplicar el porcentaje de iva al subtotal (Ej: 100 * 0.12 = 12).
* El total de la linea se calcula automaticamente como la suma entre el subtotal y el valor del iva.

---

### Etiqueta 

Es una forma de categorizar uno o varios [productos](#producto).

#### Reglas
* El nombre debe ser único.
* La descripción puede ser opcional.
* El color debe ser un código hexadecimal válido. Por defecto, el codigo será blanco ( #ffffff o #FFFFFF)

---

### Oferta

Es un evento temporal que afecta a los productos, ya sea por medio de descuentos, regalando productos u otra acción promocional. Se puede aplicar directamente a los [productos](#producto) o indirectamente, aplicandose a una o varias [marcas](#marca), a una o varias [etiquetas](#etiqueta) o a una o varias [compañías](#compañia). 

#### Reglas
* El nombre debe ser único.
* La descripción puede ser opcional.
* El tipo de oferta puede ser **Descuento** o **Combo**.
* El valor del descuento puede ser opcional, pero no puede ser negativo.
> **Valor descuento** es porcentaje
* Cantidad minima puede ser opcional, pero no puede ser negativa.
> Es la cantidad minima para activar la respectiva oferta.
* Producto regalo es opcional, pero debe referenciar un producto.
> **Valor descuento**, **cantidad minima** y **producto regalo** son opcionales para permitir flexibilidad a la hora de crear ofertas.
* La fecha de inicio debe ser menor o igual a la fecha de fin.
* La fecha de fin debe ser mayor o igual a la fecha actual.
* La misma oferta no puede tener efecto 2 veces en el mismo producto (Ej: Oferta 1 es aplicada directamente a Producto A y a Marca X, pero Producto A pertenece a Marca X, la oferta solo vale una vez).

---

### Cliente 

Persona que compra productos en la tienda.

#### Reglas
* El nombre es obligatorio.
* El telefono es opcional.

--- 

### Venta

Registra una transacción comercial entre la tienda y un cliente. Permite manejar diferentes formas de pago y generar [deudas](#deuda) si es necesario.

#### Reglas
* Inicialmente, la fecha de la venta corresponde a la fecha actual, pero puede ser modificada.
* El medio de pago es obligatorio, pero por defecto será **Efectivo**. El cliente puede elegir entre **Efectivo, Digital, Mixto o Fiado**.
> Si se elige **Fiado**, se creará o se actualizará una [deuda](#deuda). <br>
>***Sugerencia para el usuario**: Si el cliente no puede pagar todo, se escoge **Fiado** para que se genere una deuda a su nombre y restarle a esa deuda el monto pagado.*
* El total se calcula automaticamente como la suma del total de cada linea de [detalle venta](#detalle_venta).
* Debe estar asociado a un [cliente](#cliente)


### Detalle venta

Representa una linea de [producto](#producto) dentro de una [venta](#venta).

#### Reglas
* Debe estar asociado a una [venta](#venta).
* Debe estar asociado a un [producto](#producto).
* La cantidad no puede ser negativa.
* El precio de venta por defecto es el **precio de venta** del producto, pero puede ser modificado.
* El descuento manual es opcional, pero no puede ser negativo.
* El subtotal es el resultado de multiplicar la cantidad por el precio de venta menos el descuento manual, se calcula automaticamente.

---

### Deuda

Es el registro de un monto que un cliente debe a la tienda. Se genera cuando la [venta](#venta) se realiza mediante pago **fiado**.

#### Reglas
* Solo se genera si el cliente no paga el valor completo.
* El saldo pendiente nunca puede ser negativo.
* Una deuda pagada (monto 0 ) cambia automáticamente de estado.
* Una deuda debe estar asociada a un [cliente](#cliente).   

---

## 4. Reglas transversales

Reglas que involucran varias entidades.

Ejemplos:

* Registrar una venta disminuye el stock.
* Cancelar un pedido no modifica el inventario.
* Una oferta vencida deja de aplicarse automáticamente.

---

## 5. Casos especiales

Aquí documentas excepciones.

Ejemplo:

* ¿Qué pasa si un producto no tiene marca?
* ¿Qué ocurre si una oferta aplica tanto por marca como por etiqueta?
* ¿Qué sucede si un cliente tiene varias deudas?

---

## 6. Futuras reglas

No implementadas aún, pero previstas.

* Bloquear ventas cuando el stock sea insuficiente.
* Aplicar promociones acumulables.

---

## Un detalle que considero importante

En vez de escribir párrafos largos, escribiría las reglas como especificaciones numeradas.

Por ejemplo:

```text
VR-001. El stock de un producto no puede ser negativo.

VR-002. Una venta debe contener al menos un producto.

VR-003. Una deuda solo puede generarse cuando el pago recibido sea inferior al total de la venta.
```

Tiene varias ventajas:

* puedes referenciar reglas fácilmente ("ver VR-015");
* facilita el mantenimiento;
* da una apariencia muy profesional, similar a documentos de análisis funcional.

