# Backend FastAPI

## Generar entorno virtual e instalar dependencias

```SML
python -m venv venv

(Linux / MacOS)
source venv/bin/activate

(Windows)
venv\Scripts\activate

pip install -r requirements.txt
```

## Configurar .env con credenciales de la Base de Datos (PostgreSQL)

```SML
DB_HOST=localhost
DB_PORT=5432
DB_USER={usuario}
DB_PASSWORD={contraseña}
DB_NAME={nombre de base de datos}
```

## Ejecutar migraciones

```bash
alembic upgrade head
```

## Levantar servicio

```SML
(Linux / MacOS)
source venv/bin/activate

(Windows)
venv\Scripts\activate

uvicorn app.main:app --reload
```

## Utilidades

[Secret Key Generator](https://jwtsecret.com/generate)

[Instalación PostgreSQL](https://www.postgresql.org/download/)
