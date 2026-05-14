# Manual de Configuración — MARK XXXIX

Guía para administradores y usuarios avanzados. Cubre modelos, voces, prompts, rutas, paneles, memoria, herramientas y solución de problemas a nivel de instalación.

> Para el uso diario consulta [MANUAL_USUARIO.md](MANUAL_USUARIO.md).

---

## 1. Estructura del proyecto

```
IA-Project/
├── main.py                 ← entrada; sesión Live, audio, UI
├── ui.py                   ← interfaz PyQt6 (HUD, paneles, setup)
├── setup.py                ← script auxiliar de instalación
├── readme.md
├── requirements.txt
├── face.png                ← (opcional) rostro del avatar; si no existe, el HUD se muestra sin imagen central
│
├── config/
│   ├── __init__.py         ← detección de SO, lectura de config
│   └── api_keys.json       ← (creado en 1ª ejecución)
│
├── core/
│   └── prompt.txt          ← prompt del sistema (personalidad)
│
├── memory/
│   ├── config_manager.py   ← lectura/escritura api_keys.json
│   ├── memory_manager.py   ← memoria a largo plazo (long_term.json)
│   └── long_term.json      ← (creado al guardar la primera entrada)
│
├── agent/
│   ├── planner.py          ← descompone objetivos en pasos
│   ├── executor.py         ← ejecuta pasos secuencialmente
│   ├── error_handler.py    ← decide retry/skip/replan/abort
│   └── task_queue.py       ← cola de tareas en segundo plano
│
├── actions/                ← 17 herramientas
│   ├── browser_control.py
│   ├── code_helper.py
│   ├── computer_control.py
│   ├── computer_settings.py
│   ├── desktop.py
│   ├── dev_agent.py
│   ├── file_controller.py
│   ├── file_processor.py
│   ├── flight_finder.py
│   ├── game_updater.py
│   ├── open_app.py
│   ├── reminder.py
│   ├── screen_processor.py
│   ├── send_message.py
│   ├── weather_report.py
│   ├── web_search.py
│   └── youtube_video.py
│
├── docs/                   ← este manual y el de usuario
└── .venv/                  ← entorno virtual (Python 3.11)
```

---

## 2. Instalación desde cero

