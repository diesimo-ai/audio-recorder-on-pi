# POC Audio Recorder

POC d'enregistrement audio sur Raspberry Pi avec simulation de transfert cloud.

## Démarrage rapide

```bash
# Rendre les scripts éxucutables
chmod +x setup.sh run.sh

# Installation
./setup.sh

# Mode normal
./run.sh

# Mode simulation
./run.sh --simulate
```

## Prérequis

- Python 3.8+
- PortAudio
- Microphone (USB ou compatible)
- Connexion 4G (ou simulation)

## Configuration

Paramètres principaux (`poc_audio.py`):
```python
SAMPLE_RATE = 16000
CHANNELS = 1
SEGMENT_DURATION = 60  # secondes
```

## Structure

```
.
├── poc_audio.py     # Script principal
├── setup.sh         # Installation des dépendances
├── run.sh           # Script de lancement
├── cloud_sim/       # Stockage des fichiers simulés
└── *.log           # Fichiers de logs
```

## Fonctionnalités

- Enregistrement audio segmenté (1 minute par segment)
- Vérification de connectivité réseau
- Simulation de transfert cloud
- Logs détaillés
- Mode simulation pour tests

## En développement

- Gestion basique des erreurs et reconnexions
- Transfert cloud simulé par copie locale
- Mode simulation avec génération de signal

## Notes

Ce POC sert de base de discussion pour:
- Validation de la faisabilité
- Recueil des besoins spécifiques
- Définition des prochaines étapes

## Contact

Pour toute question, suggestion ou retour, je serai ravi d’échanger avec vous.

Afonso Diela  

