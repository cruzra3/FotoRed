import streamlit as st
import sqlite3

from database import inicializar_bd, guardar_publicacion, obtener_publicaciones, registrar_usuario, autenticar_usuario


st.set_page_config(page_title="FotoRed", page_icon="📷", layout="centered")

try:
    inicializar_bd()
except (sqlite3.Error, OSError):
    st.error("No se pudo abrir la base de datos local. Comprueba los permisos de la carpeta data.")
    st.stop()

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = None

def cambiar_formulario(vista):
    for clave in ("login_usuario", "login_clave", "registro_usuario", "registro_clave"):
        st.session_state.pop(clave, None)
    st.session_state.vista_acceso = vista


if "vista_acceso" not in st.session_state:
    st.session_state.vista_acceso = "login"

with st.sidebar:
    if st.session_state.usuario_actual is not None:
        st.header("Tu cuenta")
        st.subheader(f"@{st.session_state.usuario_actual['nombre']}")
        if st.button("Cerrar sesión", key="salir"):
            st.session_state.clear()
            st.rerun()
    else:
        st.header("📷 FotoRed")
        if "aviso_registro" in st.session_state:
            st.success(st.session_state.pop("aviso_registro"))
        if st.session_state.vista_acceso == "login":
            st.subheader("Iniciar sesión")
            with st.form("login"):
                nombre_login = st.text_input("Usuario", key="login_usuario")
                clave_login = st.text_input("Contraseña", type="password", key="login_clave")
                entrar = st.form_submit_button("Entrar", type="primary", width="stretch")
            if entrar:
                try:
                    cuenta = autenticar_usuario(nombre_login, clave_login)
                except sqlite3.Error:
                    st.error("No se pudo consultar la cuenta. Inténtalo de nuevo.")
                else:
                    if cuenta is None:
                        st.error("Usuario o contraseña incorrectos.")
                    else:
                        st.session_state.usuario_actual = cuenta
                        # El próximo rerun retirará estos widgets y sus datos de la vista.
                        st.session_state.vista_acceso = "login"
                        st.rerun()
            st.write("¿No tienes una cuenta?")
            st.button("Registrarte", on_click=cambiar_formulario, args=("registro",))
        else:
            st.subheader("Crear una cuenta")
            st.caption("Regístrate para compartir tus fotografías en FotoRed.")
            with st.form("registro"):
                nombre_registro = st.text_input(
                    "Nombre de usuario", max_chars=30, key="registro_usuario",
                    help="De 3 a 30 letras sin acentos, números o guiones bajos.",
                )
                contrasena_registro = st.text_input(
                    "Contraseña", type="password", max_chars=20,
                    help="Entre 8 y 20 caracteres.", key="registro_clave",
                )
                registrar = st.form_submit_button("Crear cuenta", type="primary", width="stretch")
            if registrar:
                try:
                    creado = registrar_usuario(nombre_registro, contrasena_registro)
                except ValueError as error:
                    st.error(str(error))
                except sqlite3.Error:
                    st.error("No se pudo guardar la cuenta. Inténtalo de nuevo.")
                else:
                    if creado:
                        st.session_state.aviso_registro = "Cuenta creada. Inicia sesión para continuar."
                        st.session_state.vista_acceso = "login"
                        st.rerun()
                    else:
                        st.warning("Ese nombre de usuario ya está registrado.")
            st.write("¿Ya tienes una cuenta?")
            st.button("Iniciar sesión", on_click=cambiar_formulario, args=("login",))

st.title("📷 FotoRed")
st.subheader("Un espacio para compartir tus fotografías")
st.write("¡Bienvenido a FotoRed! Estamos construyendo esta aplicación paso a paso.")

st.info("Prototipo local: inicia sesión para publicar con tu cuenta. El feed es visible para todos.")

st.header("Previsualizar una fotografía")
st.caption("Selecciona un JPG o PNG y pulsa Publicar para guardarlo y añadirlo al feed.")

cuenta_actual = st.session_state.usuario_actual
clave_editor = cuenta_actual["id"] if cuenta_actual else "invitado"
foto = st.file_uploader(
    "Selecciona una fotografía", type=["jpg", "jpeg", "png"],
    key=f"foto_{clave_editor}",
)
descripcion = st.text_area(
    "Descripción de la fotografía (opcional)",
    placeholder="Ejemplo: Una tarde explorando la naturaleza.",
    key=f"descripcion_{clave_editor}",
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

if st.session_state.usuario_actual is None:
    st.caption("Inicia sesión para publicar. Puedes previsualizar una foto sin iniciar sesión.")

if st.button("Publicar", disabled=st.session_state.usuario_actual is None):
    if st.session_state.usuario_actual is None:
        st.warning("Debes iniciar sesión para publicar.")
    elif imagen_valida:
        try:
            guardar_publicacion(st.session_state.usuario_actual["id"], datos_foto, descripcion.strip())
        except ValueError as error:
            st.error(str(error))
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
        if publicacion.get("usuario_id") is None:
            st.caption("Contenido de ejemplo · sin cuenta asociada")
        st.image(publicacion["imagen"], width="stretch")
        if publicacion["descripcion"]:
            st.text(publicacion["descripcion"])
