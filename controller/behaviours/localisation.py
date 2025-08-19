from posetree.pose import Tuple
import py_trees
import typing
from posetree import PoseTree, Pose
from scipy.spatial.transform import Rotation
import numpy as np


class Localisation(py_trees.behaviour.Behaviour):
    """Uses odometry and vision data to obtain current robot pose."""

    def __init__(self, name: str):
        super().__init__(name)

        self.blackboard = self.attach_blackboard_client(name="Localisation")

        self.blackboard.register_key(
            "odom", access=py_trees.common.Access.READ, required=True
        )
        self.blackboard.register_key("posetree", access=py_trees.common.Access.WRITE)

        self.last_odom = np.array([0.0, 0.0, 0.0])

    def setup(self, **kwargs: typing.Any) -> None:
        """Used to dependency inject PoseTree instance."""
        if "posetree" in kwargs and isinstance(
            posetree := kwargs["posetree"], PoseTree
        ):
            self.blackboard.posetree = posetree

            self.blackboard.posetree.add_frame(
                Pose.from_position_and_rotation(
                    [0, 0, 0], Rotation.identity(), "field", self.blackboard.posetree
                ),
                "chassis",
            )
        else:
            raise TypeError("Expected posetree to be passed in Localisation.setup()")

    def update(self) -> py_trees.common.Status:
        """Stub implementation that just converts odometry into a pose"""

        delta = self.blackboard.odom - self.last_odom

        pose = Pose.from_position_and_rotation(
            [delta[0], delta[1], 0],
            Rotation.from_euler("z", delta[2]),
            "chassis",
            self.blackboard.posetree,
        ).in_frame("field")

        self.last_odom = self.blackboard.odom

        self.blackboard.posetree.add_frame(pose, "chassis")

        return py_trees.common.Status.RUNNING
