"""
# Citations:
https://research.ijcaonline.org/volume113/number3/pxc3901586.pdf
https://ecam-eurobot.github.io/Tutorials/mechanical/mecanum.html

# Components
inverse kinematics: determine motor speeds necessary for desired movement
PID control loop: use encoder input to keep motor speeds close to calculated speeds
forwards kinematics: use encoder input to determine current chassis movement
odometry: integrate forward kinematics results over time to obtain displacement (odom transform)
"""
from machine import Pin
import time

ENCODER_STATES = [
    0, -1, 1, 0,
    1, 0, 0, -1,
    -1, 0, 0, 1,
    0, 1, -1, 0
]

class Encoder:
    def __init__(self, c1, c2):
        # Validation
        if isinstance(c1, int):
            c1 = Pin(c1, Pin.IN)
        elif isinstance(c1, Pin):
            c1.init(mode=Pin.IN)
        else:
            raise TypeError("Argument 'c1' must be an integer or Pin object")

        if isinstance(c2, int):
            c2 = Pin(c2, Pin.IN)
        elif isinstance(c2, Pin):
            c2.init(mode=Pin.IN)
        else:
            raise TypeError("Argument 'c2' must be an integer or Pin object")

        self.c1 = c1
        self.c2 = c2

        self.speed = 0
        self.prev_change = time.ticks_ms()
        self.prev_state = 0

        self.c1.irq()
        self.c1.irq()
        self.c2.irq()
        self.c2.irq()

    def irq_callback(self, pin: Pin):
        self.speed = time.ticks_diff(time.ticks_ms(), self.prev_change)
        self.prev_change = time.ticks_ms()

        # combine encoders into 1 value
        state = self.c1.value() * 2 + self.c2.value()

        # find direction
        self.speed *= ENCODER_STATES[self.prev_state * 4 + state]
        self.prev_state = state
