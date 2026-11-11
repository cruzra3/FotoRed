import streamlit as st
import sqlite3

from database import inicializar_bd, guardar_publicacion, obtener_publicaciones, registrar_usuario, autenticar_usuario, obtener_perfil, actualizar_perfil, buscar_usuarios
from database import establecer_like, agregar_comentario, obtener_interacciones
from database import establecer_seguimiento, obtener_seguimiento
from database import obtener_feed_seguidos


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

def abrir_perfil(usuario_id):
    st.session_state.perfil_visitado = usuario_id


def mostrar_publicaciones(publicaciones):
    for publicacion in publicaciones:
        with st.container(border=True):
            st.subheader(f"@{publicacion['usuario']}")
            if publicacion.get("usuario_id") is None:
                st.caption("Contenido de ejemplo · sin cuenta asociada")
            else:
                st.button(
                    "Ver perfil", key=f"autor_{publicacion['id']}",
                    on_click=abrir_perfil, args=(publicacion["usuario_id"],),
                )
            st.image(publicacion["imagen"], width="stretch")
            if publicacion["descripcion"]:
                st.text(publicacion["descripcion"])
            if publicacion.get("usuario_id") is None:
                continue
            cuenta = st.session_state.usuario_actual
            publicacion_id = publicacion["id"]
            try:
                social = obtener_interacciones(publicacion_id, cuenta["id"] if cuenta else None)
            except sqlite3.Error:
                st.error("No se pudieron cargar las interacciones.")
                continue
            st.caption(f"{social['likes']} Me gusta · {len(social['comentarios'])} comentarios")
            etiqueta = "Quitar Me gusta" if social["like_propio"] else "Me gusta"
            if st.button(etiqueta, key=f"like_{publicacion_id}", disabled=cuenta is None):
                try:
                    establecer_like(cuenta["id"], publicacion_id, not social["like_propio"])
                except (ValueError, sqlite3.Error):
                    st.error("No se pudo actualizar el Me gusta. Comprueba tu sesión.")
                else:
                    st.rerun()
            with st.expander("Comentarios"):
                for comentario in social["comentarios"]:
                    st.text(f"@{comentario['usuario']}: {comentario['texto']}")
                if cuenta is None:
                    st.caption("Inicia sesión para dar Me gusta o comentar.")
                else:
                    with st.form(f"comentario_{publicacion_id}_{cuenta['id']}", clear_on_submit=True):
                        texto_comentario = st.text_area("Escribe un comentario", max_chars=500)
                        comentar = st.form_submit_button("Comentar")
                    if comentar:
                        try:
                            agregar_comentario(cuenta["id"], publicacion_id, texto_comentario)
                        except ValueError as error:
                            st.error(str(error))
                        except sqlite3.Error:
                            st.error("No se pudo guardar el comentario.")
                        else:
                            st.rerun()


with st.sidebar:
    if st.session_state.usuario_actual is not None:
        st.header("Tu cuenta")
        st.subheader(f"@{st.session_state.usuario_actual['nombre']}")
        st.button("Mi perfil", key="mi_perfil", on_click=abrir_perfil,
                  args=(st.session_state.usuario_actual["id"],))
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

    st.divider()
    st.header("Navegación")
    opciones_feed = ["General", "Siguiendo"] if st.session_state.usuario_actual else ["General"]
    st.radio("Feed", opciones_feed, key="tipo_feed", on_change=abrir_perfil, args=(None,))
    st.header("Buscar usuarios")
    busqueda = st.text_input("Usuario o nombre", key="buscar_usuario")
    if busqueda.strip():
        try:
            resultados = buscar_usuarios(busqueda)
        except sqlite3.Error:
            st.error("No se pudo realizar la búsqueda.")
        else:
            if not resultados:
                st.info("No se encontraron usuarios.")
            for resultado in resultados:
                etiqueta = resultado["nombre_visible"] or resultado["nombre"]
                st.button(f"{etiqueta} (@{resultado['nombre']})",
                          key=f"resultado_{resultado['id']}",
                          on_click=abrir_perfil, args=(resultado["id"],))
    st.button("Volver al feed", key="volver_feed", on_click=abrir_perfil, args=(None,))

