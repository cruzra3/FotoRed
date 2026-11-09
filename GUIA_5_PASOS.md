# Protocolo sencillo para aprender a desarrollar con ChatGPT, Codex, Python y Streamlit

**Estructura mínima:** 1 prompt reutilizable + 3 documentos persistentes.

Esta guía reúne los cinco apartados del protocolo. Es una recomendación práctica de aprendizaje, no un estándar obligatorio u oficial de OpenAI.

## Paso 1. Preparar los tres documentos persistentes

| Documento | Función | Cuándo se actualiza |
| --- | --- | --- |
| `AGENTS.md` | Reglas de trabajo y explicaciones que debe seguir Codex | Cuando cambien las reglas |
| `PROJECT.md` | Qué aplicación quieres construir, funcionalidades y límites | Cuando cambien los requisitos |
| `PROGRESS.md` | Qué se completó, qué sigue y qué problemas hay | Después de cada tarea |

`AGENTS.md` es una convención de instrucciones que Codex reconoce al trabajar en un repositorio. `PROJECT.md` y `PROGRESS.md` son nombres recomendados, pero **no** son archivos especiales que Codex interprete automáticamente. Se le indica que los lea mediante `AGENTS.md` y el prompt.

Ejemplo del proyecto: FotoRed, una aplicación web social con funciones similares a Instagram, desarrollada progresivamente con Python y Streamlit. Para la primera versión solo se propone una página inicial, un feed de ejemplo y un perfil de ejemplo, sin autenticación ni base de datos real.

Los documentos completos están en esta misma carpeta:
- `AGENTS.md`
- `PROJECT.md`
- `PROGRESS.md`

## Paso 2. Utilizar un solo prompt maestro

Abre `PROMPT_MAESTRO.md`, copia el prompt y utilízalo en ChatGPT o Codex **cuando la herramienta tenga acceso a los tres documentos**. El prompt obliga a leer las referencias, identificar una tarea pequeña, explicar el plan, implementarla si la herramienta tiene acceso al código, verificar lo posible y actualizar el progreso.

Si una herramienta no puede leer o editar los archivos, deberá indicarlo y facilitar los cambios manualmente. No debe fingir que probó código ni que actualizó archivos.

## Paso 3. Organizar la carpeta y conectar el contexto

Estructura inicial:

```text
FotoRed/
├── AGENTS.md
├── PROJECT.md
├── PROGRESS.md
└── app.py                 # lo creará Codex en la primera tarea
```

Para empezar puedes colocar también `PROMPT_MAESTRO.md` y esta guía en la misma carpeta. **No existe todavía `app.py` en el ZIP**: Codex lo generará cuando implementes la primera tarea.

**En ChatGPT:** crea un Proyecto llamado FotoRed. Copia las reglas de `AGENTS.md` en las instrucciones del proyecto y adjunta `PROJECT.md` y `PROGRESS.md` como fuentes. En una sesión nueva, utiliza el prompt maestro.

**En Codex:** abre la carpeta FotoRed como repositorio/carpeta de trabajo. `AGENTS.md` se usa para instrucciones del repositorio; el prompt o ese archivo indican leer `PROJECT.md` y `PROGRESS.md`.

**Sincronización:** adjuntar documentos a ChatGPT no sincroniza sus modificaciones automáticamente con los archivos locales de Codex. Tras cada tarea, conserva una versión actualizada en ambos entornos si usas los dos.

## Paso 4. Repetir el ciclo de aprendizaje

1. **Pedir:** usa el prompt y selecciona una tarea pequeña.
2. **Crear:** Codex implementa esa tarea, o ChatGPT facilita los cambios si no puede editar código.
3. **Probar:** ejecuta la aplicación y comprueba si funciona; no des por superadas pruebas no ejecutadas.
4. **Registrar:** actualiza `PROGRESS.md` con lo que realmente se completó y lo pendiente.
5. **Repetir:** avanza a la siguiente funcionalidad.

Ejemplo del orden: página principal → feed ficticio → perfil ficticio → persistencia → autenticación. El orden es orientativo, no un cronograma obligatorio.

## Paso 5. Dejar las Skills para después

Para el aprendizaje inicial **no necesitas crear un `SKILL.md`**. Las Skills son apropiadas para procedimientos repetibles en distintos proyectos; por el momento bastan las reglas de `AGENTS.md`, la descripción `PROJECT.md` y el estado `PROGRESS.md`.

Si más adelante repites frecuentemente el mismo tipo de procedimiento (por ejemplo, añadir funcionalidades con pruebas), entonces puedes plantearte una Skill para Codex.

## Referencias oficiales (para consultar capacidades, no como aval de este protocolo)

- Codex: `AGENTS.md` — https://developers.openai.com/codex/guides/agents-md
- Codex: Skills — https://developers.openai.com/codex/skills
- ChatGPT Projects — https://help.openai.com/en/articles/10169521-projects-in-chatgpt

**Nota:** estos enlaces son referencias oficiales conocidas; su contenido exacto puede evolucionar. Esta carpeta contiene solo documentación y el prompt: no es todavía una aplicación implementada o probada.
