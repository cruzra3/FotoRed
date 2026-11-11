# FotoRed — Protocolo sencillo de aprendizaje con IA

Este paquete reúne los **cinco pasos** del protocolo sencillo para aprender a crear aplicaciones con ChatGPT, Codex, Python y Streamlit.

## Empieza aquí

1. Lee `GUIA_5_PASOS.md`.
2. Ajusta `PROJECT.md` según la aplicación que quieras construir.
3. Usa `AGENTS.md` para fijar reglas de trabajo.
4. Conserva `PROGRESS.md` actualizado después de cada tarea.
5. Copia el contenido de `PROMPT_MAESTRO.md` en ChatGPT o Codex.

## Archivos
- `GUIA_5_PASOS.md`: explicación completa de los pasos 1 al 5.
- `AGENTS.md`: instrucciones persistentes para Codex.
- `PROJECT.md`: definición persistente del proyecto de ejemplo.
- `PROGRESS.md`: registro inicial del progreso.
- `PROMPT_MAESTRO.md`: prompt reutilizable.

## Ejecutar la página inicial

Desde la carpeta `Projects`, utiliza el entorno virtual existente:

```bash
env/bin/python -m pip install -r FotoRed/requirements.txt
env/bin/python -m streamlit run FotoRed/app.py
```

Abre la dirección local que indique Streamlit. Verás el título FotoRed, una
bienvenida, un aviso sobre el estado del prototipo y tres publicaciones ficticias.
Las fotografías de muestra se cargan desde Picsum y requieren conexión a Internet.

`app.py` contiene la página principal y `requirements.txt` indica la versión de
Streamlit utilizada. Este es un prototipo de aprendizaje, no una aplicación lista
para producción. Incluye un feed, registro e inicio de sesión en la barra lateral.
Si la barra está oculta, ábrela con el control de Streamlit en la esquina superior
izquierda. Incluye perfiles editables y búsqueda de cuentas.

## Previsualizar una fotografía

Puedes escribir una descripción opcional en el campo de texto. Con una fotografía
válida seleccionada, el texto aparece debajo de la vista previa. Para actualizarlo,
haz clic fuera del campo después de escribir. Si queda vacío o solo contiene
espacios, no se muestra una descripción. El texto se muestra literalmente, sin
interpretar Markdown. Editarlo no cambia publicaciones anteriores.

En la sección «Previsualizar una fotografía», selecciona un archivo JPG, JPEG o
PNG de tu computadora. Aparecerá su vista previa encima del feed. Puedes cambiar
el archivo o quitarlo usando el selector. Si el contenido no es una imagen válida,
se mostrará un aviso.

Pulsa «Publicar» para añadir una copia de la foto y su descripción al principio
del feed, con la cuenta que inició sesión. Sin una foto válida aparecerá un aviso.
La descripción es opcional. Cada clic válido crea una publicación; cambiar el texto
o quitar el archivo del selector no elimina lo ya publicado.

## Publicaciones guardadas con SQLite

`database.py` crea automáticamente `FotoRed/data/fotored.sqlite3`. Al publicar,
guarda el identificador de tu cuenta, su nombre, la descripción y los bytes de la imagen.
La base de datos se ubica junto al código aunque ejecutes Streamlit desde otra
carpeta. Se utiliza sqlite3, incluido en Python; no requiere instalar otro paquete.

Las publicaciones guardadas aparecen antes de las fotos de ejemplo, con las más
recientes primero. Permanecen al recargar o reiniciar Streamlit, siempre que se
conserve el archivo de la base de datos. Las publicaciones de la versión anterior
que solo estaban en memoria no se migran.

Para comprobarlo, publica una foto, recarga la página y después detén Streamlit
con Ctrl+C y ejecútalo de nuevo. La foto y su descripción deben seguir en el feed.
Prueba también una publicación sin descripción.

La carpeta `data/` está excluida de Git: los commits guardan el código, no las fotos
ni la base de datos. Para respaldar los datos, detén la aplicación y copia
`data/fotored.sqlite3` a un lugar seguro.

Sigue siendo un prototipo local con inicio de sesión básico. Las sesiones que usan la misma
base de datos ven las mismas publicaciones; todavía no hay privacidad por usuario.

## Registro de usuarios (prototipo)

En la barra lateral pulsa «Registrarte». Introduce un nombre de
3 a 30 letras ASCII, números o guiones bajos, y una contraseña de 8 a 20
caracteres. Los nombres se guardan en minúsculas y sin espacios en los extremos:
`Ana` y ` ana ` representan el mismo usuario. La contraseña se conserva exactamente
al calcular el hash; no se recorta ni transforma.

