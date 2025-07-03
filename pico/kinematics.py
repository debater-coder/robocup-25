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
import time

lx = 0.05
ly = 0.05
r = 0.024

def inverse_kinematics(vx: float, vy: float, w: float):
    rotation = (lx + ly) * w
    return (
        1/r * (vx - vy - rotation),
        1/r * (vx + vy + rotation),
        1/r * (vx + vy - rotation),
        1/r * (vx - vy + rotation),
    )

def forwards_kinematics(w1: float, w2: float, w3: float, w4: float):
    return (
        (w1 + w2 + w3 + w4) * r/4,
        (-w1 + w2 + w3 - w4) * r/4,
        (-w1 + w2 - w3 + w4) * r/(4 * (lx + ly)),
    )

rl = MotorFeedback(6, 7, 11, reverse=True)
fl = MotorFeedback(4, 5, 19, reverse=True)
rr = MotorFeedback(8, 9, 13)
fr = MotorFeedback(2, 3, 21)
motors = [fl, fr, rl, rr]
