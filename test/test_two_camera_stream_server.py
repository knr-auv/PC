import cv2
import time
import logging
import multiprocessing
import sys
sys.path.append('..')
import stream


class StreamProcess(multiprocessing.Process):

    def __init__(self, port, cam):
        multiprocessing.Process.__init__(self)
        self.port = port
        self.cam = cam

    def run(self):
        video = stream.StreamServer(port=self.port)
        while True:
            cv2.imshow(str(self.cam), video.recive_frame())
            cv2.waitKey(1)


logging.basicConfig(level=logging.DEBUG)

camera_stream_nr1 = StreamProcess(5050, "Stream number 1")
camera_stream_nr2 = StreamProcess(5051, "Stream number 2")
logging.debug("Creat Processes")
time.sleep(2)

camera_stream_nr1.start()
camera_stream_nr2.start()
logging.debug("Start Processes")

camera_stream_nr1.join()
camera_stream_nr2.join()
