from fastapi import FastAPI
from app.routers import usuarios, alimentos

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Especificar origenes
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(alimentos.router, prefix="/alimentos", tags=["Alimentos"])

@app.get("/")
def root():
    return {"message": "Welcome to the nutri-swap API"}
