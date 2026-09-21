# 🛡️ Panel Automatizado IP Logger para Termux

Herramienta automatizada en Python y Flask diseñada para Termux, utilizando túneles seguros de Cloudflare para capturar información de conexiones (IP y User-Agent) redirigiendo de forma fluida a un enlace de destino.

## 🚀 Instalación y Uso

1. Descomprime este repositorio en tu dispositivo Termux.
2. Otorga permisos de ejecución al script de instalación:
   ```bash
   chmod +x scripts/setup.sh
   ```
3. Ejecuta el instalador para configurar las dependencias:
   ```bash
   bash scripts/setup.sh
   ```
4. Inicia la aplicación ejecutando directamente:
   ```bash
   python ip.py
   ```
