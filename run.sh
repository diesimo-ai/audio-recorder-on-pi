#!/bin/bash

# Activation de l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Environnement virtuel non trouvé. Exécutez setup.sh d'abord."
    exit 1
fi

# Nettoyage des anciens logs
if [ -f "audio_recorder.log" ]; then
    mv audio_recorder.log "audio_recorder_$(date +%Y%m%d_%H%M%S).log"
fi

# Lancement du script avec les arguments passés
python poc_audio.py "$@"

# Désactivation de l'environnement virtuel
deactivate
