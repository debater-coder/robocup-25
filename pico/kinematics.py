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

# stage 1: accurate movement forwards only
# stage 2: four directions
# stage 3: four directions + rotation
# stage 4: pose based movement

rl = MotorFeedback(6, 7, 11, reverse=True)
fl = MotorFeedback(4, 5, 19, reverse=True)
rr = MotorFeedback(8, 9, 13)
fr = MotorFeedback(2, 3, 21)
