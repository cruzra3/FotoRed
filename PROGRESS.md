# PROGRESS.md

## Estado actual
Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Revisión visual manual completada por
el usuario, quien confirmó que la pantalla se ve bien.
Selección y previsualización de fotografías implementadas con aprobación del usuario.
La vista previa incluye una descripción opcional, revisada por el usuario y guardada
en un commit local. Ahora el botón Publicar guarda foto, descripción y usuario
ficticio en SQLite, conservándolos tras recargar o reiniciar la aplicación.
El usuario comprobó satisfactoriamente la publicación con y sin descripción,
el orden de las publicaciones y su pérdida al recargar la página en la versión
anterior de publicaciones temporales. La nueva persistencia está pendiente de
revisión manual.

## Completado
- Persistencia local con SQLite aprobada e implementada en database.py; tabla creada automáticamente y fotos almacenadas como BLOB
- Feed lee las publicaciones guardadas por id descendente antes de las fotografías de ejemplo
- Consultas con parámetros y conexiones cerradas tras cada operación; mensajes de error al abrir, guardar o leer
- data/ excluida de Git; README actualizado con ubicación de la base, comprobación y respaldo
- Verificación con BD temporal y AppTest: publicación con/sin descripción, bytes y Unicode conservados, orden, persistencia en sesión nueva, rechazo sin foto o con archivo inválido y error de guardado sin falso éxito (selector simulado)
- Revisión manual confirmada por el usuario: publicar con y sin descripción, nuevas publicaciones primero y eliminación de publicaciones temporales al recargar
- Botón Publicar aprobado e implementado con st.session_state; nuevas publicaciones al principio del feed bajo el perfil ficticio
- Imagen almacenada como bytes en memoria, independiente del archivo del selector; descripción opcional copiada al publicar
- AppTest: bloqueo sin imagen y con archivo inválido, publicación, orden, conservación al editar y retirar archivo, y sesión nueva vacía; sin excepciones (selector simulado)
- Regla explícita en AGENTS.md: actualizar PROGRESS.md siempre que haya cambios
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
- Revisión manual de la persistencia local con SQLite

## Pendiente
- Confirmar en el navegador que las publicaciones permanecen al recargar y reiniciar Streamlit
- Implementar autenticación

## Problemas conocidos
Ninguno reportado tras la verificación con AppTest y la revisión visual del usuario.
Las fotografías externas de Picsum requieren Internet. El prototipo no está listo
para producción.
La base local no se sube con Git y necesita respaldo separado. No hay autenticación:
las sesiones que comparten la base pueden ver las mismas publicaciones. Las pruebas
de persistencia usaron una base temporal, sin crear datos de prueba en la base real.
El usuario confirmó la revisión visual del selector y la vista previa. No se han
confirmado por separado las pruebas de sustitución, eliminación y archivo inválido
en el navegador; las pruebas automatizadas utilizaron archivos simulados.

## Próxima tarea
Revisar manualmente la persistencia de publicaciones con y sin descripción tras
recargar y reiniciar Streamlit. Después, proponer un incremento pequeño y pedir
aprobación antes de implementarlo.
