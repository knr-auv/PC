from threading import Thread
from time import sleep

from inputs import get_gamepad


class PadSteering(Thread):
    """Collect input from the gamepad connected to PC,
    convert it into the output used to steer the robot"""

    def __init__(self):
        """Initialization of the gamepad"""
        # thread init
        Thread.__init__(self)
        # initialization of all used values.
        self.input = [0, 0, 0, 0, 0]
        self.output = [0, 0, 0, 0, 0]
        # Deadzone is the part of axis that we take as a 0 to reduce noise remaining after releasing analog stick
        self.deadzone = 0.
        # Left and right are analogs. Horizontal is x-axis, Vertical is y-axis.
        self.left_vertical = self.left_horizontal = self.right_vertical = self.right_horizontal = 0
        self.left_trigger = self.right_trigger = self.trigger_value = self.trigger_steering = 0

    def run(self):
        # Main loop for catching and processing input into output
        while True:
            events = get_gamepad()
            for event in events:
                self.catch_input(event)
            # self.print_input() # - Use somewhere between catch_input end of the loop for debbugging processed input
            # Processing input before final conversion into output
            self.convert_range()
            self.set_deadzone(0.1)
            self.apply_deadzone()
            # Converting into output
            self.convert_to_output()

    def catch_input(self, event):
        """Function used to catch needed input from gamepad.
        Anolog values range <-32768, 32767>.
        Left and right triggers values range <0, 255>, so trigger is in between <-255, 255>"""
        if event.code == "ABS_X":
            self.left_horizontal = event.state
        if event.code == "ABS_Y":
            self.left_vertical = event.state
        if event.code == "ABS_RX":
            self.right_horizontal = event.state
        if event.code == "ABS_RY":
            self.right_vertical = event.state
        if event.code == "ABS_Z":
            self.left_trigger = event.state
        if event.code == "ABS_RZ":
            self.right_trigger = event.state
        self.input = [self.left_horizontal, self.left_vertical, self.right_horizontal, self.right_vertical, self.right_trigger - self.left_trigger]

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def print_input(self):
        print(self.input)

    def set_deadzone(self, deadzone):
        """Deadzone for xbox one controller should be in range <0,06, 0,1>"""
        self.deadzone = deadzone

    def apply_deadzone(self):
        for i in range(0, 5, 1):
            if abs(self.input[i]) < self.deadzone:
                self.input[i] = 0

    def convert_range(self):
        """Used to convert every value into range <-1, 1>"""
        for i in range(0, 4):
            if self.input[i] > 0:
                self.input[i] /= 32767
            else:
                self.input[i] /= 32768
        self.input[4] /= 255

    def set_trigger(self, trigger_val):
        self.output[4] = trigger_val

    def convert_to_output(self):
        """Converting input into motors duty or PID offsets"""
        # Converting left analog stick input into vertical motors duty
        throttle = 1000 * self.input[1]
        motor_factor = self.input[0]
        if motor_factor >= 0:
            left_motor_duty = throttle
            right_motor_duty = throttle*(1-motor_factor)
        else:
            left_motor_duty = throttle * (1 - abs(motor_factor))
            right_motor_duty = throttle
        # Converting right analog stick input into two axes offsets
        right_horizontal_steering = int(self.input[2]*180)
        right_vertical_steering = int(self.input[3]*180)
        right_horizontal_diff = right_horizontal_steering - self.output[2]
        if abs(right_horizontal_diff) > 3:
            right_horizontal_steering = int(right_horizontal_steering - (0.95*right_horizontal_diff))
        if 160 <= right_horizontal_steering < 180:
            right_horizontal_steering += 1
        elif -160 >= right_horizontal_steering > -180:
            right_horizontal_steering -= 1
        right_vertical_diff = right_vertical_steering - self.output[3]
        if abs(right_vertical_diff) > 3:
            right_vertical_steering = int(right_vertical_steering - (0.95*right_vertical_diff))
        if 160 <= right_vertical_steering < 180:
            right_vertical_steering += 1
        elif -160 >= right_vertical_steering > -180:
            right_vertical_steering -= 1
        horizontal_steering = int(1000 * self.input[4]) # depth meter not working
        self.output[0] = int(left_motor_duty)
        self.output[1] = int(right_motor_duty)
        self.output[2] = right_horizontal_steering
        self.output[3] = right_vertical_steering
        self.output[4] = horizontal_steering # depth meter not working


class TriggerThread(Thread):
    """class used to change offset on depth"""
    def __init__(self, given_pad):
        self.pad = given_pad
        self.trigger_val = 0
        Thread.__init__(self)

    def run(self):
        while True:
            self.trigger_val += (self.pad.right_trigger - self.pad.left_trigger)/255
            sleep(0.05)
            self.pad.set_trigger(int(self.trigger_val))


if __name__ == "__main__":
    pad = PadSteering()
    pad.start()
    # trigger_thread = TriggerThread(pad) # depth meter not working
    # trigger_thread.start() # depth meter not working
    while True:
        print(pad.get_output())
