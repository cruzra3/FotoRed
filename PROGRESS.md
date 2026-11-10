# PROGRESS.md

## Estado actual
Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Revisión visual manual completada por
el usuario, quien confirmó que la pantalla se ve bien.
Selección y previsualización de fotografías implementadas con aprobación del usuario.
La vista previa ahora incluye una descripción opcional, sin guardar ni publicar.
El usuario confirmó que este cambio se ve bien y realizó el commit local.

## Completado
- Revisión visual de la descripción confirmada por el usuario; commit local verificado: 693376c (Añadir descripción opcional a la vista previa)
- Campo de descripción opcional con st.text_area y texto debajo de una vista previa válida
- AppTest: descripción vacía, espacios, texto con varias líneas y texto literal; sin foto y archivo inválido; sin excepciones (selector de archivo simulado)
- El usuario confirmó que la selección y vista previa se ven bien; commit local verificado: cb6080e (Añadir selección y vista previa de fotografías)
- Selector JPG/JPEG/PNG y vista previa, sin persistencia ni publicación en el feed
- Manejo de archivos cuyo contenido no es una imagen válida
- Verificación con AppTest: inicio sin archivo y feed conservado; vistas previas JPEG y PNG y aviso de archivo inválido con selector simulado
- Revisión visual manual de la primera versión: el usuario confirmó que la pantalla se ve bien
- Perfil ficticio con nombre, usuario y biografía en st.sidebar
- Verificación con Streamlit AppTest: datos del perfil en la barra lateral, título y tres imágenes del feed; ejecución sin excepciones
- Feed de ejemplo con tres usuarios ficticios, fotografías de Picsum y descripciones
- Verificación del feed con Streamlit AppTest: sin excepciones; tres usuarios, elementos de imagen y descripciones comprobados
- Preferencia actual: guardar con commits locales; posponer git push
- Documentación del flujo Git/GitHub para guardar cada paso; reglas persistentes y .gitignore añadidos
- Definición inicial de funcionalidades
- Selección de Python y Streamlit como tecnologías iniciales
- Estructura mínima: app.py y requirements.txt
- Página principal con título, bienvenida y aviso de prototipo
- Instrucciones de ejecución en README.md
- Verificación con Streamlit AppTest: ejecución sin excepciones, título y aviso comprobados

## En progreso
- Esperando aprobación del usuario para publicar temporalmente en el feed

## Pendiente
- Aprobar el botón Publicar y las publicaciones temporales con st.session_state
- Implementar persistencia
- Implementar autenticación

## Problemas conocidos
Ninguno reportado tras la verificación con AppTest y la revisión visual del usuario.
Las fotografías externas de Picsum requieren Internet. El prototipo no está listo
para producción.
El usuario confirmó la revisión visual del selector y la vista previa. No se han
confirmado por separado las pruebas de sustitución, eliminación y archivo inválido
en el navegador; las pruebas automatizadas utilizaron archivos simulados.

## Próxima tarea
Propuesta pendiente de aprobación: añadir un botón Publicar, validar que exista
una imagen válida y añadir la foto con su descripción al principio del feed mediante
st.session_state. Las publicaciones se conservarán solo durante la sesión, sin
persistencia en disco ni base de datos. Pedir aprobación antes de implementar.
