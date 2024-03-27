#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:01:06 2024

@author: louisepoteau
"""
from ultralytics import YOLO
import cv2

import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2

"""
We trained the model with YOLOV8 before and we just used the results now
model = YOLO('best.pt') 

Load video
VideoPath = './test.mp4'

"""



def detection(VideoPath, Model):

    # Créer une instance de la caméra et configurer la résolution
    cap = cv2.VideoCapture(1)
    #cap = Picamera2()
    cap.resolution = (640, 480)
    
    
    # Créer un encodeur et un fichier de sortie pour l'enregistrement vidéo
    encoder = H264Encoder(10000000)  # 10 Mbps
    output = FileOutput("test123.h264")
    
    # Configurer la prévisualisation de la caméra
    cap.configure(cap.create_preview_configuration())
    app = QApplication([])
    qpicamera2 = QGlPicamera2(cap, width=640, height=480, keep_ar=False)
    qpicamera2.setWindowTitle("Qt Picamera2 App")
    
    # Démarrer l'enregistrement vidéo
    cap.start_recording(encoder, output)
    
    # Afficher la fenêtre de prévisualisation
    qpicamera2.show()
    app.exec()
    
    cap1 = cv2.VideoCapture(1)
    
    Switch = True 
    # read frames
    
    while Switch:
        Switch, Frame = cap.read(cap)
        if Switch:

            #Track objects
            #Model.track is a YOLOV8 module
            results = Model.track(Frame, persist=True)
            
            #Plot results
            AnnotedFrame = results[0].plot()

            #Visualize
            cv2.imshow('frame', AnnotedFrame)
            
            #If q is taped, the window will shut down
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
            

    # Arrêter l'enregistrement vidéo
    cap.stop_recording()

detection('./test4.mp4', YOLO('best.pt'))
