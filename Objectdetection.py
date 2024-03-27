import cv2
import logging
import datetime
import time
import edgetpu.detection.engine
from PIL import Image
from Traffic import *

_SHOW_IMAGE = False

class ObjectsOnRoad(object):
    #Cette classe détecte les objets sur la route et contrôle la navigation de la voiture (vitesse/ direction) en conséquence

    def __init__(self,
                 car=None,
                 speed_limit=40,
                 model='/home/littleberrycar/DeepPiCar/models/object_detection/data/model_result/road_signs_quantized_edgetpu.tflite',
                 label='/home/littleberrycar/DeepPiCar/models/object_detection/data/model_result/road_sign_labels.txt',
                 width=640,
                 height=480):
        
        # model: Ce doit être un modèle tflite spécifiquement compilé pour Edge TPU.
        # https://coral.withgoogle.com/web-compiler/
        logging.info('Création d\'un objet ObjectsOnRoadProcessor...')
        self.width = width
        self.height = height

        # Initialisation de la voiture
        self.car = car
        self.speed_limit = speed_limit
        self.speed = speed_limit

        # Initialisation des modèles TensorFlow
        with open(label, 'r') as f:
            pairs = (l.strip().split(maxsplit=1) for l in f.readlines())
            self.labels = dict((int(k), v) for k, v in pairs)

        # Initialisation du moteur Edge TPU
        logging.info('Initialisation du moteur Edge TPU avec le modèle %s...' % model)
        self.engine = edgetpu.detection.engine.DetectionEngine(model)
        self.min_confidence = 0.30
        self.num_of_objects = 3
        logging.info('Initialisation du moteur Edge TPU avec le modèle terminée.')

        # Initialisation d'OpenCV pour dessiner des boîtes
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10, height - 10)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)  # blanc
        self.boxColor = (0, 0, 255)  # ROUGE
        self.boxLineWidth = 1
        self.lineType = 2
        self.annotate_text = ""
        self.annotate_text_time = time.time()
        self.time_to_show_prediction = 1.0  # ms

        # Initialisation des objets de la circulation
        self.traffic_objects = {0: SpeedLimit(25),
                                1: SpeedLimit(40),
                                2: StopSign()}

    def process_objects_on_road(self, frame):
        # Point d'entrée principal du gestionnaire d'objets sur la route
        logging.debug('Traitement des objets.................................')
        objects, final_frame = self.detect_objects(frame)
        self.control_car(objects)
        logging.debug('Traitement des objets TERMINÉ..............................')

        return final_frame



    def control_car(self, objects):
        logging.debug('Contrôle de la voiture...')
        car_state = {"speed": self.speed_limit, "speed_limit": self.speed_limit}

        if len(objects) == 0:
            logging.debug('Aucun objet détecté, conduite à la vitesse limite de %s.' % self.speed_limit)

        contain_stop_sign = False
        for obj in objects:
            obj_label = self.labels[obj.label_id]
            processor = self.traffic_objects[obj.label_id]
            if processor.is_close_by(obj, self.height):
                processor.set_car_state(car_state)
            else:
                logging.debug("[%s] objet détecté, mais il est trop loin, on ignore. " % obj_label)
            if obj_label == 'Stop':
                contain_stop_sign = True

        if not contain_stop_sign:
            self.traffic_objects[5].clear()

        self.resume_driving(car_state)



    def resume_driving(self, car_state):
        old_speed = self.speed
        self.speed_limit = car_state['speed_limit']
        self.speed = car_state['speed']

        if self.speed == 0:
            self.set_speed(0)
        else:
            self.set_speed(self.speed_limit)
        logging.debug('Vitesse actuelle = %d, Nouvelle vitesse = %d' % (old_speed, self.speed))

        if self.speed == 0:
            logging.debug('arrêt complet pendant 1 seconde')
            time.sleep(1)


    ############################
    # Étapes de traitement d'image
    ############################
    def detect_objects(self, frame):
        logging.debug('Détection d\'objets...')