### 2.1 Requisitos
- Python **3.11 o 3.12** (no usar 3.13/3.14: incompatibilidad con `pyaudio`/`pycaw`)
- Git
- Conexión a internet
- Cuenta Google con API key de Gemini ([aistudio.google.com/apikey](https://aistudio.google.com/apikey))

### 2.2 Pasos en Windows (PowerShell)

```powershell
# 1. Clonar
git clone https://github.com/FatihMakes/Mark-XXXIX.git
cd Mark-XXXIX

# 2. Crear venv con Python 3.11 explícito
py -3.11 -m venv .venv

# 3. Activar venv
.\.venv\Scripts\Activate.ps1

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Instalar navegadores Playwright
python -m playwright install

# 7. Ejecutar
python main.py
```

> En este equipo ya está hecho. Usa directamente `.\.venv\Scripts\python.exe main.py`.

### 2.3 Variables de entorno (opcional)
Ninguna obligatoria. La API key se guarda en `config/api_keys.json` por la UI. No se usan archivos `.env`.

---

## 3. Archivo de claves — `config/api_keys.json`

**Ruta:** `config/api_keys.json` (creado tras el primer setup)
**Esquema:**

```json
{
  "gemini_api_key": "AIzaSy...",
  "os_system": "windows"
}
```

| Campo | Tipo | Valores | Descripción |
|---|---|---|---|
| `gemini_api_key` | string | API key válida | Clave de Google Gemini |
| `os_system` | string | `windows` \| `mac` \| `linux` | Detecta automáticamente; afecta al routing de herramientas específicas del SO |

**Para reiniciar configuración:** borra el archivo y vuelve a abrir la app.

**Lectura programática:** `memory/config_manager.py:load_api_keys()` → devuelve dict; `get_gemini_api_key()` → solo la clave.

---

## 4. Modelos de Gemini en uso

| Propósito | Modelo | Archivo:línea | ¿Cambiar? |
|---|---|---|---|
| **Voz en vivo (principal)** | `models/gemini-2.5-flash-native-audio-preview-12-2025` | `main.py:45` | Sí, pero debe soportar Live API + audio nativo |
| **Visión por pantalla** | `models/gemini-2.5-flash-native-audio-preview-12-2025` | `actions/screen_processor.py:75` | Igual al anterior |
| **Planificador inicial** | `gemini-2.5-flash-lite` | `agent/planner.py:179` | Sí, modelo barato para razonar pasos |
| **Refinamiento de plan / ejecución** | `gemini-2.5-flash` | `agent/planner.py:239`, `agent/executor.py:51, 151, 382` | Modelo balance precio/capacidad |
| **Análisis de errores** | `gemini-2.5-flash-lite` | `agent/error_handler.py:95` | Igual que el planner |
| **Generación de código de recuperación** | `gemini-2.0-flash` | `agent/error_handler.py:154` | Anterior generación, más estable |
| **Configuración del PC (LLM auxiliar)** | `gemini-2.5-flash-lite` | `actions/computer_settings.py:575` | Razonamiento sobre comandos del SO |
| **Búsqueda web (Grounding)** | `gemini-2.5-flash` | `actions/web_search.py:26` | Soporta Google Search Grounding |
| **YouTube/file/code/dev** | `gemini-2.5-flash` | `actions/youtube_video.py:165`, `actions/file_processor.py:39`, `actions/code_helper.py:18,476`, `actions/dev_agent.py:19,20` | — |
| **Vuelos** | `gemini-2.5-flash-lite` | `actions/flight_finder.py:67` | — |

**Para cambiar un modelo:** edita la constante en el archivo correspondiente. Ejemplo, bajar todo a `gemini-2.5-flash-lite` para reducir costo:

```python
# main.py:45
MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"  # NO cambiar este (necesita audio nativo)

# agent/executor.py:51
EXECUTOR_MODEL = "gemini-2.5-flash"  # → puedes bajarlo a flash-lite
```

> Lista completa de modelos disponibles: https://ai.google.dev/gemini-api/docs/models

---

## 5. Voz del asistente

**Archivo:** `main.py:561`
**Constante:** `voice_name = "Charon"`

Voces disponibles en Gemini Live (preconstruidas):

| Voz | Tipo |
|---|---|
| Puck | Joven, neutra |
| Charon | Profunda, masculina **(actual)** |
| Kore | Femenina cálida |
| Fenrir | Profunda, dramática |
| Aoede | Femenina suave |

**Para cambiar:**

```python
# main.py, función run(), aprox línea 561
voice_name = "Kore"  # cambia por la deseada
```

Reinicia la app para aplicar.

---

## 6. Idioma

**No hay configuración explícita de idioma.** El modelo de voz nativo detecta el idioma del usuario y responde en el mismo. Si quieres forzar un idioma:

1. Edita `core/prompt.txt`.
2. Añade al inicio una línea como: `Always respond in Spanish, regardless of input language.`
3. Reinicia.

---

## 7. Prompt del sistema — `core/prompt.txt`

Este archivo define la **personalidad y reglas** del asistente. Se carga al iniciar y se inyecta como contexto a todos los modelos.

**Para personalizar:**
- Tono, estilo de respuesta, emojis, formalidad.
- Reglas de seguridad (ej. "nunca borres archivos sin confirmar").
- Restricciones de herramientas ("no uses send_message sin pedir permiso").
- Memoria activa (qué guardar / qué no).

**Recomendación:** haz una copia (`prompt.txt.bak`) antes de editarlo. Un mal prompt puede romper el routing de herramientas.

---

## 8. Memoria a largo plazo

**Archivo:** `memory/long_term.json`
**Gestor:** `memory/memory_manager.py`

### Esquema

```json
{
  "identity":      { "name":         { "value": "Oscar", "updated": "2026-05-13" } },
  "preferences":   { "favorite_food":{ "value": "...",   "updated": "..." } },
  "projects":      { "learn_python": { "value": "...",   "updated": "..." } },
  "relationships": { "sister":       { "value": "...",   "updated": "..." } },
  "wishes":        { "travel_japan": { "value": "...",   "updated": "..." } },
  "notes":         { "custom":       { "value": "...",   "updated": "..." } }
}
```

### Constantes ajustables

| Constante | Archivo:línea | Valor por defecto | Efecto |
|---|---|---|---|
| `MAX_VALUE_LEN` | `memory_manager.py:17` | 380 caracteres | Trunca cada entrada larga con "…" |
| `MAX_TOTAL_SIZE` | `memory_manager.py:18` | 2200 caracteres | Si se excede, elimina las más antiguas |

### Operaciones

- **Borrar todo:** elimina `memory/long_term.json`.
- **Editar manualmente:** abre el JSON, ajusta campos. La próxima sesión los leerá.
- **Backup:** copia el archivo a otra ubicación.
- **Compartir entre usuarios:** no recomendado (mezcla identidades).

---

## 9. Interfaz — personalización visual

**Archivo:** `ui.py`

### Tamaños y geometría

| Variable | Línea | Default |
|---|---|---|
| `_LEFT_W` | 42 | 148 px (panel izquierdo) |
| `_RIGHT_W` | 43 | 340 px (panel derecho) |
| Tamaño mínimo ventana | ~ | 820 × 580 |
| Tamaño por defecto | ~ | 980 × 700 |

### Paleta de colores — clase `C` (líneas 48-69)

```python
class C:
    BG       = "#0a0e1a"   # fondo principal
    PANEL    = "#0f1521"   # paneles laterales
    PRIMARY  = "#00d4ff"   # cyan acento
    ACCENT   = "#ff8800"   # naranja secundario
    TEXT     = "#e4e7eb"   # texto base
    MUTED    = "#5e6675"   # texto secundario
    OK       = "#00ff88"   # éxito (mic activo)
    BAD      = "#ff3b3b"   # error (mic muteado)
    # ...
```

Cambia los hex para repintar todo el HUD.

### Avatar (`face.png`)

- **Es opcional.** El repo no incluye `face.png`; si falta, el HUD funciona igual pero sin imagen central (solo anillos, waveform y demás efectos).
- Para añadir rostro: coloca un PNG cuadrado llamado `face.png` en la raíz del proyecto.
- El HUD aplica máscara circular y escala según el audio (ver [ui.py:276-291](../ui.py#L276-L291)).
- Tamaño recomendado: 256×256 o superior.
- El nombre se puede cambiar editando [main.py:867](../main.py#L867): `JarvisUI("otro_nombre.png")`.

### Atajos de teclado

| Tecla | Acción | Definido en |
|---|---|---|
| F4 | Toggle mic | `ui.py` (handler en MainWindow) |
| F11 | Toggle pantalla completa | `ui.py` |
| Enter | Enviar texto | `ui.py` (signal del QLineEdit) |

Para añadir más atajos, busca `keyPressEvent` en `ui.py:MainWindow`.

---

## 10. Audio

**Archivo:** `main.py`

| Constante | Línea | Default | Notas |
|---|---|---|---|
| `SEND_SAMPLE_RATE` | 47 | 16000 Hz | Mic → API. Formato esperado por Gemini Live |
| `RECEIVE_SAMPLE_RATE` | 48 | 24000 Hz | API → speakers. NO cambiar |
| `CHUNK_SIZE` | 49 | 1024 | Tamaño de buffer; bajarlo reduce latencia pero sube CPU |

**Dispositivo de audio:** se usa el predeterminado del SO. Para forzar uno específico, edita las llamadas a `sounddevice.RawInputStream` / `RawOutputStream` añadiendo el parámetro `device=N` (donde `N` se obtiene con `python -m sounddevice`).

---

## 11. Pipeline del agente — parámetros

### Planner — `agent/planner.py`
- Máximo de pasos: **5** (definido en el prompt PLANNER_PROMPT, líneas 17-166).
- Si parsea mal, recae en un único paso `web_search`.
- Cambiar el límite implica editar el prompt.

### Executor — `agent/executor.py`
- Reintentos por paso: **3** (constante `MAX_RETRIES`, ~línea 50).
- Backoff entre reintentos: 2 segundos.
- Replanificaciones máximas: **2** (`MAX_REPLANS`, ~línea 251).

### Task queue — `agent/task_queue.py`
- Tareas concurrentes: **1** (`MAX_CONCURRENT`, línea 38).
- Prioridades: HIGH=1, NORMAL=2, LOW=3.
- Para correr varias tareas a la vez, sube `MAX_CONCURRENT` (cuidado con conflictos en el mouse/teclado).

### Error handler — `agent/error_handler.py`
- Decisiones posibles: `RETRY`, `SKIP`, `REPLAN`, `ABORT`.
- Genera código de fallback con `gemini-2.0-flash` cuando es necesario.

---

## 12. Herramientas — habilitar/deshabilitar

Las 17 herramientas se declaran en `main.py:73-481` como `tool_declarations`. Para deshabilitar una:

1. Comenta su entrada en la lista de tools.
2. El planificador dejará de usarla.
3. Verifica que `_execute_tool` (~línea 480) tampoco la enrute.

**Caso típico:** desactivar `reminder` en macOS/Linux porque depende de Task Scheduler de Windows.

---

## 13. Dependencias específicas por SO

### Windows (todo soportado)
Paquetes que NO existen en otros SO y son obligatorios para sus herramientas:
- `pycaw` — control de audio
- `comtypes` — interfaz COM
- `pywinauto` — automatización UI
- `win10toast` — notificaciones
- `winreg` — registro (módulo built-in en Win)
- `pygetwindow`, `pyautogui` — control de ventanas/mouse

### macOS
- Sustituye `pycaw` por `osascript` (no incluido).
- `reminder.py` no funciona; usa `osascript` para Calendar manualmente.
- Algunas funciones requieren permisos de Accesibilidad (System Settings → Privacy & Security).

### Linux
- Sin `pycaw`, usar `pactl` (PulseAudio) o `amixer` (ALSA).
- `pywinauto` no aplica; algunos `computer_control` fallarán.

---

## 14. Logs y depuración

### Log en pantalla
Panel derecho de la UI → ActivityLog. Muestra acciones, resultados y errores.

### Log en consola
Toda salida `print()` va a la consola desde donde lanzaste `python main.py`. Para guardarla:

```powershell
.\.venv\Scripts\python.exe main.py *> log.txt
```

### Modo verbose
No hay flag oficial. Para más detalle, añade prints en:
- `agent/executor.py:execute()` — antes y después de cada `_call_tool`.
- `agent/error_handler.py:analyze_error()` — para ver decisiones.

---

## 15. Costos y cuotas

**Plan gratuito de Gemini** (a la fecha de este manual):
- Generoso para uso personal: ~ varios cientos de llamadas/día.
- El modelo de **audio nativo** consume tokens más rápido que texto puro.
- Monitor de uso: https://aistudio.google.com/apikey

**Para minimizar costo:**
- Cambia `gemini-2.5-flash` → `gemini-2.5-flash-lite` en planner/executor (sección 4).
- Apaga el mic cuando no lo uses (F4) — la sesión Live consume tokens incluso en silencio.
- Limita la memoria en `MAX_TOTAL_SIZE` (cada llamada incluye el contexto).

---

## 16. Seguridad

⚠️ **Riesgos a tener en cuenta:**

1. **Ejecuta acciones reales:** borra archivos, navega, escribe código, instala paquetes. No hay confirmación previa por defecto.
2. **API key en texto plano:** `config/api_keys.json` no está cifrado. Excluye esta carpeta de cualquier sync público (Git, OneDrive público).
3. **Memoria con datos personales:** `memory/long_term.json` puede contener nombres, relaciones, proyectos. Mismo cuidado.
4. **Permisos del SO:** el asistente tiene los mismos permisos que tu usuario. Si lo corres como admin, puede modificar el sistema.

**Recomendaciones:**
- Añade `config/api_keys.json` y `memory/long_term.json` a `.gitignore` (ya viene excluido en el repo original; verifica).
- Para confirmaciones manuales, edita `core/prompt.txt` y agrega: `Antes de cualquier acción destructiva (borrar, sobrescribir, enviar mensaje), pide confirmación explícita al usuario.`

---

## 17. Actualización

```powershell
cd "c:\Users\Oscar Dev\Documents\IA-Project"
git pull
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install
```

Tras `git pull`, revisa si el README o el CHANGELOG mencionan cambios de schema en `api_keys.json` o `long_term.json`.

---

## 18. Desinstalación

```powershell
# Cierra la app
# Borrar entorno virtual
Remove-Item -Recurse -Force .\.venv
# Borrar config y memoria (opcional, si quieres limpiar tus datos)
Remove-Item .\config\api_keys.json
Remove-Item .\memory\long_term.json
# Borrar el repo entero
cd ..
Remove-Item -Recurse -Force .\IA-Project
```

---

## 19. FAQ técnica

**P: ¿Puedo usar Anthropic Claude / OpenAI en vez de Gemini?**
R: No directamente. Toda la app está acoplada al SDK `google-genai` y al modelo Live. Habría que reescribir el loop principal.

**P: ¿Funciona offline?**
R: No. El modelo está en la nube de Google.

**P: ¿Por qué se reconecta cada cierto tiempo?**
R: La sesión Live tiene un máximo de duración (~10-15 min). El loop reconecta automáticamente con backoff de 3s (`main.py:864`).

**P: ¿Cómo añadir mi propia herramienta?**
R:
1. Crea `actions/mi_herramienta.py` con una función pública.
2. Importa en `main.py`.
3. Añade su declaración a `tool_declarations` (`main.py:73-481`).
4. Añade su despacho en `_execute_tool`.
5. Reinicia.

**P: ¿Dónde están los pesos del modelo?**
R: En servidores de Google. El cliente solo envía/recibe streams.

**P: ¿Soporta multiusuario?**
R: No. La memoria es global por instalación.

---

## 20. Referencias

- Repo original: https://github.com/FatihMakes/Mark-XXXIX
- Gemini API: https://ai.google.dev/gemini-api/docs
- Lista de modelos: https://ai.google.dev/gemini-api/docs/models
- Playwright Python: https://playwright.dev/python/
- PyQt6: https://doc.qt.io/qtforpython-6/
- Gestiona tu API key: https://aistudio.google.com/apikey

---

Última revisión: 2026-05-13.
