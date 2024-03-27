import cv2
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput


from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2

def main():
        #stream = BytesIO
        camera = Picamera2()
        camera.resolution = (640,480)
        #camera.start_preview()
    
    
    
    
        camera.configure(camera.create_preview_configuration())
        app = QApplication([])
        qpicamera2 = QGlPicamera2(camera, width=800, height=600, keep_ar=False)
        qpicamera2.setWindowTitle("Qt Picamera2 App")
        camera.start()
        qpicamera2.show()
        app.exec()
    
    

        
        encoder = H264Encoder(100000000)
        output = FileOutput("test123.h264")
        camera.start_recording(encoder,output)


        time.sleep(10)
        camera.stop_recording()
        #camera.stop_preview()


            
if __name__ == '__main__':
    main()




