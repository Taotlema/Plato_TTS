'''
Author: Ayemhenre Isikhuemhen
Date: 2026-10-18
LastEditors:AI

***TEMPORARY FILE/SETUP FOR DEMO***

File Description: Main application window and navigation. The effective spine for Pato's user interface.
'''

# Imports
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget
from app.audio import playback_queue
from app.engine.kokoro import KokoroEngine

# Load Worker Class: Loads the model off the main thread so the window stays responsive.
class LoadWorker(QThread):
    loaded = pyqtSignal()
    failed = pyqtSignal(str)

    # Class Constructor
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    # For the demo - checking if the model loaded and works
    def run(self):
        try:
            self.engine.load()
            self.loaded.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

# A lot of stuff I am going to restructer but used in order to demo tts

class SpeakWorker(QThread):
    spoken = pyqtSignal(object, int)
    failed = pyqtSignal(str)

    def __init__(self, engine, text):
        super().__init__()
        self.engine = engine
        self.text = text

    def run(self):
        try:
            samples, rate = self.engine.synthesize(self.text)
            self.spoken.emit(samples, rate)
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kokoro TTS")
        self.resize(600, 400)

        self.engine = KokoroEngine()
        self.speaker = None

        self.text_box = QPlainTextEdit("Hello! This is Kokoro running on my computer.")
        self.status = QLabel("Loading model (the first run downloads about 350 MB)...")
        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.on_play)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_box)
        layout.addWidget(self.status)
        layout.addWidget(self.play_button)

        self.loader = LoadWorker(self.engine)
        self.loader.loaded.connect(self.on_loaded)
        self.loader.failed.connect(self.on_load_failed)
        self.loader.start()

    def on_loaded(self):
        self.status.setText("Ready")
        self.play_button.setEnabled(True)

    def on_load_failed(self, message):
        self.status.setText("Could not load the model: " + message)

    def on_play(self):
        text = self.text_box.toPlainText().strip()
        if not text:
            self.status.setText("Type some text first.")
            return
        self.play_button.setEnabled(False)
        self.status.setText("Generating speech...")
        self.speaker = SpeakWorker(self.engine, text)
        self.speaker.spoken.connect(self.on_spoken)
        self.speaker.failed.connect(self.on_speak_failed)
        self.speaker.start()

    def on_spoken(self, samples, rate):
        playback_queue.play(samples, rate)
        self.status.setText("Playing")
        self.play_button.setEnabled(True)

    def on_speak_failed(self, message):
        self.status.setText("Error: " + message)
        self.play_button.setEnabled(True)

    def closeEvent(self, event):
        for worker in (self.loader, self.speaker):
            if worker is not None:
                worker.wait(10_000)
        playback_queue.stop()
        event.accept()