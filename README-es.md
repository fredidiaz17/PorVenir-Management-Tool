This is the README version for Spanish speakers. 

If you're looking for the English one, use the next link:
[Readme.md](README.md)


---
# 📘 Sistema de gestión para tienda de barrio (PorvenirMGT) - Backend

**Proyecto:** Sistema de gestión para tienda de barrio (PorvenirMGT)<br>
**Autor:** Fredi Díaz<br>
**Fecha de inicio:** 06/10/2025

---

## 1. Descripción general del sistema

El sistema permitirá gestionar las ventas, pedidos y productos de una tienda de barrio.
El objetivo es optimizar el control de inventario, el seguimiento de deudas y la relación con preventistas y proveedores.

---

## 2. Objetivos del sistema

* Facilitar el registro y consulta de productos.
* Controlar el stock y movimientos de inventario.
* Registrar ventas y deudas de clientes.
* Administrar pedidos realizados a preventistas.
* Gestionar la información de marcas y compañías proveedoras.

---

## 3. Arquitectura del proyecto - Enfoque Backend.
El proyecto constará de 2 partes: Un [Front]() <!-- TODO: definir, asi sea brevemente el front + agregar enlace del repositorio de git -->y un Backend desplegado a modo de API, creado con FastAPI + SQLAlchemy.

### Estructura de Archivos. 

<!-- TODO: Hacer esto una vez definida los archivos + directorios. -->

### Diseño de la Base de Datos.

Para saber mas sobre el diseño de la Base de Datos, use el siguiente [enlace](docs/es-Español/BD_INFO.md)

---

## 4. Tecnologías usadas.

* Python: Lenguaje de programación. Util por...
* FastAPI: Framework de Python usado para la creación de APIs REST
* MySQL: Base de datos relacional. Pendiente migración a PostgreSQL.

---

## 5. Como instalar o replicar.

Por hacer

### Replicar el repositorio GitHub.



---

## 6. Documentación anexa.

* Imagen del **DER** (versión actual).
* Historial de versiones del diseño.
* Notas adicionales de implementación.

## 7. Pendientes Version 1.0 (17/07/2026)
* Implementar el resto de Routers/Endpoints [X].
* Cambiar la estructura de la API a una estructura por Dominio (Ejemplo: src/v1/routers/venta.py -> src/v1/ventas/routers/venta.py)
* Migrar la BD de MySQL a PostgreSQL (Se puede usar MySQL de forma nativa con SQLAlchemy, pero el objetivo es usar PostgreSQL).
* Evaluar la BD actual antes de migrar (definir nullables, comportamiento de Foreign Keys, etc).
* Implementar un ORM de SQLAlchemy.
* Crear el front de la aplicación.
* Desplegar el Backend a la web.
* Desplegar el Front a la web.
* Implementar body request y body response con Pydantic.
* Hacer que el backend sea mas eficiente con async/await.
* Cambiar el create_All de la inicialización de la bd (main.py) por Alembic.