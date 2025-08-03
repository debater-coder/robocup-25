import numpy as np
import time


class CommandMock:
    def __init__(self) -> None:
        self.odom = np.array([0, 0, 0])
        self.vx = 0
        self.vy = 0
        self.vw = 0
        self.last_time = time.time()

    def send_command(self, vx: float, vy: float, vw: float):
        self.vx = vx
        self.vy = vy
        self.vw = vw

    def get_odometry(self):
        elapsed = time.time() - self.last_time
        self.last_time = time.time()

        self.odom += elapsed * np.array([self.vx, self.vy, self.vw])

        return tuple(self.odom)
