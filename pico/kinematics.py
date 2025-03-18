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
from Makerverse_Motor_2ch import motor
import time
import micropython

micropython.alloc_emergency_exception_buf(100)


class Encoder:
    """Encoder for motor. Uses only one encoder input as direction sensing was unreliable"""
    def __init__(self, c1 ):
        c1 = Pin(c1, Pin.IN, Pin.PULL_UP)
        self.c1 = c1
        self.odom = 0
        self.direction = 1

        self.c1.irq(self.irq_callback, Pin.IRQ_RISING)

    def irq_callback(self, pin: Pin):
        self.odom += self.direction

    def __str__(self) -> str:
        return str(self.odom)


encoder_rl = Encoder(11)
encoder_rr = Encoder(13)
encoder_fl = Encoder(19)
encoder_fr = Encoder(21)

while True:
    print(f"rl: {encoder_rl}, rr: {encoder_rr}, fl: {encoder_fl}, fr: {encoder_fr}")
