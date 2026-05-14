"""
Abre el perfil de Chrome que usa JARVIS (.jarvis_profiles/chrome) para que
inicies sesión en tus cuentas (Google, etc). Las cookies y el login quedan
guardados en ese perfil — JARVIS los reusará a partir de ahí.

Uso:
    .\.venv\Scripts\python.exe scripts\setup_chrome_profile.py

Cierra la ventana cuando termines de iniciar sesión. Eso es todo.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE_DIR = Path.home() / ".jarvis_profiles" / "chrome"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

print(f"[Setup] Perfil JARVIS: {PROFILE_DIR}")
print("[Setup] Abriendo Chrome con el perfil de JARVIS...")
print("[Setup] Inicia sesión en Google (y otros sitios) y cierra la ventana cuando termines.\n")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        str(PROFILE_DIR),
        channel="chrome",
        headless=False,
        no_viewport=True,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--disable-default-apps",
            "--no-default-browser-check",
        ],
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://accounts.google.com/")

    # Bloquea hasta que el usuario cierre la última pestaña/ventana.
    print("[Setup] Esperando a que cierres la ventana...")
    try:
        while ctx.pages:
            ctx.pages[0].wait_for_event("close", timeout=0)
    except Exception:
        pass

print("\n[Setup] ✅ Listo. Las cookies se guardaron en el perfil de JARVIS.")
print("[Setup] La próxima vez que JARVIS abra Chrome, ya estarás logueado.")
