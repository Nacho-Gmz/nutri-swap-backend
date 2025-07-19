from fastapi import FastAPI
from app.routers import auth, intercambios, usuarios, alimentos

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Especificar origenes
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Autenticacion"])
app.include_router(usuarios.router, tags=["Usuarios"])
app.include_router(alimentos.router, tags=["Alimentos"])
app.include_router(intercambios.router, tags=["Intercambios"])


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de NutriSwap"}
