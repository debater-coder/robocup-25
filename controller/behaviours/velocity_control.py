import py_trees
import typing
import time
import numpy as np

from interfaces import SupportsCommand
from dataclasses import dataclass


@dataclass
class PDControl:
    """Closed loop proportional-derivative control of a single axis."""

    kp: float
    kd: float
    error_prev: float = 0

    def update(self, error: float, delta: float) -> float:
        proportional = error * self.kp
        derivative = (error - self.error_prev) / delta * self.kd

        self.error_prev = error

        return proportional + derivative


class VelocityControl(py_trees.behaviour.Behaviour):
    """Performs closed loop control of robot velocity using odometry."""

    def __init__(self, name: str):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name="Velocity Control")
        self.command: SupportsCommand | None = None

        # Sensed from odometry
        self.blackboard.register_key("odom", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("vel", access=py_trees.common.Access.WRITE)

        # Input from control
        self.blackboard.register_key("target_vel", access=py_trees.common.Access.READ)

        self.last_time = time.time()
        self.blackboard.odom = np.array([0, 0, 0])
        self.blackboard.vel = np.array([0, 0, 0])

        # Separate PD controllers for each axis
        self.controls = [
            PDControl(kp=1, kd=0.1),  # x
            PDControl(kp=1, kd=0.1),  # y
            PDControl(kp=1, kd=0.1),  # w
        ]

    def setup(self, **kwargs: typing.Any) -> None:
        """Used to dependency inject SupportsCommand instance."""
        if "command" in kwargs and isinstance(
            command := kwargs["command"], SupportsCommand
        ):
            # set initial odometry
            self.blackboard.odom = command.get_odometry()
            self.last_time = time.time()

            self.command = command
            self.logger.info(f"Initialised with command: {command}")
        else:
            raise TypeError("Expected command to be passed in VelocityControl.setup()")

    def get_odometry(self):
        if not self.command:
            raise ValueError("Expected command to be initialised by setup()")

        return np.array(self.command.get_odometry())

    def send_command(self, vx: float, vy: float, vw: float):
        if not self.command:
            raise ValueError("Expected command to be initialised by setup()")

        self.command.send_command(vx, vy, vw)

    def update(self) -> py_trees.common.Status:
        delta = time.time() - self.last_time
        self.last_time = time.time()

        if delta > 0.5:
            self.logger.warning(
                f"Delta time too large: {delta:.3f}s — skipping PID update"
            )
            return py_trees.common.Status.RUNNING

        odom = self.get_odometry()
        self.blackboard.vel = (odom - self.blackboard.odom) / delta  # current velocity
        self.blackboard.odom = odom

        vx, vy, vw = (
            control.update(target - actual, delta)
            for target, actual, control in zip(
                self.blackboard.target_vel, self.blackboard.vel, self.controls
            )
        )

        self.send_command(vx, vy, vw)

        return py_trees.common.Status.RUNNING

    def terminate(self, new_status: py_trees.common.Status) -> None:
        """Safely stop motors on termination."""
        self.send_command(0, 0, 0)
