from operator import attrgetter
from threading import Thread

IS_WINDOWS = True

try:
    from .x_input import XInputJoystick
except AttributeError:
    IS_WINDOWS = False


class Manipulator(Thread):
    def __init__(self):
        Thread.__init__(self)
        # Joystick Setup
        if not IS_WINDOWS:
            return

        joysticks = XInputJoystick.enumerate_devices()
        device_numbers = list(map(attrgetter("device_number"), joysticks))
        print(f"found {len(joysticks)} devices: {device_numbers}")
        if not joysticks:
            print("no joysticks available")
            return
        self.joystick = joysticks[0]
        print(f"using {self.joystick.device_number}")
        battery = self.joystick.get_battery_information()
        print(battery)

    def run(self):

        if not IS_WINDOWS:
            return

        if not self.joystick:
            return

        @self.joystick.event
        def on_button(button, pressed):
            print("button", button, pressed)

        @self.joystick.event
        def on_axis(axis, value):
            left_speed = 0
            right_speed = 0
            print("axis", axis, value)
            if axis == "left_trigger":
                left_speed = value
            elif axis == "right_trigger":
                right_speed = value
            self.joystick.set_vibration(left_speed, right_speed)

        while True:
            self.joystick.dispatch_events()