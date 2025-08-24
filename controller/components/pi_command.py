import numpy as np
import time
from gpiozero import PhaseEnableMotor

MAXSPEED = 0.060288

LX = 0.05  # half-length X between wheels
LY = 0.05  # half-length Y between wheels


def inverse_kinematics(vx: float, vy: float, w: float):
    rotation = (LX + LY) * w
    return (
        (vx - vy - rotation),
        (vx + vy + rotation),
        (vx + vy - rotation),
        (vx - vy + rotation),
    )


def forwards_kinematics(w1: float, w2: float, w3: float, w4: float):
    return (
        (w1 + w2 + w3 + w4) / 4,
        (-w1 + w2 + w3 - w4) / 4,
        (-w1 + w2 - w3 + w4) / (4 * (LX + LY)),
    )


class PiCommand:
    def __init__(self) -> None:
        self.odom = np.array([0.0, 0.0, 0.0])
        self.vx = 0
        self.vy = 0
        self.vw = 0
        self.last_time = time.time()

        self.rl = PhaseEnableMotor(17, 4, pwm=True)
        self.fl = PhaseEnableMotor(22, 27, pwm=True)
        self.rr = PhaseEnableMotor(9, 10, pwm=True)
        self.fr = PhaseEnableMotor(11, 5, pwm=True)

        self.motors = [self.fl, self.fr, self.rl, self.rr]

    def send_command(self, vx: float, vy: float, vw: float):
        self.vx = min(MAXSPEED, max(-MAXSPEED, vx / MAXSPEED))
        self.vy = min(MAXSPEED, max(-MAXSPEED, vy / MAXSPEED))
        self.vw = min(MAXSPEED, max(-MAXSPEED, vw / MAXSPEED))

        for motor, speed in zip(
            self.motors, inverse_kinematics(self.vx, self.vy, self.vw)
        ):
            motor.speed(speed)

    def get_odometry(self):
        elapsed = time.time() - self.last_time
        self.last_time = time.time()

        self.odom += elapsed * np.array([self.vx, self.vy, self.vw])

        return tuple(self.odom)
