from gpiozero import PhaseEnableMotor
import numpy as np
import cv2 as cv

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


rl = PhaseEnableMotor(17, 4, pwm=True)
fl = PhaseEnableMotor(22, 27, pwm=True)
rr = PhaseEnableMotor(9, 10, pwm=True)
fr = PhaseEnableMotor(11, 5, pwm=True)

orangeLower = np.array([20, 86, 6])
orangeUpper = np.array([35, 255, 153])

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
