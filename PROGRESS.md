# PROGRESS.md

## Estado actual
Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Revisión visual manual completada por
el usuario, quien confirmó que la pantalla se ve bien.

## Completado
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
- Esperando aprobación del usuario para el siguiente incremento

## Pendiente
- Aprobar e implementar la selección y previsualización de una fotografía
- Implementar persistencia
- Implementar autenticación

## Problemas conocidos
Ninguno reportado tras la verificación con AppTest y la revisión visual del usuario.
Las fotografías externas de Picsum requieren Internet. El prototipo no está listo
para producción.

## Próxima tarea
Propuesta pendiente de aprobación: permitir seleccionar una fotografía JPG o PNG
y previsualizarla con st.file_uploader y st.image, sin guardarla ni añadirla al feed.
Pedir aprobación antes de implementar este cambio.
