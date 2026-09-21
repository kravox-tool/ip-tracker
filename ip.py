import os
import sys

# Ejecuta el script principal desde la raíz de forma limpia
ruta_app = os.path.join("core", "app.py")

if not os.path.exists(ruta_app):
    print("\033[1;31m[-] Error: No se encuentra 'core/app.py'. Asegúrate de estar en la carpeta raíz del proyecto.\033[0m")
    sys.exit(1)

print("\033[1;32m[*] Iniciando panel IP Logger...\033[0m")
os.system(f"python {ruta_app}")
