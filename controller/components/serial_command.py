from __future__ import annotations
from multiprocessing import Process, Queue
from typing import Tuple, TypeGuard
import warnings
import queue


def serial_process(
    dev: str,
    command_queue: Queue[tuple[float, float, float]],
    odom_queue: Queue[tuple[float, float, float]],
):
    import serial

    port = serial.Serial(dev, 115200, write_timeout=0.5, timeout=0.02)

    # Reset port (^C^D)
    print("Resetting...")
    port.write(b"\x03\x04")
    port.flush()
    port.reset_input_buffer()
    print("Reset complete.")

    pending = ""

    while True:
        try:
            vx, vy, vw = command_queue.get_nowait()
            data = f"{vx} {vy} {vw}\n".encode()
            print(f"WRITE start data={data!r}")
            port.write(data)
            print("WRITE done")
            port.flush()
            print("FLUSH done")
        except queue.Empty:
            pass
        except serial.SerialTimeoutException:
            print("SerialTimeoutException on write/flush")

        print("READ start")
        line = port.readline().decode()
        print("READ done", line)
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

        self.command_queue: Queue[tuple[float, float, float]] = Queue()
        self.odom_queue: Queue[tuple[float, float, float]] = Queue()

        self.process = Process(
            target=serial_process, args=(port, self.command_queue, self.odom_queue)
        )
        self.process.start()

    def send_command(self, vx: float, vy: float, vw: float):
        if self.prev_command != (vx, vy, vw):
            self.command_queue.put((vx, vy, vw))
        self.prev_command = (vx, vy, vw)

    def get_odometry(self):
        item = None
        while True:
            try:
                item = self.odom_queue.get_nowait()
            except queue.Empty:
                break

        if item is not None:
            self.odometry = item

        return self.odometry
