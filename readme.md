# 🤖 Jaris — Asistente Personal con IA

Asistente de voz multiplataforma que escucha, ve, entiende y controla tu computadora en tiempo real. Ejecución local, basado en Google Gemini.

---

## ✨ Resumen

Jaris es un asistente conversacional con voz nativa que interpreta lo que dices, analiza tu pantalla, procesa documentos y ejecuta tareas complejas. Funciona en Windows, macOS y Linux (con mejor soporte en Windows).

---

## 🚀 Capacidades

| Característica | Descripción |
|---|---|
| 🎙️ Voz en tiempo real | Conversación de baja latencia, multilenguaje |
| 🖥️ Control del sistema | Abre apps, gestiona archivos, ejecuta comandos |
| 🧩 Tareas autónomas | Planificación de objetivos multi-paso |
| 👁️ Visión | Analiza pantalla y cámara web |
| 🧠 Memoria persistente | Recuerda preferencias, proyectos y contexto |
| ⌨️ Entrada híbrida | Voz y teclado intercambiables |

### Herramientas disponibles
Búsqueda web, control de navegador (Playwright), YouTube, clima, mensajería, recordatorios, control de configuraciones del SO, gestión de archivos, escritura de código, generación de proyectos, juegos (Steam/Epic), búsqueda de vuelos, procesamiento de archivos cargados.

---

## ⚡ Instalación rápida

```bash
git clone https://github.com/oscardev2025/Jaris.git
cd Jaris
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install
python main.py
```

> En el primer arranque, la UI te pedirá tu **Gemini API key** (gratis en https://aistudio.google.com/apikey) y la guardará en `config/api_keys.json`.

---

## 📋 Requisitos

| Requisito | Detalle |
|---|---|
| SO | Windows 10/11, macOS o Linux |
| Python | 3.11 o 3.12 |
| Micrófono | Requerido para voz |
| API Key | Google Gemini (gratuita) |
| Conexión | Internet estable |

---

## 📚 Documentación

- [Manual de Usuario](docs/MANUAL_USUARIO.md) — uso diario, herramientas, atajos.
- [Manual de Configuración](docs/MANUAL_CONFIGURACION.md) — modelos, voz, prompts, paths.

---

## ⚠️ Licencia

Uso personal y no comercial únicamente — **[Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**.

---

## 🙏 Créditos

Basado en el proyecto **MARK XXXIX** de [FatihMakes](https://github.com/FatihMakes/Mark-XXXIX), licenciado bajo CC BY-NC 4.0. Esta versión incluye personalizaciones, traducciones al español y ajustes propios.
