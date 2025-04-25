from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr
import psycopg2
import bcrypt
from psycopg2.extras import RealDictCursor
from typing import List, Optional

app = FastAPI()

# Configuración de la conexión
DB_CONFIG = {
    'dbname': 'alimentos',
    'user': 'postgres',
    'password': '1234567',
    'host': 'localhost',
    'port': 5432
}

# Conexión a la base de datos


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Error conectando a la base de datos:", e)
        return None

# Modelo Pydantic para la creación y actualización de alimentos


class Alimento(BaseModel):
    Alimento: str
    Categoria: str
    Cantidad: float
    Unidad: str
    Peso_bruto: float
    Peso_neto: float
    Energia: float
    Proteinas: float
    Lipidos: float
    Carbohidratos: float


class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    correo: EmailStr


class UsuarioCreate(UsuarioBase):
    contrasenia: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# Endpoint para obtener todos los alimentos


@app.get("/nombrealimentos", response_model=List[dict])
async def get_all_nombrealimentos():
    """Obtiene todos los alimentos."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT "Alimento" FROM public."Datos_alimentos";""")
            alimentos = cursor.fetchall()
            return alimentos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Endpoint para obtener todos los alimentos


@app.get("/alimentos", response_model=List[dict])
async def get_all_alimentos():
    """Obtiene todos los alimentos."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""SELECT * FROM public."Datos_alimentos";""")
            alimentos = cursor.fetchall()
            return alimentos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Endpoint para obtener alimentos por categoría


