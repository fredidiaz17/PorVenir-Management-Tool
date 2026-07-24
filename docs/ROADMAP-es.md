* Implementar el resto de Routers/Endpoints [X].
* Cambiar la estructura de la API a una estructura por Dominio (Ejemplo: src/v1/routers/venta.py -> src/v1/ventas/routers/venta.py).
* Migrar la BD de MySQL a PostgreSQL (Se puede usar MySQL de forma nativa con SQLAlchemy, pero el objetivo es usar PostgreSQL).
* Evaluar la BD actual antes de migrar (definir nullables, comportamiento de Foreign Keys, etc).
* Implementar un ORM de SQLAlchemy.
* Crear el front de la aplicación.
* Desplegar el Backend a la web.
* Desplegar el Front a la web.
* Implementar body request y body response con Pydantic.
* Hacer que el backend sea mas eficiente con async/await.
* Cambiar el create_All de la inicialización de la bd (main.py) por Alembic.

---
## 9. Pendientes de documentación.
* Reglas de negocio.
* Documentación funcional de entidades.
* Validaciones de los CRUD.
* Casos de uso.
* Endpoints específicos de la API.
* Decisiones de diseño o arquitectura en profundidad.