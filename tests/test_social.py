from contextlib import closing
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
import sys
import unittest

from PIL import Image
from streamlit.testing.v1 import AppTest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class SocialTest(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.ruta_original = database.RUTA_BD
        database.RUTA_BD = Path(self.temporal.name) / "social.sqlite3"
        database.inicializar_bd()
        database.registrar_usuario("ana", "Abcd1234")
        database.registrar_usuario("luis", "Abcd5678")
        self.ana = database.autenticar_usuario("ana", "Abcd1234")["id"]
        self.luis = database.autenticar_usuario("luis", "Abcd5678")["id"]
        foto = BytesIO()
        Image.new("RGB", (12, 12), "blue").save(foto, format="PNG")
        database.guardar_publicacion(self.ana, foto.getvalue(), "Foto de Ana")
        self.post = database.obtener_publicaciones()[0]["id"]

    def tearDown(self):
        database.RUTA_BD = self.ruta_original
        self.temporal.cleanup()

    def test_likes_por_cuenta_y_persistencia(self):
        database.establecer_like(self.ana, self.post, True)
        database.establecer_like(self.ana, self.post, True)
        database.establecer_like(self.luis, self.post, True)
        database.inicializar_bd()
        self.assertEqual(database.obtener_interacciones(self.post)["likes"], 2)
        database.establecer_like(self.luis, self.post, False)
        self.assertTrue(database.obtener_interacciones(self.post, self.ana)["like_propio"])
        self.assertFalse(database.obtener_interacciones(self.post, self.luis)["like_propio"])
        self.assertEqual(database.obtener_interacciones(self.post)["likes"], 1)

    def test_comentarios_validacion_y_autor(self):
        for texto in ("", " \n ", "x" * 501):
            with self.assertRaises(ValueError):
                database.agregar_comentario(self.luis, self.post, texto)
        database.agregar_comentario(self.luis, self.post, "  ¡Qué foto! ' 📷  ")
        database.agregar_comentario(self.ana, self.post, "x" * 500)
        comentarios = database.obtener_interacciones(self.post)["comentarios"]
        self.assertEqual(comentarios[0], {"usuario": "luis", "texto": "¡Qué foto! ' 📷"})
        self.assertEqual(len(comentarios), 2)

    def test_seguimiento_sin_duplicados_ni_autoseguir(self):
        for _ in range(2):
            database.establecer_seguimiento(self.luis, self.ana, True)
        self.assertEqual(database.obtener_seguimiento(self.ana, self.luis),
                         {"seguidores": 1, "seguidos": 0, "siguiendo": True})
        self.assertEqual(database.obtener_seguimiento(self.luis)["seguidos"], 1)
        with self.assertRaises(ValueError):
            database.establecer_seguimiento(self.ana, self.ana, True)
        with self.assertRaises(ValueError):
            database.establecer_seguimiento(None, self.ana, True)
        database.establecer_seguimiento(self.luis, self.ana, False)
        self.assertEqual(database.obtener_seguimiento(self.ana)["seguidores"], 0)

    def test_rechazo_invitado_y_contenido_antiguo(self):
        with closing(sqlite3.connect(database.RUTA_BD)) as con, con:
            antiguo = con.execute(
                "INSERT INTO publicaciones (usuario, imagen, descripcion) VALUES ('ejemplo', ?, '')",
                (b"imagen",),
            ).lastrowid
        for usuario, post in [(None, self.post), (-1, self.post), (self.ana, antiguo), (self.ana, -1)]:
            with self.assertRaises(ValueError):
                database.establecer_like(usuario, post, True)
            with self.assertRaises(ValueError):
                database.agregar_comentario(usuario, post, "texto")

    def test_flujo_interacciones_ui(self):
        app = AppTest.from_file(APP).run()
        self.assertTrue(app.button(key=f"like_{self.post}").disabled)
        app.text_input(key="login_usuario").input("luis")
        app.text_input(key="login_clave").input("Abcd5678")
        next(b for b in app.button if b.label == "Entrar").click().run()
        app.button(key=f"like_{self.post}").click().run()
        self.assertEqual(app.button(key=f"like_{self.post}").label, "Quitar Me gusta")
        comentario = next(t for t in app.text_area if t.label == "Escribe un comentario")
        comentario.input("Comentario de Luis")
        next(b for b in app.button if b.label == "Comentar").click().run()
        self.assertFalse(app.exception)
        self.assertIn("@luis: Comentario de Luis", [t.value for t in app.text])
        app.button(key=f"autor_{self.post}").click().run()
        app.button(key=f"seguir_{self.ana}").click().run()
        self.assertEqual(app.button(key=f"seguir_{self.ana}").label, "Dejar de seguir")
        app.button(key=f"seguir_{self.ana}").click().run()
        app.button(key=f"like_{self.post}").click().run()
        self.assertEqual(database.obtener_interacciones(self.post)["likes"], 0)
        self.assertFalse(app.exception)
        invitado = AppTest.from_file(APP).run()
        self.assertIn("@luis: Comentario de Luis", [t.value for t in invitado.text])


if __name__ == "__main__":
    unittest.main()
