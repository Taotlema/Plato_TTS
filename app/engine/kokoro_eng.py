'''
Author: Ayemhenre Isikhuemhen
Date: 2026-10-18
LastEditors:
File Description: Boots up the Kokoro text to speech model.
'''

# Imports
import urllib.request
from app import config

# Kokoro Engine Class
class KokoroEngine:

    # Class Constructor
    def __init__(self):
        self._kokoro = None

    # load(): Download the model files if they are missing, then load them.
    def load(self):
        config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        for path in (config.MODEL_FILE, config.VOICES_FILE):
            if not path.exists():
                print(f"Downloading {path.name} (first run only)...")
                partial = path.with_name(path.name + ".part")
                urllib.request.urlretrieve(f"{config.BASE_URL}/{path.name}", partial)
                partial.replace(path)

        from kokoro_onnx import Kokoro

        self._kokoro = Kokoro(str(config.MODEL_FILE), str(config.VOICES_FILE))

    # synthesize: Return (samples, sample_rate) for the given text.
    def synthesize(self, text):
        return self._kokoro.create(
            text, voice=config.VOICE, speed=config.SPEED, lang=config.LANGUAGE
        )