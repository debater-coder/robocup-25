# MicroPython classes for driving single motors, two motor robots, and stepper motors with 
# the Core Electronics Makerverse 2ch Motor Driver.
# 
# Written by Brenton Schulz
# Initial release: FEB-14-22

from machine import PWM, Pin
import time

_FORWARD = 1
_REVERSE = 0

class motor():
    def __init__(self, pwmPin = 0, dirPin = 1, speed = 100, pwmFreq = 200):
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
        self.pwmDuty = int(speed/100*65535)
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

    def drive(self, speed, duration_ms):
        self.speed(speed)
        time.sleep_ms(duration_ms)
        self.stop()

class twoMotorRobot():
    def __init__(self, pwmPinLeft = 0, dirPinLeft = 1, pwmPinRight = 2, dirPinRight = 3):
        self.motorLeft = motor(pwmPinLeft, dirPinLeft)
        self.motorRight = motor(pwmPinRight, dirPinRight)
    
    def speed(self, speed = 100):
        self.motorLeft.speed(speed)
        self.motorRight.speed(speed)
    
    def turnLeft(self):
        self.motorLeft.stop()
        self.motorRight.forward()
        
    def turnRight(self):
        self.motorLeft.forward()
        self.motorRight.stop()
        
    def rotateRight(self):
        self.motorLeft.reverse()
        self.motorRight.forward()
        
    def rotateLeft(self):
        self.motorLeft.forward()
        self.motorRight.reverse()
        
    def driveForward(self):
        self.motorLeft.forward()
        self.motorRight.forward()
        
    def driveReverse(self):
        self.motorLeft.reverse()
        self.motorRight.reverse()
        
    def stop(self):
        self.motorLeft.stop()
        self.motorRight.stop()
    