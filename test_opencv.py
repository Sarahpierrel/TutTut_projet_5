import cv2  

def main():
    camera = cv2.VideoCapture(-1)  # Initialisation de la caméra
    camera.set(3, 640)  # Définition de la largeur de l'image
    camera.set(4, 480)  # Définition de la hauteur de l'image

    while camera.isOpened():  # Boucle pour lire chaque image
        _, image = camera.read()  # Lecture de l'image
        cv2.imshow('Original', image)  # Affichage de la l'image originale

        #b_w_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Conversion de l'image en niveaux de gris
        #cv2.imshow('B/W', b_w_image)  # Affichage de l'image en niveaux de gris

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Attendre touche 'q' pour quitter
            break

    cv2.destroyAllWindows()  # Fermeture de toutes les fenêtres OpenCV

if __name__ == '__main__':
    main()  # Appel de la fonction principale
