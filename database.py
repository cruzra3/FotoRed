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
            columnas_usuario = {fila[1] for fila in conexion.execute("PRAGMA table_info(usuarios)")}
            if "nombre_visible" not in columnas_usuario:
                conexion.execute("ALTER TABLE usuarios ADD COLUMN nombre_visible TEXT NOT NULL DEFAULT ''")
            if "biografia" not in columnas_usuario:
                conexion.execute("ALTER TABLE usuarios ADD COLUMN biografia TEXT NOT NULL DEFAULT ''")
            conexion.execute("""CREATE TABLE IF NOT EXISTS likes (
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                publicacion_id INTEGER NOT NULL REFERENCES publicaciones(id),
                PRIMARY KEY (usuario_id, publicacion_id)
            )""")
            conexion.execute("""CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                publicacion_id INTEGER NOT NULL REFERENCES publicaciones(id),
                texto TEXT NOT NULL CHECK(length(trim(texto)) BETWEEN 1 AND 500)
            )""")
            conexion.execute("""CREATE TABLE IF NOT EXISTS seguimientos (
                seguidor_id INTEGER NOT NULL REFERENCES usuarios(id),
                seguido_id INTEGER NOT NULL REFERENCES usuarios(id),
                PRIMARY KEY (seguidor_id, seguido_id),
                CHECK (seguidor_id != seguido_id)
            )""")


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


def obtener_publicaciones(usuario_id=None):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        consulta = "SELECT id, usuario, imagen, descripcion, usuario_id FROM publicaciones"
        parametros = ()
        if usuario_id is not None:
            consulta += " WHERE usuario_id = ?"
            parametros = (usuario_id,)
        filas = conexion.execute(
            consulta + " ORDER BY id DESC", parametros
        ).fetchall()
        return [dict(fila) for fila in filas]


def obtener_perfil(usuario_id):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        fila = conexion.execute(
            "SELECT id, nombre, nombre_visible, biografia FROM usuarios WHERE id = ?",
            (usuario_id,),
        ).fetchone()
        return dict(fila) if fila else None


def actualizar_perfil(usuario_actual_id, nombre_visible, biografia):
    nombre_visible = nombre_visible.strip()
    biografia = biografia.strip()
    if len(nombre_visible) > 60 or len(biografia) > 150:
        raise ValueError("El nombre permite hasta 60 caracteres y la biografía hasta 150.")
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        with conexion:
            cursor = conexion.execute(
                "UPDATE usuarios SET nombre_visible = ?, biografia = ? WHERE id = ?",
                (nombre_visible, biografia, usuario_actual_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("La cuenta ya no existe. Vuelve a iniciar sesión.")


def buscar_usuarios(texto):
    texto = texto.strip().casefold()
    if not texto:
        return []
    # Los signos % y _ se buscan literalmente, no como comodines de LIKE.
    patron = "%" + texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        conexion.create_function("casefold", 1, str.casefold)
        filas = conexion.execute(
            """SELECT id, nombre, nombre_visible, biografia FROM usuarios
               WHERE casefold(nombre) LIKE ? ESCAPE '\\'
                  OR casefold(nombre_visible) LIKE ? ESCAPE '\\'
               ORDER BY nombre""",
            (patron, patron),
        ).fetchall()
        return [dict(fila) for fila in filas]


def validar_interaccion(conexion, usuario_id, publicacion_id):
    if not conexion.execute("SELECT 1 FROM usuarios WHERE id = ?", (usuario_id,)).fetchone():
        raise ValueError("Debes iniciar sesión con una cuenta existente.")
    if not conexion.execute(
        "SELECT 1 FROM publicaciones WHERE id = ? AND usuario_id IS NOT NULL", (publicacion_id,)
    ).fetchone():
        raise ValueError("Esta publicación no admite interacciones.")


def establecer_like(usuario_id, publicacion_id, activo):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        with conexion:
            validar_interaccion(conexion, usuario_id, publicacion_id)
            if activo:
                conexion.execute(
                    "INSERT OR IGNORE INTO likes VALUES (?, ?)", (usuario_id, publicacion_id)
                )
            else:
                conexion.execute(
                    "DELETE FROM likes WHERE usuario_id = ? AND publicacion_id = ?",
                    (usuario_id, publicacion_id),
                )


def agregar_comentario(usuario_id, publicacion_id, texto):
    texto = texto.strip()
    if not 1 <= len(texto) <= 500:
        raise ValueError("El comentario debe tener entre 1 y 500 caracteres.")
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        with conexion:
            validar_interaccion(conexion, usuario_id, publicacion_id)
            conexion.execute(
                "INSERT INTO comentarios (usuario_id, publicacion_id, texto) VALUES (?, ?, ?)",
                (usuario_id, publicacion_id, texto),
            )


def obtener_interacciones(publicacion_id, usuario_id=None):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.row_factory = sqlite3.Row
        total = conexion.execute(
            "SELECT COUNT(*) FROM likes WHERE publicacion_id = ?", (publicacion_id,)
        ).fetchone()[0]
        propio = conexion.execute(
            "SELECT 1 FROM likes WHERE publicacion_id = ? AND usuario_id = ?",
            (publicacion_id, usuario_id),
        ).fetchone() is not None
        comentarios = conexion.execute(
            """SELECT u.nombre AS usuario, c.texto FROM comentarios c
               JOIN usuarios u ON u.id = c.usuario_id
               WHERE c.publicacion_id = ? ORDER BY c.id""", (publicacion_id,)
        ).fetchall()
        return {"likes": total, "like_propio": propio,
                "comentarios": [dict(fila) for fila in comentarios]}


def establecer_seguimiento(seguidor_id, seguido_id, activo):
    if seguidor_id == seguido_id:
        raise ValueError("No puedes seguirte a ti mismo.")
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        with conexion:
            for usuario_id in (seguidor_id, seguido_id):
                if not conexion.execute("SELECT 1 FROM usuarios WHERE id = ?", (usuario_id,)).fetchone():
                    raise ValueError("Debes usar cuentas existentes para seguir usuarios.")
            if activo:
                conexion.execute("INSERT OR IGNORE INTO seguimientos VALUES (?, ?)",
                                 (seguidor_id, seguido_id))
            else:
                conexion.execute("DELETE FROM seguimientos WHERE seguidor_id = ? AND seguido_id = ?",
                                 (seguidor_id, seguido_id))


def obtener_seguimiento(perfil_id, usuario_actual_id=None):
    with closing(sqlite3.connect(RUTA_BD)) as conexion:
        seguidores = conexion.execute(
            "SELECT COUNT(*) FROM seguimientos WHERE seguido_id = ?", (perfil_id,)
        ).fetchone()[0]
        seguidos = conexion.execute(
            "SELECT COUNT(*) FROM seguimientos WHERE seguidor_id = ?", (perfil_id,)
        ).fetchone()[0]
        siguiendo = conexion.execute(
            "SELECT 1 FROM seguimientos WHERE seguidor_id = ? AND seguido_id = ?",
            (usuario_actual_id, perfil_id),
        ).fetchone() is not None
        return {"seguidores": seguidores, "seguidos": seguidos, "siguiendo": siguiendo}
