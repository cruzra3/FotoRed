# PROGRESS.md

## Estado actual
Versión local de FotoRed completada y aceptada por el usuario: confirmó que todo
el checklist final funcionó sin problemas. Las cuatro etapas y las ocho
funcionalidades acordadas están implementadas. Se conservan los resultados de las
15 pruebas automatizadas previas con bases temporales y la aceptación manual final.
Etapa 4 guardada en el commit local verificado 35c7b49. Este cierre es del prototipo
local de aprendizaje, sin despliegue ni preparación para producción.

Primera versión implementada: página principal, feed de tres publicaciones ficticias
y perfil de ejemplo en la barra lateral. Revisión visual manual completada por
el usuario, quien confirmó que la pantalla se ve bien.
Selección y previsualización de fotografías implementadas con aprobación del usuario.
La vista previa incluye una descripción opcional, revisada por el usuario y guardada
en un commit local. Ahora el botón Publicar guarda foto, descripción y usuario
ficticio en SQLite, conservándolos tras recargar o reiniciar la aplicación.
El usuario comprobó satisfactoriamente la publicación con y sin descripción,
el orden de las publicaciones y su pérdida al recargar la página en la versión
anterior de publicaciones temporales. Después confirmó que la versión con SQLite
se ve bien y realizó el commit local.

## Plan de cierre en cuatro etapas
1. Sesiones y autoría: implementada y aceptada por el usuario tras sus pruebas.
2. Perfiles y búsqueda: implementada; usuario confirmó commit y avanzar a etapa 3.
3. Likes, comentarios y seguimiento: implementada; usuario confirmó commit y avanzar a etapa 4.
4. Feed de seguidos, navegación y revisión final: implementada, verificada automáticamente y aceptada por el usuario.