Pulsa «Crear cuenta». Un nombre repetido muestra un aviso. Ante un error, el formulario conserva los datos para corregirlos. Al crear
la cuenta, vuelve a Iniciar sesión con un aviso de confirmación y limpia el registro.
La tabla usuarios se crea sin borrar las publicaciones existentes.

Se almacena un hash PBKDF2-HMAC-SHA256 con 600 000 iteraciones y una sal aleatoria
independiente de 16 bytes para cada cuenta. Se guardan algoritmo, iteraciones,
sal y hash, nunca la contraseña en texto plano. Solo se usa la biblioteca estándar.
Referencia: [hashlib de Python](https://docs.python.org/3/library/hashlib.html).

Para comprobarlo, registra un nombre nuevo y vuelve a intentarlo con el mismo
nombre en mayúsculas: debe indicar que ya existe. Prueba también campos vacíos
y una contraseña corta. Una vez creada la cuenta, recarga e intenta registrarla
otra vez para comprobar su persistencia.

## Flujo de acceso

Se muestra un formulario a la vez: «Iniciar sesión» o «Crear una cuenta».
Los botones «Registrarte» e «Iniciar sesión» permiten alternar. Al cambiar de vista
se limpian los datos de ambos formularios. Los errores conservan lo escrito para
corregirlo. Tras registrar la cuenta se vuelve al acceso, sin iniciar sesión
automáticamente. Una vez dentro solo se muestra la cuenta y «Cerrar sesión».

Es una adaptación para FotoRed del patrón de acceso/registro separado. Instagram
respondió con HTTP 429 al intentar consultar sus páginas oficiales de acceso,
registro y ayuda; no se verificó su interfaz actual exacta. No se presenta esta
adaptación como una réplica exacta. FotoRed usa únicamente usuario y contraseña;
no incluye correo/teléfono, verificación por códigos, Facebook ni recuperación.

## Etapa 1: sesiones y autoría

Tras crear una cuenta, utiliza «Iniciar sesión» y pulsa «Entrar». Las cuentas
existentes siguen funcionando. El usuario se normaliza como en el registro, pero
la contraseña se verifica exactamente como fue escrita. El inicio de sesión no
impone el nuevo máximo de registro a contraseñas de cuentas creadas anteriormente.
Se recalcula PBKDF2 con la sal guardada y se compara con hmac.compare_digest:
[documentación de Python](https://docs.python.org/3/library/hmac.html#hmac.compare_digest).

La barra lateral muestra la cuenta conectada y «Cerrar sesión». Se guarda solo
su identificador y nombre en st.session_state, sin guardar su contraseña como parte
de la identidad de sesión. Al recargar la página se pierde la sesión y debes entrar
otra vez; las publicaciones guardadas siguen visibles.

Puedes ver el feed y previsualizar sin entrar. Publicar requiere una sesión y una
cuenta existente. La base obtiene el nombre a partir del id de esa cuenta. Al cerrar
sesión se limpia el estado del editor; al cambiar de cuenta no se reutiliza el borrador.

La migración añade usuario_id a publicaciones sin borrar filas ni asignar publicaciones
antiguas a cuentas por coincidencia de nombre. Las antiguas y las fotos fijas llevan
la etiqueta «Contenido de ejemplo · sin cuenta asociada». Las nuevas quedan vinculadas
a su autor real. Por ello, no uses DELETE FROM usuarios para limpiar cuentas con
publicaciones asociadas; la eliminación de cuentas no está implementada.

Comprobación manual:

- Sin entrar, el feed es visible y Publicar está deshabilitado.
- Contraseña incorrecta o usuario inexistente: aparece el mismo aviso de credenciales.
- Entra con una cuenta existente, publica y verifica su nombre en el feed.
- Cierra sesión: desaparece tu identidad, se limpia el editor y Publicar se deshabilita.
- Entra con otra cuenta y publica: debe aparecer el segundo autor.
- Recarga: se pierde la sesión, las publicaciones y autores se conservan.
- Las publicaciones anteriores siguen visibles como contenido de ejemplo.

Pruebas automatizadas desde Projects:

```bash
env/bin/python -m unittest discover -s FotoRed/tests -v
```

Usan bases temporales y simulan el selector de imágenes. Es un prototipo para uso
local: todavía no tiene recuperación de cuentas, protección frente a intentos
repetidos de acceso ni sesiones persistentes para un despliegue público.

## Etapa 2: perfiles y búsqueda

Con sesión iniciada, pulsa «Mi perfil». En «Editar mi perfil» puedes guardar un
nombre para mostrar (hasta 60 caracteres) y una biografía (hasta 150). Ambos son
opcionales; si el nombre visible está vacío, se muestra el usuario. El nombre de
usuario y la contraseña no se cambian desde este formulario.

La migración añade nombre_visible y biografia a usuarios con valores vacíos,
sin borrar cuentas, hashes ni publicaciones. No hace falta crear una base nueva.

En la barra lateral, escribe en «Usuario o nombre». La búsqueda funciona también
sin sesión, encuentra coincidencias parciales sin distinguir mayúsculas y maneja
letras acentuadas (Á coincide con á; a no equivale a á). Los signos % y _ son
literales. Una consulta vacía no lista cuentas.

Pulsa un resultado para visitar el perfil, o «Ver perfil» en una publicación con
autor real. Solo se muestran las publicaciones cuyo usuario_id coincide con el
perfil, de más reciente a más antigua. El contenido de ejemplo sin cuenta no se
asigna a perfiles por coincidencia de nombre. Si no hay publicaciones, se muestra
un aviso. «Volver al feed» regresa a la página principal.

El editor solo se muestra para la cuenta conectada. El UPDATE toma el id de la
sesión, no el del perfil visitado. Las consultas de perfil y búsqueda no devuelven
hashes de contraseñas. Los perfiles y publicaciones siguen siendo públicos en
este prototipo local; fotos de perfil y edición del nombre de usuario quedan
fuera de esta etapa.

## Guardar el progreso con Git y GitHub

Git guarda versiones del proyecto mediante **commits** en tu computadora.
GitHub guarda una copia remota cuando ejecutas **push**.
Al terminar cada paso, el asistente debe entregar comandos adaptados a los archivos
modificados y un mensaje de commit descriptivo.

### Configuración inicial (una sola vez por proyecto)

Abre una terminal dentro de la carpeta de tu proyecto. Para FotoRed, desde
`Projects`, ejecuta `cd FotoRed`. Si usas esta plantilla para otro proyecto,
entra en la carpeta de ese nuevo proyecto.

Comprueba si ya estás dentro de un repositorio:

```bash
git status
```

Si indica que no es un repositorio, inicializa uno:

```bash
git init -b main
```

Comprueba tu identidad antes del primer commit:

```bash
git config user.name
git config user.email
```

Si falta algún dato, configúralo para este proyecto (sustituye los ejemplos):

```bash
git config user.name "Tu nombre"
git config user.email "tu-correo@example.com"
```

Revisa `.gitignore` antes de preparar archivos: excluye entornos virtuales,
contraseñas y archivos locales. Después crea el primer commit:

```bash
git status
git add .
git diff --cached
git commit -m "Crear estructura inicial del proyecto"
```

Aquí `git add .` prepara todos los archivos no ignorados de esta carpeta.
Revisa el contenido de `git diff --cached` antes de confirmar.

Crea un repositorio vacío en GitHub, sin README, licencia ni `.gitignore`,
ya que los archivos se subirán desde tu proyecto. Sustituye `TU_USUARIO`
y `TU_REPOSITORIO` por los datos reales:

```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

GitHub puede solicitar autenticación. Si ya existe un remoto, consulta
`git remote -v` antes de añadir uno. Estos comandos suponen un repositorio
nuevo con rama `main`; en uno existente, conserva su configuración.

### Al terminar cada paso

Desde la carpeta del proyecto:

```bash
git status
git diff
```

Prepara solamente los archivos de la tarea. Por ejemplo, si modificaste
`README.md` y `PROGRESS.md`:

```bash
git add README.md PROGRESS.md
git diff --cached
git commit -m "Documentar el flujo para guardar el progreso"
git push
git status
```

El asistente debe ajustar esa lista a cada paso, incluyendo los archivos nuevos.
`git diff` muestra cambios en archivos ya rastreados; consulta también
`git status` y revisa los archivos nuevos. `git diff --cached` muestra exactamente
lo preparado para el commit. Si el push falla, el commit sigue guardado localmente,
pero aún no está subido a GitHub.

Para consultar tus últimos pasos:

```bash
git log --oneline -5
```

### Reutilizar esta plantilla

Copia los documentos a la carpeta del nuevo proyecto y adapta `PROJECT.md` y
`PROGRESS.md`. No copies la carpeta oculta `.git`: cada proyecto debe empezar
con su propio historial. Sigue luego la configuración inicial anterior.
