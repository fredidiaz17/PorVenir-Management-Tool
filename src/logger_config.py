# Creando el archivo para los logging

import logging

# Configurar logger

logging.basicConfig(
    level=logging.INFO,                                # Nivel de logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),           # Guardar logs en archivo
        logging.StreamHandler()                     # También los muestra en consola
    ]
)

logger = logging.getLogger(__name__)