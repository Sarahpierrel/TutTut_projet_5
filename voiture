import logging
import cv2
import datetime
import serial
import struct
from time import sleep
from hand_coded_lane_follower import HandCodedLaneFollower
from panneaux import panneaux
from range import findHSVRange

_SHOW_IMAGE = True

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

class LittleBerryCar(object):

    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320 #176        160         352
    __SCREEN_HEIGHT = 240 #144        120         288
    __SPEED_TURNING = 100


    def __init__(self):
        """ Init camera """
        logging.info('Starting LittleBerryCar')

        logging.debug('Set up camera')
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)

        self.lane_follower = HandCodedLaneFollower(self)
       
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.video_orig = self.create_video_recorder('../data/tmp/car_video%s.avi' % datestr)
        self.video_lane = self.create_video_recorder('../data/tmp/car_video_lane%s.avi' % datestr)

        """ Init speed """
        logging.debug('Setup Speed')
        self.speedTurning = self.__SPEED_TURNING
        self.speed = self.__INITIAL_SPEED

    def create_video_recorder(self, path):
        return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        ser.write(struct.pack('>B', 0))
        self.camera.release()
        self.video_orig.release()
        self.video_lane.release()
        cv2.destroyAllWindows()

    def drive(self, speed=__INITIAL_SPEED):
        """ Main entry point of the car, and put it in drive mode"""

        logging.info('Starting to drive at speed %s...' % speed)
        i = 0
        while self.camera.isOpened():
            _, image_lane = self.camera.read()
            img, ret = panneaux(self.camera)
            i+=1
            print(i)
            if(ret and i >50):
                i=0
                show_image('Panneaux', img)
                ser.write(struct.pack('>B', 0))
                line = ser.readline().decode('utf-8').rstrip()
                sleep(3)
                cv2.destroyAllWindows()
            #findHSVRange(self.camera)
            self.video_orig.write(image_lane)
            image_lane = self.follow_lane(image_lane)
            self.video_lane.write(image_lane)
            show_image('Lane Lines', image_lane)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break

    def follow_lane(self, image):
        image = self.lane_follower.follow_lane(image)
        return image


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


def main():
    with LittleBerryCar() as car:
        car.drive(100)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    
    main()
