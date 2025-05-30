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

## Agregar un usuario a base de datos 

Manualmente desde un administrador de la base de datos crear una fila nueva en la tabla de usuarios:
La contraseña está hasheada y es "admin123".

```sql 
Juan, Perez, email@email.com, $2b$12$uZCGwLNDZxH4HfDxAnbaPe8L4B0TSJ3NhRqbrhnGj3wsSIGf/gZgC, true
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
