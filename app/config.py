'''
Author: Ayemhenre Isikhuemhen
Date: 2026-10-18
LastEditors: AI

***TEMPORARY FILE/SETUP FOR DEMO***

File Description: Stores shared configurations values: file paths, model location, and App variables.
'''

"""Settings and file locations."""
# Imports
from pathlib import Path
from platformdirs import user_data_dir

# Models are brought into and live in the user directory
MODEL_DIR = Path(user_data_dir("KokoroTTS", appauthor=False)) / "models"
MODEL_FILE = MODEL_DIR / "kokoro-v1.0.onnx"
VOICES_FILE = MODEL_DIR / "voices-v1.0.bin"

# Download Kokoro on first ever startup.
BASE_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"

# Model Variables
VOICE = "af_heart"
SPEED = 1.0
LANGUAGE = "en-us"