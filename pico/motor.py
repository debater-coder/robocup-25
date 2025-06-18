# MicroPython classes for driving single motors, two motor robots, and stepper motors with
# the Core Electronics Makerverse 2ch Motor Driver.
#
# Written by Brenton Schulz
# Initial release: FEB-14-22

from machine import PWM, Pin

_FORWARD = 1
_REVERSE = 0


class Motor:
    def __init__(self, pwmPin=0, dirPin=1, speed=100, pwmFreq=200):
        if isinstance(pwmPin, int):
            pwmPin = Pin(pwmPin, Pin.OUT)
        elif isinstance(pwmPin, Pin):
            pwmPin.init(mode=Pin.OUT)
        else:
            raise TypeError("Argument 'pwm' must be an integer or Pin object")

        if isinstance(dirPin, int):
            dirPin = Pin(dirPin, Pin.OUT)
        elif isinstance(dirPin, Pin):
            dirPin.init(mode=Pin.OUT)
        else:
            raise TypeError("Argument 'direction' must be an integer or Pin object")

        self.pwmFreq = pwmFreq

        self.pwm = PWM(pwmPin)
        self.pwm.freq(self.pwmFreq)
        self.pwm.duty_u16(0)
        self.pwmDuty = 63353
        self.speedValue = speed
        self.dirPin = dirPin
        self.direction = _FORWARD
        self.dirPin.value(self.direction)

    def speed(self, speed):
        if speed < 0:
            self.direction = _REVERSE
        else:
            self.direction = _FORWARD
        speed = abs(speed)
        self.speedValue = speed
        self.pwmDuty = int(speed / 100 * 65535)
        if self.pwmDuty > 65535:
            self.pwmDuty = 65535
        self.go()

    def stop(self):
        self.pwm.duty_u16(0)

    def go(self):
        self.dirPin.value(self.direction)
        self.pwm.duty_u16(self.pwmDuty)

    def forward(self):
        self.direction = _FORWARD
        self.go()

    def reverse(self):
        self.direction = _REVERSE
        self.go()
