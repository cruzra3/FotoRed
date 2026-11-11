import sqlite3
import sys
import unittest
from contextlib import closing
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image
from streamlit.testing.v1 import AppTest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class SesionesTest(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.ruta_original = database.RUTA_BD
        database.RUTA_BD = Path(self.temporal.name) / "prueba.sqlite3"
        database.inicializar_bd()
        database.registrar_usuario("ana", "Abcd1234")
        database.registrar_usuario("luis", "Abcd5678")

    def tearDown(self):
        database.RUTA_BD = self.ruta_original
        self.temporal.cleanup()

    def test_credenciales(self):
        self.assertEqual(database.autenticar_usuario(" ANA ", "Abcd1234")["nombre"], "ana")
        self.assertIsNone(database.autenticar_usuario("ana", "incorrecta"))
        self.assertIsNone(database.autenticar_usuario("ausente", "Abcd1234"))
        self.assertIsNone(database.autenticar_usuario("' OR 1=1 --", "Abcd1234"))

    def test_migracion_conserva_autoria_antigua(self):
        ruta = Path(self.temporal.name) / "antigua.sqlite3"
        with closing(sqlite3.connect(ruta)) as conexion, conexion:
            conexion.execute("CREATE TABLE publicaciones (id INTEGER PRIMARY KEY, usuario TEXT NOT NULL, imagen BLOB NOT NULL, descripcion TEXT NOT NULL)")
            conexion.execute("INSERT INTO publicaciones VALUES (1, 'ana_fotos', ?, 'anterior')", (b"imagen",))
        with patch.object(database, "RUTA_BD", ruta):
            database.inicializar_bd()
            database.inicializar_bd()
            filas = database.obtener_publicaciones()
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["usuario"], "ana_fotos")
        self.assertIsNone(filas[0]["usuario_id"])

    def test_publicacion_requiere_cuenta_existente(self):
        with self.assertRaises(ValueError):
            database.guardar_publicacion(None, b"imagen", "texto")
        self.assertEqual(database.obtener_publicaciones(), [])

    def test_alternar_registro_y_login(self):
        app = AppTest.from_file(APP).run()
        self.assertEqual(len(app.text_input), 3)  # Acceso y búsqueda.
        next(b for b in app.button if b.label == "Registrarte").click().run()
        self.assertFalse(any(b.label == "Entrar" for b in app.button))
        app.text_input(key="registro_usuario").input("nueva")
        app.text_input(key="registro_clave").input("corta")
        next(b for b in app.button if b.label == "Crear cuenta").click().run()
        self.assertTrue(app.sidebar.error)
        self.assertEqual(app.text_input(key="registro_usuario").value, "nueva")
        app.text_input(key="registro_clave").input("Abcd1234")
        next(b for b in app.button if b.label == "Crear cuenta").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.sidebar.success)
        self.assertEqual(app.session_state.vista_acceso, "login")
        self.assertIsNone(app.session_state.usuario_actual)
        self.assertNotIn("registro_clave", app.session_state)
        self.entrar(app, "nueva", "Abcd1234")
        self.assertEqual(app.session_state.usuario_actual["nombre"], "nueva")
        self.assertEqual([t.key for t in app.text_input], ["buscar_usuario"])
        self.assertNotIn("login_clave", app.session_state)

    def entrar(self, app, usuario, clave):
        app.text_input(key="login_usuario").input(usuario)
        app.text_input(key="login_clave").input(clave)
        next(b for b in app.button if b.label == "Entrar").click().run()
        self.assertFalse(app.exception)

    def test_perfiles_busqueda_y_limites(self):
        ana = database.autenticar_usuario("ana", "Abcd1234")
        luis = database.autenticar_usuario("luis", "Abcd5678")
        database.actualizar_perfil(ana["id"], "Ángela Rivera", "Mi biografía")
        database.inicializar_bd()
        self.assertEqual(database.obtener_perfil(ana["id"])["biografia"], "Mi biografía")
        self.assertEqual(database.obtener_perfil(luis["id"])["biografia"], "")
        self.assertEqual(database.buscar_usuarios("ÁNGELA")[0]["id"], ana["id"])
        self.assertEqual(database.buscar_usuarios("AN")[0]["nombre"], "ana")
        for texto in ("", "ausente", "%", "_", "' OR 1=1 --"):
            self.assertEqual(database.buscar_usuarios(texto), [])
        for nombre, bio in [("x" * 61, ""), ("", "x" * 151)]:
            with self.assertRaises(ValueError):
                database.actualizar_perfil(ana["id"], nombre, bio)
        database.actualizar_perfil(ana["id"], "x" * 60, "y" * 150)
        self.assertIsNone(database.obtener_perfil(-1))

    def test_navegacion_y_edicion_propia(self):
        app = AppTest.from_file(APP).run()
        self.entrar(app, "ana", "Abcd1234")
        app.button(key="mi_perfil").click().run()
        self.assertFalse(app.exception)
        next(t for t in app.text_input if t.label == "Nombre para mostrar").input("Ana Rivera")
        app.text_area[0].input("Fotografía y naturaleza")
        next(b for b in app.button if b.label == "Guardar perfil").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.success)
        self.assertIn("Ana Rivera", [t.value for t in app.text])
        app.text_input(key="buscar_usuario").input("luis").run()
        next(b for b in app.button if b.label.endswith("(@luis)")).click().run()
        self.assertFalse(app.exception)
        self.assertFalse(any(b.label == "Guardar perfil" for b in app.button))
        self.assertTrue(any("todavía no tiene" in i.value for i in app.info))
        app.button(key="volver_feed").click().run()
        self.assertTrue(any(b.label == "Publicar" for b in app.button))
        app.text_input(key="buscar_usuario").input("sin_resultados").run()
        self.assertTrue(any("No se encontraron" in i.value for i in app.info))

    def test_publicaciones_filtradas_por_id(self):
        ana = database.autenticar_usuario("ana", "Abcd1234")
        luis = database.autenticar_usuario("luis", "Abcd5678")
        foto = BytesIO()
        Image.new("RGB", (12, 12), "blue").save(foto, format="PNG")
        database.guardar_publicacion(ana["id"], foto.getvalue(), "Solo Ana")
        database.guardar_publicacion(luis["id"], foto.getvalue(), "Solo Luis")
        self.assertEqual(len(database.obtener_publicaciones(ana["id"])), 1)
        app = AppTest.from_file(APP).run()
        app.text_input(key="buscar_usuario").input("ana").run()
        next(b for b in app.button if b.label.endswith("(@ana)")).click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("image")), 1)
        self.assertIn("Solo Ana", [t.value for t in app.text])
        self.assertNotIn("Solo Luis", [t.value for t in app.text])
        self.assertFalse(any(b.label == "Guardar perfil" for b in app.button))

    def test_flujo_dos_cuentas_y_logout(self):
        foto = BytesIO()
        Image.new("RGB", (12, 12), "blue").save(foto, format="PNG")
        with patch("streamlit.file_uploader", return_value=foto):
            app = AppTest.from_file(APP).run()
            self.assertTrue(next(b for b in app.button if b.label == "Publicar").disabled)
            self.entrar(app, "ana", "incorrecta")
            self.assertIsNone(app.session_state.usuario_actual)
            self.assertTrue(app.sidebar.error)
            self.entrar(app, "ana", "Abcd1234")
            app.text_area[0].input("Foto de Ana").run()
            next(b for b in app.button if b.label == "Publicar").click().run()
            self.assertEqual(database.obtener_publicaciones()[0]["usuario"], "ana")
            app.button(key="salir").click().run()
            self.assertIsNone(app.session_state.usuario_actual)
            self.assertEqual(app.text_area[0].value, "")
            self.assertTrue(next(b for b in app.button if b.label == "Publicar").disabled)
            self.entrar(app, "luis", "Abcd5678")
            next(b for b in app.button if b.label == "Publicar").click().run()
            self.assertFalse(app.exception)
        filas = database.obtener_publicaciones()
        self.assertEqual([f["usuario"] for f in filas], ["luis", "ana"])
        self.assertNotEqual(filas[0]["usuario_id"], filas[1]["usuario_id"])
        nuevo = AppTest.from_file(APP).run()
        self.assertIsNone(nuevo.session_state.usuario_actual)
        self.assertEqual(len(nuevo.get("image")), 5)


if __name__ == "__main__":
    unittest.main()
