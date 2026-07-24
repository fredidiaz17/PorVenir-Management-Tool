> 🌐 [Read this in English](README.md)

---
# 📘 Sistema de gestión para tienda de barrio (PorvenirMGT) - Backend

## Estado del proyecto.

> 🟡 En progreso

**Versión**: 1.0

---

## 1. Descripción general del sistema

### ¿De qué trata?

Este proyecto es una API REST construida con **FastAPI** y **SQLAlchemy**, diseñada para gestionar las operaciones de una tienda de barrio. Permite llevar control sobre inventario, ventas, ofertas, pedidos, deudas y relaciones con proveedores.

### ¿Qué problema resuelve?

*   Optimiza el control de inventario.
*   Centraliza el registro de ventas y el seguimiento de deudas.
*   Facilita la administración de pedidos a preventistas.
*   Ofrece herramientas para gestionar la información de marcas y compañías proveedoras.

### ¿Quién consume esta API?

Por ahora, esta API está pensada para ser consumida por la aplicación web del sistema (Por crear). Sin embargo, está diseñada para ser escalable y poder ser consumida por otras aplicaciones en el futuro.

---

## 2. Caracteristicas principales.

* Gestión de productos.
* Gestión de ventas.
* Gestión de pedidos.
* Control de inventario.
* Administración de ofertas.
* Gestión de clientes y deudas.

---

## 3. Arquitectura.

### Arquitectura general.

El proyecto está construido bajo una arquitectura de **API RESTful** utilizando **FastAPI** como framework principal web por su alto rendimiento. 

- **ORM y Base de datos**: Utiliza **SQLAlchemy** para interactuar con una base de datos MySQL (con **PyMySQL** como driver).

- **Validación de Datos**: Toda la validación de entrada y serialización de salida está manejada por **Pydantic**.

- **Servidor ASGI**: Utiliza **Uvicorn** para la ejecución asíncrona de la aplicación.

### Flujo de la aplicación.

El flujo típico de una petición en el sistema es el siguiente:

1. **Petición del Cliente**: Un cliente hace una petición HTTP a uno de los endpoints de la API.

2. **Enrutamiento (Routers)**: La petición llega a `main.py` y es delegada al router correspondiente dentro de `src/v1/routers/`.

3. **Validación (Schemas)**: Los datos entrantes se validan automáticamente contra los esquemas de **Pydantic** (`src/v1/schemas/`). Si los datos son inválidos, se devuelve un error 422 automáticamente.

4. **Capa de Datos (Models / Database)**: El router se comunica con la base de datos utilizando la sesión definida en `src/database/` y realiza consultas a través de los modelos de **SQLAlchemy** (`src/models/`).

5. **Respuesta**: Se devuelve una respuesta en formato JSON al cliente, donde los datos de salida vuelven a ser validados por Pydantic antes de ser enviados.


### Organización del proyecto.

El código fuente está modularizado siguiendo principios de separación de responsabilidades:

- Todo el código de la aplicación se encuentra en la carpeta `src/`.

- La API está versionada (carpeta `v1/`) para facilitar la escalabilidad y futuras modificaciones sin romper clientes existentes.

- Existe una clara separación entre los modelos de la base de datos (ORM) y los esquemas de validación de datos (Pydantic), lo que permite mayor flexibilidad y seguridad al no exponer estructuras internas de la BD directamente.

### Estructura de carpetas.

```text
Backend-PorvenirMGT/
├── .env                # Variables de entorno (conexión BD, claves, etc.)
├── docs/               # Documentación adicional y archivos SQL
├── requirements.txt    # Listado de dependencias del proyecto
├── src/                # Código fuente principal de la aplicación
│   ├── database/       # Archivos de conexión y configuración de BD
│   ├── models/         # Modelos de SQLAlchemy (Tablas de base de datos)
│   ├── v1/             # Versión 1 de la API
│   │   ├── routers/    # Endpoints de la API divididos por entidad
│   │   └── schemas/    # Esquemas Pydantic (Validación de entrada y salida)
│   ├── api_v1.py       # Agrupador de los routers de la v1
│   └── main.py         # Punto de entrada principal para ejecutar FastAPI
└── tests/              # Pruebas automatizadas del código (Pytest)
```
---

## 4. Base de datos.

La documentación completa del modelo de datos se encuentra en:

* [Diagrama Entidad-Relación]()
* [Modelo lógico](docs/Modelo_Logico.txt)
* [Información de la Base de Datos](docs/es-Español/BD_INFO.md)

---

## 5. Tecnologías.

* **Lenguaje base**: Python
* **Framework principal**: FastAPI.
* **Base de datos**: MySQL. Pendiente migrar a PostgreSQL.
* **Herramientas de arquitectura**: SQLAlchemy (ORM), Pydantic (Validaciones).
* **Herramientas de testing**: Pytest.

---

## 6. Instalación.

### Requisitos

- **Python 3.8+** (Recomendado 3.10 o superior).

- **MySQL Server** instalado y ejecutándose.

- **Git** para clonar el repositorio.

### Creación del entorno virtual

Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto.
En la raíz del proyecto, ejecuta:

```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```
### Instalación de dependencias

Con el entorno virtual activado, instala todas las librerías necesarias con `pip`:

```bash
pip install -r requirements.txt
```

### Variables de entorno

El proyecto utiliza variables de entorno para manejar información sensible como credenciales de la base de datos. Crea un archivo llamado `.env` en la raíz del proyecto con la siguiente estructura:

```env
DB_HOST=localhost
DB_USER=tu_usuario_local
DB_PASSWORD=tu_contraseña
DB_PORT=3306
DB_NAME=nombre_base_datos
```

> **Nota**: *Recuerda reemplazar `tu_usuario_local`, `tu_contraseña`, y `nombre_base_datos` con tus credenciales reales de tu servidor MySQL local*.

### Creación de la base de datos

1. Inicia sesión en tu servidor MySQL.

2. Crea la base de datos (por ejemplo, `tienda`).

3. Puedes apoyarte en el archivo `docs/schema.sql` para poblar la estructura inicial, aunque SQLAlchemy se encargará de crear las tablas automáticamente al iniciar la app si están correctamente mapeadas en los modelos.

### Ejecución del servidor

Para iniciar el servidor en modo desarrollo (con recarga automática de cambios), ejecuta el siguiente comando con **Uvicorn** desde la raíz del proyecto:

```bash
uvicorn src.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000` y su documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

---

## 7. Documentación.

enlaces a documentación mencionada hasta el momento:

|Documento | Contenido |
|----------|-----------|
| [BD_INFO.md](docs/es-Español/BD_INFO.md) | Modelo de datos |
| (Por crear) | Reglas de negocio |
| [Schema.sql](docs/schema.sql) | Archivo DDL para la creación de la base de datos |
| (Por crear) | Diagrama Entidad-Relación |
| [Modelo_Logico.txt](docs/Modelo_Logico.txt) | Modelo lógico |
| [README.md](README.md) | Versión en inglés de este documento |


---

## 8. Roadmap.

Las funcionalidades planeadas a ser implementadas en el futuro se pueden consultar [aquí](docs/ROADMAP-es.md).


---

## Licencia.

Este proyecto está bajo la **Licencia MIT**; consulta el archivo [LICENSE](LICENSE) para más detalles.