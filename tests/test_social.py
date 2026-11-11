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

    def test_feed_seguidos_filtra_ordena_y_no_duplica(self):
        self.assertEqual(database.obtener_feed_seguidos(self.luis), [])
        database.registrar_usuario("tercera", "Abcd9999")
        tercera = database.autenticar_usuario("tercera", "Abcd9999")["id"]
        imagen = database.obtener_publicaciones()[0]["imagen"]
        database.guardar_publicacion(self.luis, imagen, "Propia")
        database.guardar_publicacion(tercera, imagen, "No seguida")
        database.guardar_publicacion(self.ana, imagen, "Más reciente de Ana")
        for _ in range(2):
            database.establecer_seguimiento(self.luis, self.ana, True)
        filas = database.obtener_feed_seguidos(self.luis)
        self.assertEqual([f["descripcion"] for f in filas], ["Más reciente de Ana", "Foto de Ana"])
        self.assertEqual(database.obtener_feed_seguidos(None), [])
        database.inicializar_bd()
        self.assertEqual(len(database.obtener_feed_seguidos(self.luis)), 2)
        database.establecer_seguimiento(self.luis, self.ana, False)
        self.assertEqual(database.obtener_feed_seguidos(self.luis), [])
        self.assertEqual(len(database.obtener_publicaciones()), 4)

    def test_navegacion_feed_y_persistencia_entre_sesiones(self):
        app = AppTest.from_file(APP).run()
        self.assertEqual(list(app.radio[0].options), ["General"])
        app.text_input(key="login_usuario").input("luis")
        app.text_input(key="login_clave").input("Abcd5678")
        next(b for b in app.button if b.label == "Entrar").click().run()
        app.radio[0].set_value("Siguiendo").run()
        self.assertFalse(app.get("image"))
        self.assertTrue(any("Todavía no hay publicaciones de usuarios seguidos" in i.value for i in app.info))
        app.text_input(key="buscar_usuario").input("ana").run()
        app.button(key=f"resultado_{self.ana}").click().run()
        app.button(key=f"seguir_{self.ana}").click().run()
        app.button(key="volver_feed").click().run()
        self.assertEqual(len(app.get("image")), 1)
        app.button(key=f"like_{self.post}").click().run()
        next(t for t in app.text_area if t.label == "Escribe un comentario").input("Desde Siguiendo")
        next(b for b in app.button if b.label == "Comentar").click().run()
        self.assertFalse(app.exception)
        app.button(key=f"autor_{self.post}").click().run()
        app.radio[0].set_value("General").run()
        self.assertIsNone(app.session_state.perfil_visitado)
        self.assertEqual(len(app.get("image")), 4)
        app.button(key="salir").click().run()
        self.assertEqual(list(app.radio[0].options), ["General"])
        nuevo = AppTest.from_file(APP).run()
        nuevo.text_input(key="login_usuario").input("luis")
        nuevo.text_input(key="login_clave").input("Abcd5678")
        next(b for b in nuevo.button if b.label == "Entrar").click().run()
        nuevo.radio[0].set_value("Siguiendo").run()
        self.assertEqual(nuevo.button(key=f"like_{self.post}").label, "Quitar Me gusta")
        self.assertIn("@luis: Desde Siguiendo", [t.value for t in nuevo.text])
        nuevo.button(key=f"autor_{self.post}").click().run()
        nuevo.button(key=f"seguir_{self.ana}").click().run()
        nuevo.button(key="volver_feed").click().run()
        self.assertFalse(nuevo.exception)
        self.assertFalse(nuevo.get("image"))

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
