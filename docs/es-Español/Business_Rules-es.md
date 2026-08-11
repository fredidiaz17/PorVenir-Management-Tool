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

### Definición de numeración de las reglas:

Con el proposito de permitir un mejor seguimiento de las reglas a lo largo del documento y dar la posibilidad de referenciarlas en otros archivos de la documentación, las reglas seguiran una numeración unica compuesta por dos letras, guión (-) y un numero de 3 digitos, ej: **GR-001**. Las letras corresponden al tipo de regla (Regla general, por entidad, transversal, etc), el guion es un separador y los 3 digitos corresponden a un numero unico, incrementado en 1 por cada regla de su categoria.

Las categorias de reglas y sus respectivas abreviaciones son:
* **Reglas generales**: GR (General Rules)
* **Reglas por entidad**: ER (Entity Rules)
* **Reglas transversales**: TR (Transversal Rules)
* **Casos especiales**: SC (Special Cases)
* **Futuras reglas**: FR (Future Rules)

---

## 2. Reglas generales

Reglas que aplican a todo el sistema.

**GR-001**: Todos los precios se almacenan en moneda local.

**GR-002**: Las fechas se registran en horario local.

---


## 3. Reglas por entidad

### Compañía 

Entidad que representa a la empresa proveedora de productos. Puede tener varias [marcas](#marca) y [preventistas](#preventista) a su servicio.

**ER-001**: El nombre es obligatorio.

**ER-002**: El nombre debe ser único.

>***Nota para la versión en español:** Dado a que los motores de bases de datos y otras tecnologias suelen tener problemas con el manejo de la "Ñ", la entidad **"Compañía"** será escrita (o ya ha sido escrita) como **Compania** en el código, la base de datos y otros apartados relacionados, aunque en la documentación en español (como el presente archivo) puede variar entre usar o no la ñ.*

---

### Marca         
Representa un conjunto de productos que pertenecen a una misma marca.
Debe pertenecer a una [compania](#compania) y puede tener varios [productos](#producto) asociados.

**ER-003**: El nombre es obligatorio.

**ER-004**: El nombre debe ser único.

**ER-005**: La descripción es opcional.

---
### Producto

Representa un producto físico que es solicitado a un proveedor y vendido en la tienda. Pertenece a una  [marca](#marca) y puede tener varias [etiquetas](#etiqueta) asociadas.

**ER-006**: El nombre es obligatorio.

**ER-007**: El nombre debe ser único.

**ER-008**: El stock nunca puede ser negativo.

**ER-009**: Un producto con stock en cero no puede venderse.

**ER-010**: La unidad de medida es obligatoria.
* Puede ser: **Gramos**, **Kilogramos**, **Libras**, **Litros**, **Mililitros**, **Unidades**, **Docenas** y **Paquetes**.
* Si el usuario no escoge la unidad de medida, se le asignará por defecto **Unidades**.

**ER-011**: El precio de compra es obligatorio.

**ER-012**: El precio de compra no puede ser negativo.

**ER-013**: El precio de venta es obligatorio.

* Si el usuario no especifica un precio de venta, se le asignará por defecto un precio de venta equivalente al precio de compra más un 10% de margen de ganancia.

**ER-014**: El porcentaje de IVA es opcional.

**ER-015**: El porcentaje de IVA no puede ser negativo.

---

### Preventista  

Una persona que trabaja para una empresa (**Compañía**) y que se dedica a ofrecer los [productos](#producto) de la **Compañía** a la que pertence a las tiendas locales. Debe pertenecer a una [Compañia](#compania).

**ER-016**: El nombre es obligatorio.

**ER-017**: El telefono es opcional.

---

### Pedido 

Solicitud que se realiza al **preventista** para la compra de productos. A nivel fisico, seria equivalente a una Factura o una nota de remisión. Debe estar ligado a un [Preventista](#preventista)


**ER-018**: La fecha del pedido es inicialmente la fecha de su creación.

**ER-019**: La fecha puede ser modificada.

**ER-020**: El estado del pedido puede ser: **Pendiente por hacer**, **En camino**, **Recibido**, **Rechazado**, **No entregado**.

**ER-021**: El estado inicial del pedido es **Pendiente por hacer**.

**ER-022**: Un pedido puede ser modificado cuantas veces el usuario desee mientras no haya sido marcado como **Recibido**. Una vez marcado como Recibido, no se permitirá su edición.

>* **Pendiente por hacer**: Registrado en el sistema, pero aun no se le ha hecho el pedido al preventista.
>* **En camino**: Se le ha hecho el pedido al preventista.
>* **Recibido**: El pedido llegó exitosamente a la tienda.
>* **Rechazado**: El pedido ha sido rechazado por el tendero (usuario).
>* **No entregado**: El pedido nunca llegó a la tienda. 

**ER-023**: El subtotal se calcula automaticamente como la suma del total de cada linea (**Productos**) antes de impuestos.
**ER-024**: Los impuestos se calcula automaticamente como la suma del valor del IVA presente en cada linea de detalles del pedido.
**ER-025**: El total se calcula automaticamente como la suma del subtotal y los impuestos.


### Detalle Pedido

Representa una linea de **producto** dentro de un **pedido**. Debe estar asociado a un [pedido](#pedido) y a un [producto](#producto)


**ER-026**: Un detalle de pedido no puede existir sin un [pedido](#pedido).
> Un pedido representa una factura, un detalle de pedido representa una linea de ese documento, no tiene sentido que exista sin un pedido.

**ER-027**: Un detalle de pedido puede existir sin un [producto](#producto).
* Es obligatorio que el detalle de pedido esté ligado a un **producto** al momento de ser creado.
> Si un producto es eliminado, el detalle del pedido debe ser desvinculado de este para que de esta forma el pedido siga consevando sus detalles tal cual.

**ER-028**: La cantidad debe ser mayor a 0.

**ER-029**: El precio unitario por defecto es el **precio de compra** del producto, pero puede ser modificado.

**ER-030**: El subtotal se calcula automaticamente como el resultado de multiplicar la cantidad por el precio unitario.

**ER-031**: El porcentaje de IVA es opcional.

**ER-032**: El porcentaje de IVA no puede ser negativo.

**ER-033**: El valor del IVA se calcula automaticamente como el resultado de aplicar el porcentaje de IVA al subtotal (Ej: 100 * 0.12 = 12).

**ER-034**: El total de la linea se calcula automaticamente como la suma entre el subtotal y el valor del IVA.

---

### Etiqueta 

Es una forma de categorizar uno o varios [productos](#producto).

**ER-035**: El nombre es obligatorio.

**ER-036**: El nombre debe ser único.

**ER-037**: La descripción es opcional.

**ER-038**: El color es obligatorio y debe ser un código hexadecimal válido.
* Por defecto, el codigo será blanco ( #ffffff o #FFFFFF)

---

### Oferta

Es un evento temporal que afecta a los productos, ya sea por medio de descuentos, regalando productos u otra acción promocional. Se puede aplicar directamente a los [productos](#producto) o indirectamente por medio de una o varias [marcas](#marca), una o varias [etiquetas](#etiqueta) o, una o varias [compañías](#compañia). 

**ER-039**: El nombre es obligatorio.

**ER-040**: El nombre debe ser único.

**ER-041**: La descripción es opcional.

**ER-042**: El tipo de oferta es obligatorio 
* El tipo de oferta puede ser **Descuento** o **Combo**.

**ER-043**: El valor del descuento es ser opcional.

**ER-044**: El valor del descuento no puede ser negativo.

> **Valor descuento** es en porcentaje.

**ER-045**: Cantidad minima es opcional

**ER-046**: Cantidad minima no puede ser negativa.

> Es la cantidad minima para activar la respectiva oferta.

**ER-047**: Producto regalo es opcional.

**ER-048**: Producto regalo debe referenciar un producto.

> **Valor descuento**, **cantidad minima** y **producto regalo** son opcionales para permitir flexibilidad a la hora de crear ofertas.

**ER-049**: La fecha de inicio es obligatoria.

**ER-050**: La fecha de fin es obligatoria.

**ER-051**: La fecha de fin debe ser mayor o igual a la fecha de inicio.

**ER-052**: La misma oferta no puede tener efecto 2 veces en el mismo producto (Ej: Oferta 1 es aplicada directamente a Producto A y a Marca X, pero Producto A pertenece a Marca X, la oferta solo vale una vez).

---

### Cliente 

Persona que compra productos en la tienda.

**ER-053**: El nombre es obligatorio.

**ER-054**: El telefono es opcional.

--- 

### Venta

Registra una transacción comercial entre la tienda y un cliente. Permite manejar diferentes formas de pago y generar [deudas](#deuda) si es necesario.
Debe estar asociado a un [cliente](#cliente)

**ER-055**: Una venta no puede ser modificada, pues representa una transacción ya realizada. 
* Si se desea modificar una venta, se debe **anular** y crear una nueva.
> **Anular** implica eliminar la venta y sus detalles para revertir sus cambios en el inventario (stock).
> **Eliminar** la venta no afecta el stock.

**ER-056**: La fecha de venta corresponde a la fecha de registro de la venta.

* La fecha de venta puede ser modificada.

**ER-057**: El medio de pago es obligatorio.

**ER-058**: El medio de pago puede ser **Efectivo**, **Digital**, **Mixto** o **Fiado**. Elegir **Fiado** generará una [deuda](#deuda).
* Por defecto será **Efectivo**

> Si se genera una **deuda**, se creará o se actualizará una [deuda](#deuda) a nombre del [cliente](#cliente). <br>
>***Sugerencia para el usuario**: Si el cliente no puede pagar todo, se recomienda escoger **Fiado** para que se genere una deuda a su nombre y restarle a esa deuda el monto pagado.*

**ER-059**: El total se calcula automaticamente como la suma del total de cada linea de [detalle venta](#detalle_venta).



### Detalle venta

Representa una linea de **producto** dentro de una **venta**. Debe estar asociado a una [venta](#venta) y a un [producto](#producto)

**ER-060**: Un detalle de venta no puede existir sin una [venta](#venta).

> Si se elimina la venta, no tiene sentido conservar sus detalles.

**ER-061**: Un detalle de venta puede existir sin un [producto](#producto).


* Es obligatorio que el detalle de venta esté ligado a un **producto** al momento de ser creado.

> Se permite que un detalle de venta exista sin un producto (despues de que este ultimo fuera eliminado) para preservar el registro histórico de ventas en caso de que un producto sea eliminado.

**ER-062**: La cantidad debe ser mayor a 0.

**ER-063**: El precio de venta por defecto es el **precio de venta** del producto, pero puede ser modificado.

**ER-064**: El descuento manual es opcional.

**ER-065**: El descuento manual no puede ser negativo.

**ER-066**: El subtotal es calculado automaticamente como el resultado de multiplicar la cantidad por el precio de venta, posteriormente restandole el descuento manual.

**ER-067**: El subtotal no puede ser negativo.

---

### Deuda

Es el registro de un monto que un cliente debe a la tienda. Debe estar asociada a un [cliente](#cliente).

**ER-068**: Se genera cuando una [venta](#venta) se realiza mediante pago **fiado**.

**ER-069**: El saldo pendiente nunca puede ser negativo.

**ER-070**: Una deuda pagada ( tener saldo pendiente de 0 ) cambia automáticamente de estado.

**ER-071**: Un **cliente** solo puede tener una **deuda**. Cada vez que se genera una deuda (Una **venta fiada**), se le suma el monto de la venta a la deuda existente, o se crea la deuda si no existe.   

---

## 4. Reglas transversales

Reglas que involucran varias entidades.

### Por pensar.

* Registrar una venta disminuye el stock.
* Cancelar un pedido no modifica el inventario.
* Una oferta vencida deja de aplicarse automáticamente.

> Nota: *Estas reglas puede que ya existan como Reglas por Entidad, por lo que es necesario evaluar si se cambia o se mantiene*

---

## 5. Casos especiales

Casos excepcionales que requieran manejo especial.

### Por pensar

* ¿Qué pasa si un producto no tiene marca?
* ¿Qué ocurre si una oferta aplica tanto por marca como por etiqueta?
* ¿Qué sucede si un cliente tiene varias deudas?

> Nota: *Estas reglas puede que ya existan como Reglas por Entidad, por lo que es necesario evaluar si se cambia o se mantiene*

---

## 6. Futuras reglas

Reglas que no están implementadas aún, pero se tienen previstas.

* Bloquear ventas cuando el stock sea insuficiente.
* Aplicar promociones acumulables.
* Permitir al usuario eligir entre ofertas de diferente tipo

---

