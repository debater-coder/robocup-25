from multiprocessing import Process, Queue
import queue

from posetree import Pose, PoseTree, Transform
from components.debug_server import debug_sever
import py_trees
import numpy as np


class DebugUI(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super().__init__(name)

        self.blackboard = self.attach_blackboard_client(name="Debug UI")

        self.blackboard.register_key(
            "target_vel", access=py_trees.common.Access.WRITE, required=True
        )

        self.blackboard.register_key(
            "posetree", access=py_trees.common.Access.READ, required=True
        )

        self.blackboard.register_key(
            "vel", access=py_trees.common.Access.READ, required=True
        )

        self.target_vel_queue: Queue[tuple[float, float, float]] = Queue()
        self.pose_queue: Queue[tuple[float, float, float]] = Queue()
        self.vel_queue: Queue[tuple[float, float, float]] = Queue()

    def setup(self, **kwargs):
        self.target_vel_queue: Queue[tuple[float, float, float]] = Queue()
        self.pose_queue: Queue[tuple[float, float, float]] = Queue()
        self.vel_queue: Queue[tuple[float, float, float]] = Queue()
        self.process = Process(
            target=debug_sever,
            args=(self.target_vel_queue, self.pose_queue, self.vel_queue),
        )
        self.process.start()

    def update(self) -> py_trees.common.Status:
        try:
            vel = self.target_vel_queue.get_nowait()
            self.blackboard.target_vel = np.array(vel)
        except queue.Empty:
            pass

        posetree: PoseTree = self.blackboard.posetree
        chassis = Pose(Transform.identity(), "chassis", posetree).in_frame("field")

        self.pose_queue.put((chassis.x, chassis.y, chassis.rotation.as_euler("zyx")[0]))
        self.vel_queue.put(self.blackboard.vel)

        return py_trees.common.Status.RUNNING

    def terminate(self, new_status: py_trees.common.Status) -> None:
        if self.process:
            self.process.terminate()
            self.process = None
