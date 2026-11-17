# Descargar y Ejecutar FotoRed en otra computadora

Guía para **macOS y Linux**. Necesitas Internet para clonar e instalar dependencias.
La URL se obtuvo del remoto local configurado.

1. **Comprueba Git y Python.** Abre una terminal:

   ```bash
   git --version
   python3 --version
   ```

   Deben aparecer versiones. Usa Python 3.14. Si falta una herramienta,
   instálala antes de continuar.

2. **Elige dónde guardar el proyecto.** Por ejemplo:

   ```bash
   cd ~/Documents
   ```

   La carpeta debe existir. No uses una ubicación donde ya haya otra carpeta FotoRed.

3. **Descarga el proyecto y entra en su carpeta.**

   ```bash
   git clone https://github.com/cruzra3/FotoRed.git
   cd FotoRed
   ```

   Si es privado, necesitas acceso. Para autenticación HTTPS usa un token cuando
   solicite contraseña, no la contraseña de GitHub. No incluyas tokens en la URL
   ni en archivos. Los pasos siguientes se ejecutan dentro de FotoRed.

4. **Crea un entorno virtual nuevo.**

   ```bash
   python3 -m venv env
   ```

   No copies el entorno del equipo anterior. Los comandos usan directamente su
   Python, sin tener que activarlo. Este entorno está excluido por el .gitignore
   actual del proyecto.

5. **Instala las bibliotecas.**

   ```bash
   env/bin/python -m pip install -r requirements.txt
   ```

   Espera a que termine sin errores. No uses --break-system-packages. Si falla,
   guarda el mensaje y resuelve ese paso antes de continuar.

6. **Ejecuta las pruebas automáticas.**

   ```bash
   env/bin/python -m unittest discover -s tests -v
   ```

   Deben terminar sin fallos. Estas pruebas comprueban código; no sustituyen
   revisar la aplicación en el navegador. Esta guía se preparó revisando el
   proyecto local, sin instalarlo ni ejecutar sus pruebas en otra computadora.

7. **Elige si empezar vacío o conservar tus datos.** Para empezar de cero no tienes
   que configurar nada: la app crea la base al arrancar y podrás registrar cuentas.
   Para conservar los usuarios, fotos e interacciones, detén FotoRed en ambos equipos
   y copia de forma privada `data/fotored.sqlite3` del equipo anterior al nuevo, en
   la misma ruta. Crea `data/` si no existe. Las imágenes están dentro de esa base.
   Si ya hay una base en el destino, respáldala antes; reemplazar no combina registros.

8. **Inicia y comprueba la aplicación.**

   ```bash
   env/bin/python -m streamlit run app.py
   ```

   Abre la dirección que indique Streamlit, normalmente http://localhost:8501.
   Deja abierta la terminal. Registra una cuenta si empezaste vacío, inicia sesión y publica una foto. Si restauraste la base, comprueba tus cuentas y publicaciones anteriores.

9. **Detén y vuelve a abrir la app.** Pulsa Ctrl+C en la terminal para detenerla.
   Otro día entra en la carpeta FotoRed y repite el comando del paso 8. No hace
   falta crear el entorno ni instalar las bibliotecas cada vez.

La base y sus fotos no se descargan de GitHub porque data/ está excluida. Las fotos fijas de ejemplo de Picsum necesitan Internet.
Clonar descarga código e historial, no los archivos ignorados. Trasladar datos es
un paso separado y privado. Esta guía ejecuta la aplicación localmente; no la
publica en Internet.