## Completado
- Aceptación final: el usuario confirmó que todo funcionó sin problemas; cierre de las cuatro etapas
- Commit de etapa 4 confirmado por el usuario y verificado: 35c7b49
- Etapa 4: feed General y Siguiendo; consulta JOIN por seguimientos, orden descendente y sin duplicados
- Feed vacío con orientación; Siguiendo excluye fotos propias, cuentas no seguidas y contenido sin cuenta
- Navegación integrada con perfiles y búsqueda; cambiar feed sale del perfil y cerrar sesión vuelve a General
- Fotos fijas agrupadas en sección de ejemplo plegada; datos antiguos conservados y sin atribución automática
- Quince pruebas unittest/AppTest pasadas: etapas anteriores, filtrado con tres cuentas, seguir/dejar de seguir, navegación y persistencia de interacciones entre sesiones; bases temporales
- README actualizado con funcionamiento, checklist final y límites del prototipo local
- Etapa 3: tablas likes, comentarios y seguimientos creadas sin borrar datos; claves compuestas, claves foráneas activas en escrituras y prohibición de autoseguimiento
- Dar/quitar likes por cuenta, contadores y lectura pública de comentarios en feed y perfiles
- Comentarios de 1 a 500 caracteres, con autor real y orden cronológico; rechazo de vacíos y espacios
- Seguir/dejar de seguir desde perfiles ajenos; contadores de seguidores/seguidos; acciones solo con sesión y cuentas existentes
- Contenido antiguo sin cuenta asociada permanece sin interacciones
- Trece pruebas unittest/AppTest pasadas: etapas anteriores más persistencia, likes únicos por cuenta, comentarios, seguidores, rechazo de invitado/datos inexistentes y flujo de UI; BD temporales
- Etapa 2: migración repetible añade nombre_visible y biografia sin borrar cuentas, hashes ni publicaciones
- Edición de nombre visible (60 caracteres) y biografía (150); usuario único sin cambios; actualización dirigida al id de sesión
- Búsqueda pública por usuario y nombre visible, coincidencias parciales con casefold Unicode y comodines escapados
- Navegación desde Mi perfil, resultados y autores; Volver al feed; aviso de perfil sin publicaciones o inexistente
- Publicaciones de cada perfil filtradas por usuario_id; contenido antiguo de ejemplo no atribuido a cuentas
- Ocho pruebas unittest/AppTest pasadas: perfiles, límites, búsqueda, privacidad del editor, filtrado y navegación, además de los flujos de la etapa 1; bases temporales
- El usuario confirmó que sus pruebas de la etapa 1 y del flujo de acceso/registro funcionan; commit local verificado: 905c322
- Flujo de acceso separado: alternancia entre login y registro; al autenticar se ocultan ambos formularios
- Errores conservan entradas; cambiar de formulario limpia credenciales; registro exitoso vuelve al login con confirmación
- Consulta a páginas oficiales de Instagram bloqueada por HTTP 429; adaptación de flujo para FotoRed sin afirmar copia exacta ni verificación de la interfaz actual
- Cinco pruebas unittest/AppTest pasadas, incluida alternancia, corrección tras error, registro y login posterior y limpieza de contraseñas; BD temporal
- Etapa 1: verificación PBKDF2 con compare_digest, identidad en st.session_state y cierre de sesión
- Publicar requiere sesión y cuenta existente; autor obtenido desde SQLite por id
- Migración repetible añade usuario_id nullable sin modificar filas antiguas; contenido sin autor real etiquetado como ejemplo
- Editor separado por cuenta y limpieza al salir para evitar arrastrar borradores entre cuentas
- Cuatro pruebas unittest/AppTest pasadas: credenciales, migración, rechazo de cuenta inexistente y flujo de dos cuentas/publicación/logout/sesión nueva; bases temporales y selector simulado
- Durante las pruebas se detectó texto retenido al salir; corregido mediante claves del editor por cuenta
- Revisión manual del registro aceptada por el usuario; listo para guardar este paso mediante commit local
- Longitud de contraseña de registro ajustada por solicitud del usuario: mínimo 8 y máximo 20 caracteres, en validación, formulario y README
- Verificación en BD temporal y AppTest: 8 y 20 caracteres aceptados, 7 y 21 rechazados en la función de registro; campo limitado a 20 y mensajes del formulario comprobados
- Registro de usuarios aprobado e implementado: tabla usuarios añadida sin borrar publicaciones y formulario en la barra lateral
- Nombres únicos normalizados a minúsculas; validación de nombre y longitud de contraseña; mensajes de duplicado y error de base de datos
- Contraseñas protegidas con PBKDF2-HMAC-SHA256 (600 000 iteraciones) y sal aleatoria de 16 bytes; algoritmo, iteraciones, sal y hash almacenados, sin texto plano
- Verificación con BD temporal y AppTest: registro, duplicados con mayúsculas/espacios, entradas inválidas, sales distintas, hash reproducible y conservación de publicaciones; sin excepciones
- Revisión de SQLite confirmada por el usuario; commit local verificado: 5cf8669 (Guardar publicaciones localmente con SQLite)
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
- Ninguna tarea de implementación en progreso; versión local aceptada

## Pendiente
- Guardar esta documentación de cierre mediante commit local
- Ninguna funcionalidad pendiente del alcance local acordado

## Problemas conocidos
- El usuario reportó que pudo registrar una cuenta con la contraseña de 7 caracteres Abcd123.
  No reproducido con el código actual: AppTest envió esa contraseña con un nombre
  nuevo, mostró el error de longitud y se comprobó que no insertó usuarios en una
  base temporal. Posteriormente el usuario confirmó estar satisfecho con las pruebas.
  No se determinó la causa del reporte inicial ni se confirmó una corrección de código.
  No se modificó la validación ni se borraron cuentas reales.
Las fotografías externas de Picsum requieren Internet. El prototipo no está listo
para producción.
La base local no se sube con Git y necesita respaldo separado. El feed es público:
las sesiones que comparten la base pueden ver las mismas publicaciones. Las pruebas
de persistencia usaron una base temporal, sin crear datos de prueba en la base real.
El usuario confirmó la revisión visual del selector y la vista previa. No se han
confirmado por separado las pruebas de sustitución, eliminación y archivo inválido
en el navegador; las pruebas automatizadas utilizaron archivos simulados.

## Próxima tarea
Guardar el registro de cierre mediante commit local. Cualquier ampliación o
publicación en Internet requiere un nuevo alcance aprobado por el usuario.
