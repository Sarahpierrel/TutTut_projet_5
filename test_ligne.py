import cv2  
import sys  
from hand_coded_lane_follower import HandCodedLaneFollower  

# Définition de la fonction pour sauvegarder les images
def save_image(video_file):
    #suivre les lignes
    lane_follower = HandCodedLaneFollower()
    # Ouverture du fichier vidéo
    cap = cv2.VideoCapture(video_file + '.avi')

    try:
        i = 0  # Initialisation d'un compteur
        # Boucle pour lire chaque image de la video :
        while cap.isOpened():
            
            _, frame = cap.read()  # Lecture de l'image de la vidéo
            lane_follower.follow_lane(frame)  # Suivre la ligne dans l'image (fonction Gwen)
            # Enregistrement de l'image 
            cv2.imwrite("%s_%03d_%03d.png" % (video_file, i, lane_follower.curr_steering_angle), frame)
            i += 1  # Incrémentation du compteur pour nommer les images
            
            # taper 'q' pour sortir de la boucle
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()  # Libération de la vidéo
        cv2.destroyAllWindows()  # Fermeture de toutes les fenêtres OpenCV


if __name__ == '__main__':
    save_image(sys.argv[1])


