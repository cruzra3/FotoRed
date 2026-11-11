from contextlib import closing
from pathlib import Path
import sqlite3
import hashlib
import secrets
import re
import hmac


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
            columnas = {fila[1] for fila in conexion.execute("PRAGMA table_info(publicaciones)")}
            if "usuario_id" not in columnas:
                conexion.execute(
                    "ALTER TABLE publicaciones ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)"
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


def autenticar_usuario(nombre, contrasena):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        fila = conexion.execute(
            "SELECT id, nombre, contrasena_hash FROM usuarios WHERE nombre = ?",
            (nombre.strip().lower(),),
        ).fetchone()
    if fila is None:
        return None
    try:
        algoritmo, iteraciones, sal, esperado = fila[2].split("$")
        if algoritmo != "pbkdf2_sha256":
            return None
        calculado = hashlib.pbkdf2_hmac(
            "sha256", contrasena.encode("utf-8"), bytes.fromhex(sal), int(iteraciones)
        ).hex()
    except (ValueError, TypeError):
        return None
    if hmac.compare_digest(calculado, esperado):
        return {"id": fila[0], "nombre": fila[1]}
    return None


def guardar_publicacion(usuario_id, imagen, descripcion):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        with conexion:
            usuario = conexion.execute(
                "SELECT nombre FROM usuarios WHERE id = ?", (usuario_id,)
            ).fetchone()
            if usuario is None:
                raise ValueError("La cuenta ya no existe. Vuelve a iniciar sesión.")
            conexion.execute(
                "INSERT INTO publicaciones (usuario, imagen, descripcion, usuario_id) VALUES (?, ?, ?, ?)",
                (usuario[0], imagen, descripcion, usuario_id),
            )


def obtener_publicaciones():
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        filas = conexion.execute(
            "SELECT id, usuario, imagen, descripcion, usuario_id FROM publicaciones ORDER BY id DESC"
        ).fetchall()
        return [dict(fila) for fila in filas]
