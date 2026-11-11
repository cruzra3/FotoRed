import sqlite3
import sys
import unittest
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
        with sqlite3.connect(ruta) as conexion:
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
        self.assertEqual(len(app.text_input), 2)
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
        self.assertFalse(app.text_input)
        self.assertNotIn("login_clave", app.session_state)

    def entrar(self, app, usuario, clave):
        app.text_input(key="login_usuario").input(usuario)
        app.text_input(key="login_clave").input(clave)
        next(b for b in app.button if b.label == "Entrar").click().run()
        self.assertFalse(app.exception)

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
