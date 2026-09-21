#!/bin/bash
clear
echo -e "\033[1;33m[*] Iniciando instalador automático para Termux...\033[0m"
sleep 1

# Actualizar paquetes básicos
echo -e "\033[1;34m[*] Actualizando repositorios...\033[0m"
pkg update -y && pkg upgrade -y

# Instalar dependencias nativas
echo -e "\033[1;34m[*] Instalando Python y Cloudflared...\033[0m"
pkg install python cloudflared -y

# Instalar librerías de Python
echo -e "\033[1;34m[*] Instalando Flask mediante pip...\033[0m"
pip install flask

echo -e "\033[1;32m[+] ¡Configuración completada con éxito!\033[0m"
echo -e "\033[1;36m[!] Para iniciar la herramienta ejecuta: python core/app.py\033[0m"
