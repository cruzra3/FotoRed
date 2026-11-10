# PROGRESS.md

## Estado actual
Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Revisión visual manual completada por
el usuario, quien confirmó que la pantalla se ve bien.
Selección y previsualización de fotografías implementadas con aprobación del usuario.

## Completado
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
- Revisión manual del selector de fotografías y su vista previa

## Pendiente
- Comprobar en el navegador la selección, sustitución y eliminación de una fotografía
- Implementar persistencia
- Implementar autenticación

## Problemas conocidos
Ninguno reportado tras la verificación con AppTest y la revisión visual del usuario.
Las fotografías externas de Picsum requieren Internet. El prototipo no está listo
para producción.
La carga mediante el selector real del navegador queda pendiente de revisión manual;
las comprobaciones automatizadas de la vista previa simularon el archivo seleccionado.

## Próxima tarea
Revisar manualmente el selector y la vista previa. Después, proponer un incremento
pequeño y pedir aprobación antes de aplicarlo.
