#!/bin/bash


if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run this script with sudo: sudo bash install.sh"
  exit 1
fi

echo "[+] Hello-There is processing...."

cp hellothere.py /usr/local/bin/hellothere


chmod +x /usr/local/bin/hellothere

if command -v dos2unix &> /dev/null; then
    dos2unix /usr/local/bin/hellothere
fi

echo "[+] Installation complete! You can now run it by typing 'hellothere' from anywhere."
