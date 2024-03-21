import cv2
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2

def main():
    # Créer une instance de la caméra et configurer la résolution
    camera = Picamera2()
    camera.resolution = (640, 480)

    # Créer un encodeur et un fichier de sortie pour l'enregistrement vidéo
    encoder = H264Encoder(10000000)  # 10 Mbps
    output = FileOutput("test123.h264")

    # Configurer la prévisualisation de la caméra
    camera.configure(camera.create_preview_configuration())
    app = QApplication([])
    qpicamera2 = QGlPicamera2(camera, width=800, height=600, keep_ar=False)
    qpicamera2.setWindowTitle("Qt Picamera2 App")

    # Démarrer l'enregistrement vidéo
    camera.start_recording(encoder, output)

    # Afficher la fenêtre de prévisualisation
    qpicamera2.show()
    app.exec()

    # Attendre 10 secondes
    time.sleep(10)

    # Arrêter l'enregistrement vidéo
    camera.stop_recording()

if __name__ == '__main__':
    main()
