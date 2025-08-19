from machine import Pin
from motor import Motor
import time
import micropython

micropython.alloc_emergency_exception_buf(100)


class Encoder:
    """Encoder for motor. Uses only one encoder input as direction sensing was unreliable"""

    def __init__(self, pin):
        pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.pin = pin
        self.odom = 0
        self.direction = 1

        self.pin.irq(self.irq_callback, Pin.IRQ_RISING)

    def irq_callback(self, pin: Pin):
        self.odom += self.direction

    def __str__(self) -> str:
        return str(self.odom)


class MotorFeedback:
    """Motor using encoder as speed feedback. Direction is assumed from motor direction."""

    def __init__(
        self,
        pwm: int,
        dir: int,
        encoder: int,
        pulses_per_revolution: int = 1050,
        kp: float = 10,
        ki: float = 0,
        kd: float = 0,
        reverse=False,
    ):
        self.motor = Motor(pwm, dir)
        self.encoder = Encoder(encoder)
        self.ppm = pulses_per_revolution
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.reverse = reverse
        self.speed = 0  # rev/s
        self.target = 0  # rev/s
        self.motor_power = 0  # [-100, 100]
        self.last_time = time.ticks_us()
        self.last_error = 0
        self.odom = 0.0

    def update(self):
        displacement = self.encoder.odom / self.ppm
        self.odom += displacement

        # calculate speed
        elapsed = time.ticks_diff(time.ticks_us(), self.last_time)
        self.speed = (displacement) / (elapsed / 1000000)

        # reset odom and time
        self.encoder.odom = 0
        self.last_time = time.ticks_us()

        # PID
        error = self.target - self.speed

        proportional = self.kp * error

        control = proportional
        self.motor_power += control
        self.motor_power = max(-100, min(100, self.motor_power))

        # update motor
        self.motor.speed(self.motor_power * (-1 if self.reverse else 1))
        self.encoder.direction = round(
            self.motor_power / max(abs(self.motor_power), 1e-6)
        )

    def set_speed(self, speed):
        self.target = speed
