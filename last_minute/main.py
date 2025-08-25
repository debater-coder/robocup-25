from typing import Literal
from gpiozero import PhaseEnableMotor, Button, LED
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


# motor gpio
rl = PhaseEnableMotor(13, 6, pwm=True)
fl = PhaseEnableMotor(22, 27, pwm=True)
rr = PhaseEnableMotor(10, 9, pwm=True)
fr = PhaseEnableMotor(11, 5, pwm=True)


def set_speed(vx, vy, vw):
    global rl
    global fl
    global rr
    global fr
    motors = [fl, fr, rl, rr]

    values = inverse_kinematics(vx, vy, vw)
    max_value = max(values, key=abs)

    # scale values by max (phase_enable motor has range (1, -1))
    values = [min(1, max(-1, value)) / max_value for value in values]

    for motor, value in zip(motors, values):
        motor.value = value


# choose goal
goal_button = Button(2)  # short 2 to ground for cyan goal, otherwise yellow goal

# goal indicator LEDs (indicates active goal)
cyan = LED(23)
yellow = LED(24)

# HSV values
orangeLower = (20, 86, 30)
orangeUpper = (35, 255, 255)

cyanLower = (180, 86, 30)
cyanUpper = (240, 255, 255)

yellowLower = (50, 86, 30)
yellowUpper = (65, 255, 255)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

has_possession = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    goal = "cyan" if goal_button.is_pressed else "yellow"
    print("goal", goal)

    rotated = cv2.rotate(frame, cv2.ROTATE_180)

    # identify ball location
    blurred = cv2.GaussianBlur(rotated, (11, 11), 0)
    width, height = rotated.shape[:2]
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    ball = None

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 40:
            cv2.circle(rotated, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            print("ball found", x, y)
            ball = (x, y)

    # we see the ball
    if ball:
        has_possession = False

        error = ball[0] - width / 2
        kp = 0.001

        if abs(error) > 150:
            # rotate proportionally to error
            set_speed(1, 0, kp * error)
        else:
            # go forward
            set_speed(1, 0, 0)

            if ball[1] > 3 / 4 * height:
                # in possession zone:
                has_possession = True

    elif has_possession:
        lower, upper = (
            (yellowLower, yellowUpper) if goal == "yellow" else (cyanLower, cyanUpper)
        )

        goal_mask = cv2.inRange(hsv, lower, upper)

        pixels = cv2.count_pixels(goal_mask)

    else:
        # can't see ball, start spinnign
        set_speed(0, 0, 1)

    cv.imshow("rotated", rotated)
    if cv.waitKey(1) == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
