from contextlib import closing
from pathlib import Path
import sqlite3
import hashlib
import secrets
import re


RUTA_BD = Path(__file__).resolve().parent / "data" / "fotored.sqlite3"


def inicializar_bd():
    RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS publicaciones (
                    id INTEGER PRIMARY KEY,
                    usuario TEXT NOT NULL,
                    imagen BLOB NOT NULL,
                    descripcion TEXT NOT NULL
                )
                """
            )
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE,
                    contrasena_hash TEXT NOT NULL
                )
                """
            )


def registrar_usuario(nombre, contrasena):
    nombre = nombre.strip().lower()
    if not re.fullmatch(r"[a-z0-9_]{3,30}", nombre):
        raise ValueError("El usuario debe tener entre 3 y 30 letras sin acentos, números o guiones bajos.")
    if not 8 <= len(contrasena) <= 20 or not contrasena.strip():
        raise ValueError("La contraseña debe tener entre 8 y 20 caracteres y no ser solo espacios.")

    sal = secrets.token_bytes(16)
    iteraciones = 600_000
    resumen = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, iteraciones)
    hash_guardado = f"pbkdf2_sha256${iteraciones}${sal.hex()}${resumen.hex()}"
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        with conexion:
            cursor = conexion.execute(
                "INSERT INTO usuarios (nombre, contrasena_hash) VALUES (?, ?) ON CONFLICT(nombre) DO NOTHING",
                (nombre, hash_guardado),
            )
            return cursor.rowcount == 1


def guardar_publicacion(usuario, imagen, descripcion):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        with conexion:
            conexion.execute(
                "INSERT INTO publicaciones (usuario, imagen, descripcion) VALUES (?, ?, ?)",
                (usuario, imagen, descripcion),
            )


def obtener_publicaciones():
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        filas = conexion.execute(
            "SELECT usuario, imagen, descripcion FROM publicaciones ORDER BY id DESC"
        ).fetchall()
        return [dict(fila) for fila in filas]
