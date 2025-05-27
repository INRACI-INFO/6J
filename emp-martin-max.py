"""
    name : martin stordeur && maxime kapczuk 
    date : 2023-10-05
    description : Application de lecture d'empreintes digitales utilisant PyQt5 et pyfingerprint.
"""



import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from pyfingerprint.pyfingerprint import PyFingerprint

class FingerprintScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanning = False

    def init_ui(self):
        self.setWindowTitle("Lecteur d'Empreinte Digitale")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        self.status_label = QLabel("Placez votre doigt sur le capteur...", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.status_label)
        self.scan_button = QPushButton("Démarrer le Scan", self)
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; color: green;")
        layout.addWidget(self.result_label)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_dots = 0
        self.setLayout(layout)

    def start_scan(self):
        if not self.scanning:
            self.scanning = True
            self.scan_button.setEnabled(False)
            self.status_label.setText("Scan en cours")
            self.animation_timer.start(500)
            threading.Thread(target=self.scan_fingerprint).start()

    def scan_fingerprint(self):
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if not f.verifyPassword():
                raise ValueError("Le capteur d'empreinte digitale n'a pas pu être initialisé.")
            while not f.readImage():
                if not self.scanning:
                    return
            f.convertImage(0x01)
            positionNumber, accuracyScore = f.searchTemplate()
            if positionNumber == -1:
                self.update_ui("Aucune correspondance trouvée.", "red")
            else:
                f.loadTemplate(positionNumber, 0x01)
                donnees_empreinte = f.downloadTemplate()
                self.update_ui(f"Empreinte trouvée (Position #{positionNumber})", "green")
                print("Données de l'empreinte digitale:", donnees_empreinte)
        except Exception as e:
            self.update_ui(f"Erreur: {str(e)}", "red")
        finally:
            self.scanning = False
            self.scan_button.setEnabled(True)
            self.animation_timer.stop()

    def update_ui(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"font-size: 16px; color: {color};")
        self.result_label.setText("Scan terminé.")

    def update_animation(self):
        self.animation_dots = (self.animation_dots + 1) % 4
        self.status_label.setText("Scan en cours" + "." * self.animation_dots)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FingerprintScannerApp()
    window.show()
    sys.exit(app.exec_())

