from typing import Tuple, TypeGuard
import serial
import warnings


def is_three_element_tuple[T](val: Tuple[T, ...]) -> TypeGuard[tuple[T, T, T]]:
    return len(val) == 3


class SerialCommand:
    """Velocity command for robot over serial to Pi Pico.

    Implements :py:class:`interfaces.SupportsCommand`"""

    def __init__(self, port: str = "/dev/ttyACM0"):
        self.port = serial.Serial(port, 115200, timeout=0)  # non-blocking

        # Reset port (^C^D)
        self.port.write(b"\x03\x04")

        self.pending = ""
        self.odometry: Tuple[float, float, float] = (0, 0, 0)

        self.prev_command = None

    def send_command(self, vx: float, vy: float, vw: float):
        if self.prev_command != (vx, vy, vw):
            self.port.write(f"{vx} {vy} {vw}\n".encode())
        self.prev_command = (vx, vy, vw)

    def get_odometry(self):
        line = self.port.readline().decode()
        if line:
            if line[-1] == "\n":
                odometry = tuple(map(float, (self.pending + line).split()))

                if not is_three_element_tuple(odometry):
                    warnings.warn("Failed to parse odometry")
                    return self.odometry

                self.odometry = odometry
                self.pending = ""
            else:
                self.pending = line

        return self.odometry
