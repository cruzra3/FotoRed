from contextlib import closing
from pathlib import Path
import sqlite3


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
