from typing import Protocol, Tuple, runtime_checkable
from abc import abstractmethod


@runtime_checkable
class SupportsCommand(Protocol):
    """Protocol for controlling robot via velocity commands."""

    @abstractmethod
    def send_command(self, vx: float, vy: float, vw: float) -> None:
        """Sends a velocity command to the robot (relative to the robot).

        These don't have any particular units, expect to use PID control to keep
        the robot at a velocity.

        Arguments:
        vx -- velocity in the x direction (+ve = forwards)
        vy -- velocity in the y direction (+ve = left)
        vw -- angular velocity (+ve = anticlockwise)
        """
        raise NotImplementedError

    @abstractmethod
    def get_odometry(self) -> Tuple[float, float, float]:
        """Returns the current odometry of the robot.

        The odometry gives the total displacement from an initial position. You
        should not assume this initial position directly, rather store offsets
        of different known odometry and compute differences between them.
        Odometry is prone to drift, so this should be supplemented by data from
        vision, and used primarily to smooth in between camera frames or to
        control velocity.

        Return value (tuple[x, y, w]):
        x -- odometry in the x direction in m (+ve = forwards)
        y -- odometry n the y direction in m (+ve = left)
        w -- relative angle in radians (+ve = anticlockwise)
        """
        raise NotImplementedError
