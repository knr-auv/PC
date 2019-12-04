from realtime_plot import RealtimePlotter
import numpy as np
import random
from time import sleep
from client import *
import threading

IP_ADDRESS = '10.42.0.158'
PORT = 8200

# yticks=[(-180, 0, +180), (-180, 0, +180), (-180, 0, +180)],

class RotatePlotter(RealtimePlotter):

    def __init__(self, ip, port):
        RealtimePlotter.__init__(self, [(-15, +15), (-15, +15), (-15, +15)],
                                 show_yvals=True,
                                 window_name='RotatePlot',
                                 styles=[('r--', 'b-'), ('r--', 'b-'), ('r--', 'b-')],
                                 ylabels=['roll', 'pitch', 'yaw'])
        self.output_roll = 0
        self.output_pitch = 0
        self.output_yaw = 0

        self.input_roll = 0
        self.input_pitch = 0
        self.input_yaw = 0

        self.client = Client(ip, port)
        self.flag = self.client.flag
        self.data_frame = []

    def get_values(self):
        return self.output_roll, self.input_roll, self.output_pitch, self.input_pitch, self.output_yaw, \
                        self.input_yaw

    def set_values(self, data_frame):

        # self.output_roll = random.randint(-180, 180)
        # self.output_pitch = random.randint(-180, 180)
        # self.output_yaw = random.randint(-180, 180)

        # self.input_roll = random.randint(-180, 180)
        # self.input_pitch = random.randint(-180, 180)
        # self.input_yaw = random.randint(-180, 180)

        if len(self.data_frame) == 6:
            self.output_roll = data_frame[0]
            self.output_pitch = data_frame[1]
            self.output_yaw = data_frame[2]

            self.input_roll = data_frame[3]
            self.input_pitch = data_frame[4]
            self.input_yaw = data_frame[5]



    def update(self):
        while True:
            self.data_frame = self.client.receiveData()
            print(self.data_frame)
            self.set_values(self.data_frame )


    def get_data_frame(self):
        return self.data_frame


if __name__ == '__main__':
    import threading

    plotter = RotatePlotter(IP_ADDRESS, PORT)

    thread = threading.Thread(target=plotter.update)
    thread.daemon = True
    thread.start()

    plotter.start()

