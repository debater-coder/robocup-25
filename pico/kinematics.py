"""
# Citations:
https://research.ijcaonline.org/volume113/number3/pxc3901586.pdf
https://ecam-eurobot.github.io/Tutorials/mechanical/mecanum.html

# Components
inverse kinematics: determine motor speeds necessary for desired movement
PID control loop: use encoder input to keep motor speeds close to calculated speeds
forward kinematics (pose estimator): use encoder input to determine current chassis movement
odometry: integrate forward kinematics results over time to obtain displacement (odom transform)
"""
from feedback import MotorFeedback

LX = 0.05  # half-length X between wheels
LY = 0.05  # half-length Y between wheels
R = 0.024  # radius of wheels

def inverse_kinematics(vx: float, vy: float, w: float):
    rotation = (LX + LY) * w
    return (
        1/R * (vx - vy - rotation),
        1/R * (vx + vy + rotation),
        1/R * (vx + vy - rotation),
        1/R * (vx - vy + rotation),
    )

def forwards_kinematics(w1: float, w2: float, w3: float, w4: float):
    return (
        (w1 + w2 + w3 + w4) * R/4,
        (-w1 + w2 + w3 - w4) * R/4,
        (-w1 + w2 - w3 + w4) * R/(4 * (LX + LY)),
    )


class Kinematics:
    def __init__(self):
        self.rr = MotorFeedback(6, 7, 11)
        self.fl = MotorFeedback(4, 5, 19, reverse=True)
        self.rl = MotorFeedback(8, 9, 13, reverse=True)
        self.fr = MotorFeedback(2, 3, 21)
        self.motors = [self.fl, self.fr, self.rl, self.rr]

    def update(self):
        for motor in self.motors:
            motor.update()

        # TODO: send odom to host

    def set_speed(self, vx: float, vy: float, w: float):
        for motor, speed in zip(self.motors, inverse_kinematics(vx, vy, w)):
            motor.set_speed(speed)
