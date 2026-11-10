import streamlit as st


st.set_page_config(page_title="FotoRed", page_icon="📷", layout="centered")

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

st.info("Prototipo de aprendizaje: todavía no permite publicar fotografías ni crear cuentas.")

st.header("Previsualizar una fotografía")
st.caption("Selecciona un JPG o PNG. Solo se mostrará una vista previa; no se guardará ni publicará.")

foto = st.file_uploader("Selecciona una fotografía", type=["jpg", "jpeg", "png"])

if foto is not None:
    try:
        st.image(foto, caption="Vista previa de tu fotografía", width="stretch")
    except (OSError, ValueError):
        st.error("No se pudo leer la imagen. Selecciona un archivo JPG o PNG válido.")

st.header("Publicaciones de ejemplo")
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

for publicacion in publicaciones:
    with st.container(border=True):
        st.subheader(f"@{publicacion['usuario']}")
        st.image(publicacion["imagen"], width="stretch")
        st.write(publicacion["descripcion"])
