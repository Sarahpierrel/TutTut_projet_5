import logging  
import cv2  
import datetime  
import serial  
import struct  
from time import sleep  
from hand_coded_lane_follower import HandCodedLaneFollower 
from panneaux import panneaux  


_SHOW_IMAGE = True  # Variable pour afficher les images

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

class LittleBerryCar(object):
    """Classe pour contrôler LittleBerryCar"""

    __INITIAL_SPEED = 0  # Vitesse initiale du véhicule
    __SCREEN_WIDTH = 320  # Largeur de l'écran de la caméra
    __SCREEN_HEIGHT = 240  # Hauteur de l'écran de la caméra
    __SPEED_TURNING = 100  # Vitesse de virage

    def __init__(self):
        """Initialisation de LittleBerryCar"""
        logging.info('Starting LittleBerryCar')

        logging.debug('Set up camera') 
        self.camera = cv2.VideoCapture(-1)  # Initialisation de la caméra
        self.camera.set(3, self.__SCREEN_WIDTH)  # Configuration de la largeur de l'image
        self.camera.set(4, self.__SCREEN_HEIGHT)  # Configuration de la hauteur de l'image

        #self.lane_follower = HandCodedLaneFollower(self)  # Initialisation du suivi de ligne

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Initialisation du code vidéo
        datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")  # Date et heure
        self.video_orig = self.create_video_recorder('../data/tmp/car_video%s.avi' % datestr)  # Enregistreur vidéo original
        self.video_lane = self.create_video_recorder('../data/tmp/car_video_lane%s.avi' % datestr)  # Enregistreur vidéo avec line

        logging.debug('Setup Speed') 
        self.speedTurning = self.__SPEED_TURNING  # Initialisation de la vitesse de virage
        self.speed = self.__INITIAL_SPEED  # Initialisation de la vitesse

    def create_video_recorder(self, path):
        """Crée un enregistreur vidéo"""
        return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """Entrée dans une instruction 'with'"""
        return self

    def __exit__(self, _type, value, traceback):
        """Sortie d'une instruction 'with'"""
        if traceback is not None:
            # Une exception s'est produite :
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()  # Nettoyage des ressources

    def cleanup(self):
        """Réinitialise le matériel"""
        logging.info('Stopping the car, resetting hardware.') 
        ser.write(struct.pack('>B', 0))  # Envoi de 0 à Arduino pour arrêter le véhicule
        self.camera.release()  # Libération ressources caméra
        self.video_orig.release()  # Libération ressources enregistreur vidéo original
        self.video_lane.release()  # Libération ressources enregistreur vidéo ligne
        cv2.destroyAllWindows()  # Fermeture fenêtres OpenCV

    def drive(self, speed=__INITIAL_SPEED):
        """ Point d'entrée principal du véhicule, et le met en mode conduite"""
    
        logging.info('Starting to drive at speed %s...' % speed)
        i = 0  # Compteur pour la détection des panneaux
        while self.camera.isOpened():  # Tant que la caméra est allumée
            _, image_lane = self.camera.read()  # Lecture de l'image ligne
            img, ret = panneaux(self.camera)  # Détection des panneaux
            i += 1  # Incrémentation du compteur
            print(i)  # Affichage du compteur
            if ret and i > 50:  # Si un panneau est détecté et que le compteur est supérieur à 50
                i = 0  # Réinitialisation du compteur
                show_image('Panneaux', img)  # Affichage de l'image avec les panneaux détectés
                ser.write(struct.pack('>B', 0))  # Envoi de 0 à Arduino pour arrêter le véhicule
                line = ser.readline().decode('utf-8').rstrip()  # Lecture de la réponse d'Arduino
                sleep(3)  # Pause de 3 secondes
                cv2.destroyAllWindows()  # Fermeture fenêtres OpenCV
            self.video_orig.write(image_lane)  # Enregistrement de l'image originale
            image_lane = self.follow_lane(image_lane)  # Suivre la ligne
            self.video_lane.write(image_lane)  # Enregistrement de l'image ligne
            show_image('Lane Lines', image_lane)  # Affichage des lignes
    
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Si la touche 'q' est enfoncée
                self.cleanup()  # Nettoyage
                break  # Sortie de la boucle
    
def follow_lane(self, image):
        """Suivi de la voie"""
        image = self.lane_follower.follow_lane(image)  # Suivi de la ligne
        return image
    
    ############################
    # Fonctions utilitaires
    ############################
def show_image(title, frame, show=_SHOW_IMAGE):
        """Affiche une image"""
        if show:
            cv2.imshow(title, frame)
    
def main():
        """Fonction principale"""
        with LittleBerryCar() as car:  # Utilisation de la classe LittleBerryCar dans une instruction 'with'
            car.drive(100)  # Démarre la conduite à une vitesse de 100
    
if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')  # Configuration du journalisation
        main()  # Appel de la fonction principale
