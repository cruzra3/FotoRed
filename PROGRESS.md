# PROGRESS.md

## Estado actual
Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Pendiente de revisión visual manual.

## Completado
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
- Revisión manual de la primera versión

## Pendiente
- Comprobar visualmente página principal, feed y perfil
- Implementar persistencia
- Implementar autenticación

## Problemas conocidos
Ninguno detectado en la verificación con AppTest. Pendiente de comprobación visual
manual en el navegador, incluida la descarga de fotografías externas de Picsum,
que requiere Internet. El prototipo no está listo para producción.

## Próxima tarea
Revisar manualmente la primera versión en el navegador y acordar el siguiente
incremento antes de implementar persistencia o autenticación.
