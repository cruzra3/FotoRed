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
para producción. Incluye un feed y un perfil ficticio en la barra lateral, con
nombre, usuario y biografía. Si la barra está oculta, ábrela con el control de
Streamlit en la esquina superior izquierda. Todavía no incluye autenticación
ni persistencia.

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
del feed, con el usuario ficticio del perfil. Sin una foto válida aparecerá un aviso.
La descripción es opcional. Cada clic válido crea una publicación; cambiar el texto
o quitar el archivo del selector no elimina lo ya publicado.

Esta función es una demostración: st.session_state conserva las publicaciones
en memoria durante la sesión, sin escribirlas en disco ni en una base de datos.
Al recargar la página o reiniciar la sesión se pierden. No se comparten con otros
usuarios y todavía no existe autenticación.

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
