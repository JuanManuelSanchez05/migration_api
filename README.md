# Migration API

Esta API está desarrollada en Flask y utiliza SQLAlchemy para manejar una base de datos. Permite cargar datos de archivos csv para tres tablas: **departments**, **jobs** y **hired_employees**.  
## Tener en cuenta:
El archivo **hired_employees** se procesa asignando valores por defecto en caso de campos vacíos (por ejemplo, `"sin_nombre"`, `"sin_departamento"`, `"sin_trabajo"` o una fecha por defecto).

## Estructura del proyecto

La estructura del proyecto es la siguiente:
migration_api/ ├── app/ │ ├── init.py │ ├── models.py │ └── routes.py ├── config.py └── run.py


- **config.py**  
  Configuración de la aplicación, incluyendo la URI de la base de datos (por defecto se usa SQLite).

- **run.py**  
  Punto de entrada para iniciar la API. Crea las tablas y ejecuta el servidor en modo debug.

- **app/__init__.py**  
  Inicializa la aplicación Flask, carga la configuración y crea la instancia de SQLAlchemy. Importa las rutas.

- **app/models.py**  
  Define los modelos: `Department`, `Job` y `Employee`.

- **app/routes.py**  
  Define el endpoint `/upload/<file_type>` para subir archivos CSV y procesarlos según el tipo (`departments`, `jobs` o `hired_employees`).

## Requisitos

- Python 3.10 o superior
- Flask
- Flask-SQLAlchemy
- pandas
- (Opcional) SQLite (ya que se utiliza como base de datos para desarrollo)

Puedes instalar las dependencias con:
```bash
pip install -r requirements.txt
