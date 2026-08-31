#!/bin/bash

# Root (sudo) yetkisi kontrolü
if [ "$EUID" -ne 0 ]; then
  echo "[-] Please execute this with sudo: sudo bash install.sh"
  exit 1
fi

echo "[+] Hello-There installing..."

cp hellothere.py /usr/local/bin/hellothere
chmod +x /usr/local/bin/hellothere

echo "[+] Installation complete! You can now run it by typing 'hellothere' from anywhere."
