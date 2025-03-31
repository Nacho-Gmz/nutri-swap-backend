# Backend FastAPI

## Generar entorno virtual e instalar dependencias

```SML
python -m venv venv

(Linux / MacOS)
source venv/bin/activate

(Windows)
venv/Scripts/Activate

pip install -r requirements.txt
```

## Levantar servicio

```SML
(Linux / MacOS)
source venv/bin/activate

(Windows)
venv\Scripts\activate

uvicorn app.main:app --reload
```
