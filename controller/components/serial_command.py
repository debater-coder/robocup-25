from __future__ import annotations
from multiprocessing import Queue
from typing import Tuple, TypeGuard
import warnings
import queue

command_queue: Queue[tuple[float, float, float]] = Queue()
odom_queue: Queue[tuple[float, float, float]] = Queue()


def serial_process(dev: str):
    import serial

    port = serial.Serial(dev, 115200)

    # Reset port (^C^D)
    port.write(b"\x03\x04")
    for i in range(50):
        port.readline()

    pending = ""

    while True:
        # send command (don't block on waiting for command)
        if not command_queue.empty():
            vx, vy, vw = command_queue.get()
            port.write(f"{vx} {vy} {vw}\n".encode())
            for i in range(50):
                port.readline()

        # receive odom (MCU is spamming it anyway so ok to block)
        line = port.readline().decode()
        if line:
            if line[-1] == "\n":
                try:
                    odometry = tuple(map(float, (pending + line).split()))

                    if not is_three_element_tuple(odometry):
                        raise ValueError
                    odom_queue.put(odometry)
                except (ValueError, TypeError):
                    warnings.warn("Failed to parse odometry")
                finally:
                    pending = ""

            else:
                pending = line


def is_three_element_tuple[T](val: Tuple[T, ...]) -> TypeGuard[tuple[T, T, T]]:
    return len(val) == 3


class SerialCommand:
    """Velocity command for robot over serial to Pi Pico.

    Implements :py:class:`interfaces.SupportsCommand`"""

    def __init__(self, port: str = "/dev/ttyACM0"):
        self.odometry: Tuple[float, float, float] = (0, 0, 0)
        self.prev_command = None

    def send_command(self, vx: float, vy: float, vw: float):
        if self.prev_command != (vx, vy, vw):
            command_queue.put((vx, vy, vw))
        self.prev_command = (vx, vy, vw)

    def get_odometry(self):
        item = None
        while True:
            try:
                item = odom_queue.get_nowait()
            except queue.Empty:
                break

        if item:
            self.odometry = item

        return self.odometry