@app.get("/alimentos/categoria/{nombre}", response_model=List[dict])
async def get_categoria_by_nombre(nombre: str):
    """Obtiene todos los alimentos de una misma categoría dando el nombre de un alimento."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """SELECT * FROM public."Datos_alimentos" WHERE "Categoria" = (SELECT "Categoria" FROM public."Datos_alimentos" WHERE "Alimento" = %s) AND "Alimento" != %s;"""
            cursor.execute(query, (nombre, nombre))
            alimentos = cursor.fetchall()
            if alimentos:
                return alimentos
            else:
                raise HTTPException(
                    status_code=404, detail="No se encontraron alimentos dentro de la misma categoría")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Endpoint para obtener un alimento por su ID


@app.get("/alimentos/{id}", response_model=dict)
async def get_alimento_by_id(id: int):
    """Obtiene un alimento por su ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT * FROM public."Datos_alimentos" WHERE id = %s;""", (id,))
            alimento = cursor.fetchone()
            if alimento:
                return alimento
            else:
                raise HTTPException(
                    status_code=404, detail="Alimento no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Endpoint para obtener datos de un alimento por su nombre


@app.get("/alimentos/{nombre}", response_model=dict)
async def get_info_alimento_by_nombre(nombre: str):
    """Obtiene datos de un alimento por su nombre."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT * FROM public."Datos_alimentos" WHERE "Alimento" = %s;""", (nombre,))
            alimento = cursor.fetchone()
            if alimento:
                return alimento
            else:
                raise HTTPException(
                    status_code=404, detail="Alimento no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

# Endpoint para crear un nuevo alimento


@app.post("/alimentos", status_code=201)
async def create_alimento(alimento: Alimento):
    """Crea un nuevo alimento."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO public."Datos_alimentos" ("Alimento", "Categoria", "Cantidad", "Unidad", "Peso_bruto", "Peso_neto", "Energia", "Proteinas", "Lipidos", "Carbohidratos")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """
            cursor.execute(query, (
                alimento.Alimento, alimento.Categoria, alimento.Cantidad, alimento.Unidad,
                alimento.Peso_bruto, alimento.Peso_neto, alimento.Energia,
                alimento.Proteinas, alimento.Lipidos, alimento.Carbohidratos
            ))
            conn.commit()
            new_id = cursor.fetchone()[0]
            return {"message": "Alimento creado", "id": new_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Endpoint para actualizar un alimento


@app.put("/alimentos/{id}")
async def update_alimento(id: int, alimento: Alimento):
    """Actualiza un alimento existente."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            UPDATE public."Datos_alimentos"
            SET "Alimento" = %s, "Categoria" = %s, "Cantidad" = %s, "Unidad" = %s, 
                "Peso_bruto" = %s, "Peso_neto" = %s, "Energia" = %s, 
                "Proteinas" = %s, "Lipidos" = %s, "Carbohidratos" = %s
            WHERE id = %s;
            """
            cursor.execute(query, (
                alimento.Alimento, alimento.Categoria, alimento.Cantidad, alimento.Unidad,
                alimento.Peso_bruto, alimento.Peso_neto, alimento.Energia,
                alimento.Proteinas, alimento.Lipidos, alimento.Carbohidratos, id
            ))
            conn.commit()
            if cursor.rowcount > 0:
                return {"message": "Alimento actualizado"}
            else:
                raise HTTPException(
                    status_code=404, detail="Alimento no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

# Para eliminar un alimento
@app.delete("/alimentos/{id}")
async def delete_alimento(id: int):
    """Elimina un alimento."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """DELETE FROM public."Datos_alimentos" WHERE id = %s;"""
            cursor.execute(query, (id,))
            conn.commit()
            if cursor.rowcount > 0:
                return {"message": "Alimento eliminado"}
            else:
                raise HTTPException(
                    status_code=404, detail="Alimento no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

            """USUARIOS"""
# Función para hashear la contraseña


def hash_contrasenia(contrasenia: str) -> str:
    return bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Función para verificar la contraseña


def verificar_contrasenia(hashed_contrasenia: str, contrasenia: str) -> bool:
    return bcrypt.checkpw(contrasenia.encode('utf-8'), hashed_contrasenia.encode('utf-8'))

# Crear un nuevo usuario


@app.post("/usuarios", response_model=Usuario)
async def crear_usuario(usuario: UsuarioCreate):
    """Crea un nuevo usuario."""
    conn = connect_to_db()
    if conn:
        try:
            hashed_contrasenia = hash_contrasenia(usuario.contrasenia)
            cursor = conn.cursor()
            query = """
            INSERT INTO usuarios (nombre, apellidos, correo, contrasenia)
            VALUES (%s, %s, %s, %s) RETURNING id;
            """
            cursor.execute(query, (usuario.nombre, usuario.apellidos,
                           usuario.correo, hashed_contrasenia))
            conn.commit()
            new_id = cursor.fetchone()[0]
            return Usuario(id=new_id, nombre=usuario.nombre, apellidos=usuario.apellidos, correo=usuario.correo)
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Obtener todos los usuarios


@app.get("/usuarios", response_model=List[Usuario])
async def obtener_usuarios():
    """Obtiene todos los usuarios."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT id, nombre, apellidos, correo FROM usuarios;")
            usuarios = cursor.fetchall()
            return [Usuario(**usuario) for usuario in usuarios]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Obtener hash de contrasenia de un usuario


@app.get("/usuariocontra/{usuario_id}")
async def obtener_contra_usuario(usuario_id: int):
    """Obtiene todos los usuarios."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT contrasenia FROM usuarios WHERE id = %s;", (usuario_id,))
            contra = cursor.fetchall()
            return [contra]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Obtener un usuario por ID
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def obtener_usuario(usuario_id: int):
    """Obtiene un usuario por su ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT id, nombre, apellidos, correo FROM usuarios WHERE id = %s;", (usuario_id,))
            usuario = cursor.fetchone()
            if usuario:
                return Usuario(**usuario)
            else:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Actualizar un usuario
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
async def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate):
    """Actualiza un usuario existente."""
    conn = connect_to_db()
    if conn:
        try:
            hashed_contrasenia = hash_contrasenia(usuario.contrasenia)
            cursor = conn.cursor()
            query = """
            UPDATE usuarios
            SET nombre = %s, apellidos = %s, correo = %s, contrasenia = %s
            WHERE id = %s RETURNING id;
            """
            cursor.execute(query, (usuario.nombre, usuario.apellidos,
                           usuario.correo, hashed_contrasenia, usuario_id))
            conn.commit()
            if cursor.rowcount > 0:
                return Usuario(id=usuario_id, nombre=usuario.nombre, apellidos=usuario.apellidos, correo=usuario.correo)
            else:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")

# Eliminar un usuario


@app.delete("/usuarios/{usuario_id}", response_model=Usuario)
async def eliminar_usuario(usuario_id: int):
    """Elimina un usuario por su ID."""
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellidos, correo FROM usuarios WHERE id = %s;", (usuario_id,))
            usuario = cursor.fetchone()
            if usuario:
                cursor.execute(
                    "DELETE FROM usuarios WHERE id = %s;", (usuario_id,))
                conn.commit()
                return Usuario(**usuario)
            else:
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    else:
        raise HTTPException(
            status_code=500, detail="No se pudo conectar a la base de datos")