st.title("📷 FotoRed")
st.subheader("Un espacio para compartir tus fotografías")

st.info("Prototipo local: inicia sesión para publicar con tu cuenta. El feed es visible para todos.")

perfil_visitado = st.session_state.get("perfil_visitado")
if perfil_visitado is not None:
    try:
        perfil = obtener_perfil(perfil_visitado)
        publicaciones_perfil = obtener_publicaciones(perfil_visitado)
    except sqlite3.Error:
        st.error("No se pudo cargar el perfil.")
        st.stop()
    if perfil is None:
        st.warning("Este usuario ya no existe.")
        st.stop()
    st.header(f"Perfil de @{perfil['nombre']}")
    st.text(perfil["nombre_visible"] or perfil["nombre"])
    st.text(perfil["biografia"] or "Sin biografía todavía.")
    cuenta = st.session_state.usuario_actual
    try:
        seguimiento = obtener_seguimiento(perfil["id"], cuenta["id"] if cuenta else None)
    except sqlite3.Error:
        st.error("No se pudieron cargar los seguidores.")
    else:
        st.caption(f"{seguimiento['seguidores']} seguidores · {seguimiento['seguidos']} seguidos")
        if cuenta is None or cuenta["id"] != perfil["id"]:
            etiqueta = "Dejar de seguir" if seguimiento["siguiendo"] else "Seguir"
            if st.button(etiqueta, key=f"seguir_{perfil['id']}", disabled=cuenta is None):
                try:
                    establecer_seguimiento(cuenta["id"], perfil["id"], not seguimiento["siguiendo"])
                except (ValueError, sqlite3.Error):
                    st.error("No se pudo actualizar el seguimiento. Comprueba tu sesión.")
                else:
                    st.rerun()
    if cuenta is not None and cuenta["id"] == perfil["id"]:
        with st.expander("Editar mi perfil"):
            with st.form(f"editar_perfil_{cuenta['id']}"):
                nombre_visible = st.text_input(
                    "Nombre para mostrar", value=perfil["nombre_visible"], max_chars=60,
                )
                biografia = st.text_area("Biografía", value=perfil["biografia"], max_chars=150)
                guardar_perfil = st.form_submit_button("Guardar perfil")
            if guardar_perfil:
                try:
                    # El destino siempre es la cuenta de sesión, nunca el perfil visitado.
                    actualizar_perfil(cuenta["id"], nombre_visible, biografia)
                except ValueError as error:
                    st.error(str(error))
                except sqlite3.Error:
                    st.error("No se pudo guardar el perfil.")
                else:
                    st.session_state.aviso_perfil = "Perfil actualizado."
                    st.rerun()
        if "aviso_perfil" in st.session_state:
            st.success(st.session_state.pop("aviso_perfil"))
    st.subheader("Publicaciones de este usuario")
    if not publicaciones_perfil:
        st.info("Este usuario todavía no tiene publicaciones.")
    mostrar_publicaciones(publicaciones_perfil)
    st.stop()

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
solo_seguidos = st.session_state.get("tipo_feed") == "Siguiendo" and cuenta_actual is not None
if solo_seguidos:
    st.caption("Publicaciones de las cuentas que sigues, de más reciente a más antigua.")
else:
    st.caption("Todas las publicaciones guardadas, de más reciente a más antigua.")

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
    publicaciones_guardadas = (
        obtener_feed_seguidos(cuenta_actual["id"]) if solo_seguidos else obtener_publicaciones()
    )
except sqlite3.Error:
    st.error("No se pudieron leer las publicaciones guardadas.")
    st.stop()

if not publicaciones_guardadas:
    if solo_seguidos:
        st.info("Todavía no hay publicaciones de usuarios seguidos. Busca una cuenta y pulsa Seguir en su perfil.")
    else:
        st.info("Todavía no hay publicaciones guardadas. Inicia sesión y comparte tu primera fotografía.")

mostrar_publicaciones(publicaciones_guardadas)
if not solo_seguidos:
    with st.expander("Contenido de ejemplo"):
        st.caption("Fotos de muestra de Picsum; requieren Internet y no están asociadas a cuentas.")
        mostrar_publicaciones(publicaciones)
