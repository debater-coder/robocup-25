from Makerverse_Motor_2ch import motor, twoMotorRobot
from time import sleep

robot = twoMotorRobot(pwmPinLeft = 0, dirPinLeft = 1, pwmPinRight = 2, dirPinRight = 25)

print("testing speed")
robot.speed(100)
sleep(2)

print("testing turnLeft()")
robot.turnLeft()
sleep(5)

print("testing turnRight()")
robot.turnLeft()
sleep(5)

print("testing rotateRight()")
robot.turnLeft()
sleep(5)

print("testing rotateLeft()")
robot.turnLeft()
sleep(5)

print("testing driveForward()")
robot.turnLeft()
sleep(5)

print("testing driveReverse()")
robot.turnLeft()
sleep(5)

print("testing stop()")
robot.stop()

