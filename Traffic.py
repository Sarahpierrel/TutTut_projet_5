from threading import Timer
import logging

class TrafficObject(object):

    def is_close_by(obj, frame_height, min_height_pct=0.05):
        # Méthode pour déterminer si l'objet est proche en fonction de la hauteur de l'image
        obj_height = obj.bounding_box[1][1] - obj.bounding_box[0][1]
        return obj_height / frame_height > min_height_pct


class SpeedLimit(TrafficObject):
    def __init__(self, speed_limit):
        #Initialise la limite de vitesse.
        self.speed_limit = speed_limit

    def set_car_state(self, car_state):
        #Définit la limite de vitesse de la voiture
        logging.debug('Limite de vitesse : définir la limite à %d' % self.speed_limit)
        car_state['speed_limit'] = self.speed_limit


class StopSign(TrafficObject):
    #Classe représentant un panneau stop.

    def __init__(self, wait_time_in_sec=3, min_no_stop_sign=20):
        #Initialise les paramètres du panneau stop
        self.in_wait_mode = False
        self.has_stopped = False
        self.wait_time_in_sec = wait_time_in_sec
        self.min_no_stop_sign = min_no_stop_sign
        self.no_stop_count = min_no_stop_sign
        self.timer = None

    def set_car_state(self, car_state):
        #Définit l'état de la voiture en réponse au panneau stop
        self.no_stop_count = self.min_no_stop_sign

        if self.in_wait_mode:
            logging.debug('Panneau stop : 2) toujours en attente')
            # Attente de 2 secondes avant de continuer
            car_state['speed'] = 0
            return

        if not self.has_stopped:
            logging.debug('Panneau stop : 1) juste détecté')

            car_state['speed'] = 0
            self.in_wait_mode = True
            self.has_stopped = True
            self.timer = Timer(self.wait_time_in_sec, self.wait_done)
            self.timer.start()
            return

    def wait_done(self):
        #Méthode appelée lorsque l'attente du panneau stop est terminée.
        logging.debug('Panneau stop : 3) fin de l\'attente pendant %d secondes' % self.wait_time_in_sec)
        self.in_wait_mode = False

    def clear(self):
        #Méthode pour réinitialiser l'état du panneau stop après son passage.
        if self.has_stopped:
            # Compteur pour s'assurer que le panneau n'est plus détecté pendant un certain temps
            self.no_stop_count -= 1
            if self.no_stop_count == 0:
                logging.debug("Panneau stop : 4) aucun panneau détecté")
                self.has_stopped = False
                self.in_wait_mode = False
