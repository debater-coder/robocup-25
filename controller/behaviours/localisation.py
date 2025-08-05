import py_trees
import typing
from posetree import PoseTree, Pose
from scipy.spatial.transform import Rotation


class Localisation(py_trees.behaviour.Behaviour):
    """Uses odometry and vision data to obtain current robot pose."""

    def __init__(self, name: str):
        super().__init__(name)

        self.blackboard = self.attach_blackboard_client(name="Localisation")

        self.blackboard.register_key(
            "odom", access=py_trees.common.Access.READ, required=True
        )

        self.posetree: PoseTree | None = None

    def setup(self, **kwargs: typing.Any) -> None:
        """Used to dependency inject PoseTree instance."""
        if "posetree" in kwargs and isinstance(
            posetree := kwargs["posetree"], PoseTree
        ):
            self.posetree = posetree
        else:
            raise TypeError("Expected posetree to be passed in Localisation.setup()")

    def update(self) -> py_trees.common.Status:
        """Stub implementation that just converts odometry into a pose"""
        if not self.posetree:
            raise ValueError("Expected Localisation.setup() to be called.")

        pose = Pose.from_position_and_rotation(
            [self.blackboard.odom[0], self.blackboard.odom[1], 0],
            Rotation.from_euler("z", self.blackboard.odom[2]),
            "field",
            self.posetree,
        )

        self.posetree.add_frame(pose, "chassis")

        return py_trees.common.Status.RUNNING
