# Manual de Usuario — MARK XXXIX (J.A.R.V.I.S)

Asistente personal de inteligencia artificial con voz, visión y control de computadora.
Basado en Google Gemini 2.5.

---

## 1. Introducción

MARK XXXIX es un asistente de voz que escucha, ve, entiende y controla tu computadora en tiempo real. Funciona en Windows, macOS y Linux (con mejor soporte en Windows). Usa la API gratuita de Google Gemini.

**Lo que puede hacer en una frase:** abrir programas, buscar en la web, controlar el navegador, leer tu pantalla, escribir y ejecutar código, gestionar archivos, enviar mensajes, configurar la computadora, instalar/actualizar juegos, buscar vuelos y mucho más — todo por voz o texto.

---

## 2. Requisitos

| Requisito | Detalle |
|---|---|
| Sistema operativo | Windows 10/11, macOS o Linux |
| Python | 3.11 o 3.12 (no 3.13/3.14) |
| Micrófono | Necesario para interacción por voz |
| API Key | Google Gemini (gratis en https://aistudio.google.com/apikey) |
| Conexión | Internet estable (la voz va en streaming) |

> En este equipo ya está instalado en `c:\Users\Oscar Dev\Documents\IA-Project\` con Python 3.11 en `.venv\`.

---

## 3. Primer arranque

1. Abre PowerShell en la carpeta del proyecto.
2. Ejecuta:
   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```
3. Aparecerá la ventana del asistente con un panel de configuración inicial (**SetupOverlay**).
4. Pega tu **Gemini API key** y selecciona tu sistema operativo (se autodetecta).
5. Haz clic en **INITIALISE SYSTEMS**.
6. La clave se guarda en [config/api_keys.json](../config/) y solo te la pide la primera vez.
7. El log mostrará "SYS: JARVIS online." y el micrófono quedará activo (indicador verde).

A partir de aquí puedes hablar o escribir comandos.

---

## 4. La interfaz

```
┌─────────────────────────────────────────────────────────────┐
│ J.A.R.V.I.S                                  12:34  13/05  │
├──────────┬──────────────────────────────┬───────────────────┤
│ CPU 23%  │                              │ ACTIVITY LOG      │
│ MEM 58%  │       ●  ●  ●                │ > comando 1       │
│ NET ▓▓   │      ╭──────╮                │ > comando 2       │
│ GPU 12%  │      │ AVATAR│  ← rostro     │                   │
│ TEMP 45° │      ╰──────╯                │ ┌───────────────┐ │
│          │       ▂▄▆█▆▄▂                │ │ Drop file...  │ │
│ uptime   │                              │ └───────────────┘ │
│ procs    │                              │ [texto] [enviar]  │
│ OS: Win  │                              │ [MIC ACTIVE] [⛶] │
├──────────┴──────────────────────────────┴───────────────────┤
│ F4: micrófono   F11: pantalla completa                     │
└─────────────────────────────────────────────────────────────┘
```

### Panel izquierdo — Monitor del sistema
Muestra en tiempo real: uso de **CPU, memoria, red, GPU, temperatura**, tiempo encendido (uptime), número de procesos y sistema operativo.

### Centro — Avatar HUD
Es la "cara" del asistente. Cambia de estado visualmente:

| Estado visual | Significado |
|---|---|
| Anillos pulsando azul cyan | LISTENING — escuchando tu voz |
| Pulso fuerte + waveform animado | SPEAKING — está hablando |
| Anillo rotando lento | THINKING — procesando |
| Cruz/scanner activo | PROCESSING — ejecutando una herramienta |
| Tinte rojo | MUTED — micrófono apagado |

Si colocas un archivo `face.png` (cuadrado) en la raíz del proyecto, lo usará como rostro central. Es opcional — sin él el HUD funciona igual.

### Panel derecho
- **Activity Log** — historial de lo que dijo, hizo y los resultados de cada comando.
- **Zona de archivos** — arrastra y suelta un archivo (PDF, imagen, código, video, audio, etc.) para que el asistente lo analice.
- **Entrada de texto** — escribe un comando y pulsa Enter (alternativa al micrófono).
- **MIC ACTIVE/MUTED** — botón para silenciar/activar micrófono.
- **⛶** — pantalla completa.

### Atajos de teclado

| Tecla | Acción |
|---|---|
| F4 | Silenciar / activar micrófono |
| F11 | Pantalla completa on/off |
| Enter (en input) | Enviar comando de texto |

---

## 5. Cómo hablar con MARK XXXIX

No hay palabra de activación tipo "Hey Jarvis". Mientras el micrófono esté activo (verde), el asistente escucha continuamente. Habla con naturalidad, en cualquier idioma — detecta el idioma automáticamente.

**Buenas prácticas:**
- Habla claro pero natural; no necesitas pausas robóticas.
- Si el ambiente es ruidoso, usa **F4** para silenciarlo entre comandos.
- Para tareas largas (varios pasos), explica el objetivo completo de una vez: el planificador descompone la tarea internamente.
- Si lo escribiste por error y quieres cancelar, di "cancelar" o pulsa Ctrl+C en la consola.

---

## 6. Capacidades — qué le puedes pedir

A continuación, las 17 herramientas reales del asistente con frases de ejemplo. Las frases son ejemplos en español; el asistente entiende cualquier idioma.

### 6.1 Aplicaciones — `open_app`
Abre programas, sitios web o servicios.
- "abre Chrome"
- "lanza Discord"
- "inicia Spotify"
- "abre el explorador de archivos"
- "abre youtube.com"

### 6.2 Control del navegador — `browser_control`
Navegación web automatizada (clics, formularios, scroll). Usa Playwright internamente.
- "busca en Google el precio del Bitcoin"
- "haz clic en el botón de iniciar sesión"
- "rellena este formulario con mi correo"
- "baja al final de la página"

### 6.3 Búsqueda web — `web_search`
Búsqueda con Google Search Grounding (resultados con citas) o DuckDuckGo como respaldo.
- "busca el precio del Bitcoin"
- "compara iPhone 15 vs Samsung S24"
- "encuentra reseñas del último Tesla"

### 6.4 Clima — `weather_report`
Reporte del clima por ciudad.
- "qué clima hace en Madrid"
- "va a llover mañana en Bogotá"
- "temperatura actual en Lima"

### 6.5 Mensajería — `send_message`
Envía mensajes por WhatsApp, Telegram u otras plataformas.
- "manda un WhatsApp a Juan diciendo que llegaré tarde"
- "envía un Telegram al grupo de la oficina"

### 6.6 Recordatorios — `reminder`
Programa recordatorios usando el Programador de Tareas de Windows. **(Solo Windows.)**
- "recuérdame a las 3 pm llamar a mi mamá"
- "ponme un recordatorio mañana a las 9 am"

### 6.7 YouTube — `youtube_video`
Reproduce, resume o investiga videos.
- "pon música relajante en YouTube"
- "resume este video"
- "muéstrame los videos en tendencia en España"

### 6.8 Visión — `screen_processor`
Captura y analiza tu pantalla o cámara web.
- "qué hay en mi pantalla"
- "mira mi cámara web"
- "lee este captura de pantalla"
- "describe el error que se ve"

### 6.9 Configuración del sistema — `computer_settings`
Volumen, brillo, ventanas, atajos, modo oscuro, WiFi, apagar, bloquear.
- "sube el volumen al 80%"
- "pon el brillo al 50%"
- "bloquea la computadora"
- "activa modo oscuro"
- "apaga el WiFi"
- "minimiza todas las ventanas"

### 6.10 Escritorio — `desktop_control`
Fondo de pantalla, organización del escritorio.
- "pon esta imagen como fondo de pantalla"
- "organiza mi escritorio"
- "descarga este wallpaper de internet y úsalo"

### 6.11 Archivos — `file_controller`
Listar, crear, leer, escribir, borrar, mover, copiar, renombrar, buscar archivos; uso de disco.
- "lista los archivos del escritorio"
- "crea un archivo llamado notas.txt"
- "encuentra todos los PDFs"
- "borra los archivos temporales"
- "cuánto espacio queda en el disco C"

### 6.12 Control directo de la PC — `computer_control`
Tipear, clic, mouse, atajos de teclado, capturar pantalla, encontrar elementos visuales en pantalla.
- "haz clic en las coordenadas 500, 300"
- "escribe este texto"
- "presiona Ctrl+C"
- "toma una captura de pantalla"
- "haz clic en el botón que dice Guardar"

### 6.13 Asistente de código — `code_helper`
Escribir, editar, explicar, ejecutar, depurar código en cualquier lenguaje.
- "escribe un script en Python para leer un CSV"
- "explícame este código"
- "ejecuta este archivo Python"
- "arregla este bug"

### 6.14 Generador de proyectos — `dev_agent`
Crea proyectos completos de varios archivos, instala dependencias, abre VS Code y corrige errores en bucle.
- "créame un web scraper para X"
- "haz un proyecto Python que haga Y"
- "construye una app sencilla en React que muestre el clima"

### 6.15 Juegos — `game_updater`
**Único punto de contacto con Steam y Epic Games:** instalar, actualizar, listar, ver descargas, programar actualizaciones.
- "actualiza mis juegos de Steam"
- "instala PUBG desde Steam"
- "está descargando Fortnite ya?"
- "programa la actualización a las 3 am"

### 6.16 Vuelos — `flight_finder`
Busca vuelos en Google Flights y te dice las mejores opciones por voz.
- "busca vuelos de Bogotá a Madrid el 20 de diciembre"
- "muéstrame vuelos en clase business a Nueva York"

### 6.17 Procesador de archivos — `file_processor`
Analiza el archivo cargado por drag-and-drop:
- **Imágenes:** describir, OCR, redimensionar
- **PDF / Word / PPT:** resumir, extraer texto
- **Código:** explicar, refactorizar
- **Audio / Video:** transcribir, convertir
- **Datos (CSV, JSON):** analizar
- **Archivos comprimidos:** listar, descomprimir

Frases:
- "describe esta imagen"
- "extrae el texto de este PDF"
- "convierte este video a MP3"
- "analiza este CSV"

---

## 7. Memoria a largo plazo

MARK XXXIX recuerda información personal entre sesiones, guardada en [memory/long_term.json](../memory/). Categorías:

| Categoría | Ejemplos |
|---|---|
| **identity** | Tu nombre, edad, profesión |
| **preferences** | Comida favorita, géneros musicales, marcas |
| **projects** | Proyectos activos en los que trabajas |
| **relationships** | Familia, amigos, colegas |
| **wishes** | Sueños, metas, viajes deseados |
| **notes** | Notas personalizadas |

**Cómo se actualiza:** cuando dices algo como "soy desarrollador" o "me gusta el café sin azúcar", el asistente decide guardarlo automáticamente. También puedes pedirle explícitamente: "recuerda que mi hermana se llama Ana".

**Límites:** máximo 2200 caracteres totales y 380 caracteres por entrada (el sistema trunca lo más antiguo si se llena).

**Para borrar todo:** elimina el archivo `memory/long_term.json` y reinicia.

---

## 8. Cargar archivos

1. Arrastra el archivo a la zona "Drop file" del panel derecho (o haz clic para examinar).
2. La zona muestra el icono, nombre, tamaño y ruta del archivo.
3. Habla o escribe lo que quieres hacer con él: "resume este PDF", "extrae texto", "analiza estos datos".
4. El asistente usa la herramienta `file_processor` con el archivo en contexto.

Tipos soportados: imágenes (PNG, JPG, etc.), video, audio, PDF, documentos (DOCX, PPTX, XLSX), código (.py, .js, .ts...), datos (CSV, JSON), archivos comprimidos (ZIP, RAR).

---

## 9. Tareas multi-paso (el agente)

Para tareas largas, MARK XXXIX usa un **planificador interno**:

1. **Plan:** descompone tu objetivo en hasta 5 pasos.
2. **Ejecución:** corre los pasos uno a uno, encadenando resultados.
3. **Recuperación:** si un paso falla, decide automáticamente entre **REINTENTAR**, **SALTAR**, **REPLANIFICAR** o **ABORTAR**. Hasta 3 reintentos por paso y 2 replanificaciones totales.

Ejemplo: "Abre Chrome, busca el precio del Bitcoin, y guárdalo en un archivo en el escritorio."
- Paso 1: `open_app(Chrome)`
- Paso 2: `web_search("precio bitcoin")`
- Paso 3: `file_controller(create, desktop/bitcoin.txt, contenido del paso 2)`

Verás cada paso en el log de actividad.

---

## 10. Solución de problemas

| Problema | Causa probable | Solución |
|---|---|---|
| No abre la ventana | Python equivocado | Usa `.\.venv\Scripts\python.exe main.py`, no `python` directamente |
| "API key invalid" | Clave caducada o mal pegada | Edita [config/api_keys.json](../config/) o bórralo y vuelve a abrir |
| No escucha voz | Mic muteado o no detectado | F4 para activar; revisa permisos de micrófono en Windows |
| No se oye respuesta | Volumen del SO al 0 / dispositivo equivocado | Cambia salida de audio en config del SO |
| `ModuleNotFoundError: pycaw` | Falta lib específica de OS | `pip install <módulo>` dentro del venv |
| Playwright no abre browser | Navegadores no instalados | `python -m playwright install` |
| Errores de red constantes | Sin internet o API caída | Revisa conexión y status de Gemini |
| Se queda "THINKING" eterno | Modelo saturado | Espera 30s; si persiste, reinicia |
| Reconexión cada 3s | Token o cuota agotada | Revisa cuota en Google AI Studio |

**Reinicio limpio:** cierra la ventana, espera 5 segundos y vuelve a ejecutar `main.py`.

---

## 11. Limitaciones conocidas

- Algunas herramientas (volumen con `pycaw`, recordatorios con Programador de Tareas) **solo funcionan en Windows**.
- El modelo de voz nativo es **preview** — puede tener latencia o cortes ocasionales.
- Las cuotas gratuitas de Gemini son generosas pero finitas; si haces uso intensivo, considera plan de pago.
- El asistente puede **ejecutar acciones reales** en tu PC (borrar archivos, abrir URLs, escribir código). Revisa antes de aprobar tareas críticas.
- No hay confirmación antes de acciones destructivas — el modelo decide.

---

## 12. Licencia

Uso personal y no comercial únicamente. Licencia [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

Creador: [@FatihMakes](https://www.youtube.com/@FatihMakes) — repo original: https://github.com/FatihMakes/Mark-XXXIX

Para configuración avanzada (modelos, voz, prompts, paths), consulta [MANUAL_CONFIGURACION.md](MANUAL_CONFIGURACION.md).
