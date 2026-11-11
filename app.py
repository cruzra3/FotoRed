import streamlit as st
import sqlite3

from database import inicializar_bd, guardar_publicacion, obtener_publicaciones, registrar_usuario


st.set_page_config(page_title="FotoRed", page_icon="📷", layout="centered")

try:
    inicializar_bd()
except (sqlite3.Error, OSError):
    st.error("No se pudo abrir la base de datos local. Comprueba los permisos de la carpeta data.")
    st.stop()

perfil = {
    "nombre": "Ana Rivera",
    "usuario": "ana_fotos",
    "biografia": "Me gusta explorar la naturaleza y compartir lo que descubro con mi cámara.",
}

with st.sidebar:
    st.header("Perfil de ejemplo")
    st.subheader(perfil["nombre"])
    st.write(f"@{perfil['usuario']}")
    st.write(perfil["biografia"])
    st.caption("Datos ficticios para este prototipo. No hay una sesión iniciada.")

    st.header("Registro de usuarios")
    st.caption("Crear una cuenta todavía no inicia sesión ni cambia el autor de las publicaciones.")
    with st.form("registro", clear_on_submit=True):
        nombre_registro = st.text_input("Nombre de usuario", max_chars=30)
        contrasena_registro = st.text_input(
            "Contraseña", type="password", max_chars=20,
            help="Entre 8 y 20 caracteres.",
        )
        registrar = st.form_submit_button("Crear cuenta")
    if registrar:
        try:
            creado = registrar_usuario(nombre_registro, contrasena_registro)
        except ValueError as error:
            st.error(str(error))
        except sqlite3.Error:
            st.error("No se pudo guardar la cuenta. Inténtalo de nuevo.")
        else:
            if creado:
                st.success("Cuenta creada. El inicio de sesión estará disponible en un próximo paso.")
            else:
                st.warning("Ese nombre de usuario ya está registrado.")

st.title("📷 FotoRed")
st.subheader("Un espacio para compartir tus fotografías")
st.write("¡Bienvenido a FotoRed! Estamos construyendo esta aplicación paso a paso.")

st.info("Prototipo de aprendizaje: publicaciones y registros guardados localmente. El inicio de sesión aún no está disponible.")

st.header("Previsualizar una fotografía")
st.caption("Selecciona un JPG o PNG y pulsa Publicar para guardarlo y añadirlo al feed.")

foto = st.file_uploader("Selecciona una fotografía", type=["jpg", "jpeg", "png"])
descripcion = st.text_area(
    "Descripción de la fotografía (opcional)",
    placeholder="Ejemplo: Una tarde explorando la naturaleza.",
)

imagen_valida = False
if foto is not None:
    try:
        datos_foto = foto.getvalue()
        st.image(datos_foto, caption="Vista previa de tu fotografía", width="stretch")
        imagen_valida = True
        if descripcion.strip():
            st.text(descripcion)
    except (OSError, ValueError):
        st.error("No se pudo leer la imagen. Selecciona un archivo JPG o PNG válido.")

if st.button("Publicar"):
    if imagen_valida:
        try:
            guardar_publicacion(perfil["usuario"], datos_foto, descripcion.strip())
        except sqlite3.Error:
            st.error("No se pudo guardar la publicación. No se confirmó el guardado.")
        else:
            st.success("Fotografía guardada en la base de datos local.")
    else:
        st.warning("Selecciona una fotografía válida antes de publicar.")

st.header("Feed de publicaciones")
st.caption("Usuarios ficticios y fotos de muestra de Picsum. Las imágenes requieren Internet.")

publicaciones = [
    {
        "usuario": "ana_fotos",
        "imagen": "https://picsum.photos/id/10/800/500",
        "descripcion": "Un momento para disfrutar de la naturaleza.",
    },
    {
        "usuario": "marcos_explora",
        "imagen": "https://picsum.photos/id/29/800/500",
        "descripcion": "Siempre hay un lugar nuevo por descubrir.",
    },
    {
        "usuario": "lucia_creativa",
        "imagen": "https://picsum.photos/id/15/800/500",
        "descripcion": "Una pausa para mirar lo que nos rodea.",
    },
]

try:
    publicaciones_guardadas = obtener_publicaciones()
except sqlite3.Error:
    st.error("No se pudieron leer las publicaciones guardadas.")
    st.stop()

for publicacion in publicaciones_guardadas + publicaciones:
    with st.container(border=True):
        st.subheader(f"@{publicacion['usuario']}")
        st.image(publicacion["imagen"], width="stretch")
        if publicacion["descripcion"]:
            st.text(publicacion["descripcion"])
