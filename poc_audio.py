import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import os
import sys
import time
import shutil
import requests
import argparse
import logging
from pathlib import Path
from typing import Optional

# Paramètres globaux
SAMPLE_RATE = 16000
CHANNELS = 1
SEGMENT_DURATION = 60  # secondes (1 minute pour le POC)
CLOUD_SIM_DIR = "cloud_sim"
CHECK_URL = "https://www.google.com"  # Pour simuler la vérif 4G

# Mode Sim
parser = argparse.ArgumentParser()
parser.add_argument('--simulate', action='store_true', help="Utiliser le mode simulation")
args = parser.parse_args()
USE_SIMULATION = args.simulate

os.makedirs(CLOUD_SIM_DIR, exist_ok=True)

class AudioRecorder:
    """Gestionnaire d'enregistrement audio"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure les logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('audio_recorder.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def record_segment(self, segment_num: int) -> Optional[Path]:
        """Enregistre un segment audio avec gestion d'erreurs"""
        try:
            filename = Path(CLOUD_SIM_DIR) / f"segment_{segment_num}.wav"
            if USE_SIMULATION:
                return self._record_simulation(filename)
            return self._record_real(filename)
        except Exception as e:
            self.logger.error(f"Erreur d'enregistrement: {e}")
            return None

    def _record_real(self, filename: Path) -> Path:
        """Enregistre l'audio depuis le microphone."""
        try:
            self.logger.info("Enregistrement réel...")
            audio = sd.rec(int(SEGMENT_DURATION * SAMPLE_RATE), 
                         samplerate=SAMPLE_RATE, 
                         channels=CHANNELS, dtype='int16')
            sd.wait()
            wavfile.write(filename, SAMPLE_RATE, audio)
            self.logger.info(f"Fichier enregistré : {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Erreur lors de l'enregistrement: {str(e)}")
            raise

    def _record_simulation(self, filename: Path) -> Path:
        """Simule un enregistrement audio en générant une onde sinusoïdale."""
        try:
            self.logger.info("Simulation d'enregistrement...")
            t = np.linspace(0, SEGMENT_DURATION, 
                          int(SAMPLE_RATE * SEGMENT_DURATION), False)
            audio = 0.5 * np.sin(2 * np.pi * 440 * t)
            audio = (audio * 32767).astype(np.int16)
            wavfile.write(filename, SAMPLE_RATE, audio)
            self.logger.info(f"Fichier simulé : {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Erreur lors de la simulation: {str(e)}")
            raise

def is_connected():
    try:
        requests.get(CHECK_URL, timeout=3)
        return True
    except:
        return False

def replay_audio(filename):
    # Read the WAV file
    fs, data = wavfile.read(filename)
    logging.info(f"Lecture du fichier {filename} à {fs} Hz")
    sd.play(data, fs)
    sd.wait()
    logging.info("Lecture terminée.")

def main():
    try:
        recorder = AudioRecorder()
        
        segment_num = 1
        while segment_num <= 3:
            if not is_connected():
                logging.warning("Connexion 4G perdue, tentative de reconnexion...")
                time.sleep(5)
                continue
                
            if segment_file := recorder.record_segment(segment_num):
                segment_num += 1
                logging.info(f"Segment {segment_num} enregistré avec succès")
            else:
                logging.error(f"Échec de l'enregistrement du segment {segment_num}")
                
            time.sleep(2)
            
    except Exception as e:
        logging.error(f"Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
