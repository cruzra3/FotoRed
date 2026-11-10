import streamlit as st


st.set_page_config(page_title="FotoRed", page_icon="📷", layout="centered")

if "publicaciones_sesion" not in st.session_state:
    st.session_state.publicaciones_sesion = []

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

st.title("📷 FotoRed")
st.subheader("Un espacio para compartir tus fotografías")
st.write("¡Bienvenido a FotoRed! Estamos construyendo esta aplicación paso a paso.")

st.info("Prototipo de aprendizaje: las publicaciones solo duran durante la sesión. No hay cuentas reales.")

st.header("Previsualizar una fotografía")
st.caption("Selecciona un JPG o PNG y pulsa Publicar para añadirlo al feed de esta sesión.")

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
        st.session_state.publicaciones_sesion.insert(
            0,
            {
                "usuario": perfil["usuario"],
                "imagen": datos_foto,
                "descripcion": descripcion.strip(),
            },
        )
        st.success("Fotografía publicada durante esta sesión.")
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

for publicacion in st.session_state.publicaciones_sesion + publicaciones:
    with st.container(border=True):
        st.subheader(f"@{publicacion['usuario']}")
        st.image(publicacion["imagen"], width="stretch")
        if publicacion["descripcion"]:
            st.text(publicacion["descripcion"])
