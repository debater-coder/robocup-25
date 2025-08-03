import py_trees
import typing
import time
import numpy as np

from interfaces import SupportsCommand


class VelocityControl(py_trees.behaviour.Behaviour):
    """Performs closed loop control of robot velocity using odometry."""

    def __init__(self, name: str):
        super().__init__(name)
        self.blackboard = self.attach_blackboard_client(name="Velocity Control")
        self.command: SupportsCommand | None = None

        self.blackboard.register_key("odom", access=py_trees.common.Access.WRITE)
        self.blackboard.register_key("target_vel", access=py_trees.common.Access.READ)

        self.last_time = time.time()

    def setup(self, **kwargs: typing.Any) -> None:
        """Used to dependency inject SupportsCommand instance."""
        if "command" in kwargs and isinstance(
            command := kwargs["command"], SupportsCommand
        ):
            self.command = command
            self.logger.info(f"Initialised with command: {command}")
        else:
            raise TypeError("Expected command to be passed in VelocityControl.setup()")

    def initialise(self) -> None:
        # We do this to reset the elapsed time the first time behaviour is ticked
        self.last_time = time.time()

    def update(self) -> py_trees.common.Status:
        delta = time.time() - self.last_time
        self.last_time = time.time()

        if delta > 0.5:
            self.logger.warning(
                f"Delta time too large: {delta:.3f}s — skipping PID update"
            )
            return py_trees.common.Status.RUNNING

        return py_trees.common.Status.RUNNING
