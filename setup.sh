#!/bin/bash

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 est requis"
    exit 1
fi

# Installation des dépendances système (pour Raspberry Pi / Debian)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pip
fi

# Création de l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances Python
pip install numpy scipy sounddevice requests

echo "Installation terminée"
