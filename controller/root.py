import py_trees
import numpy as np

from behaviours import VelocityControl
from behaviours.debug_ui import DebugUI
from behaviours.localisation import Localisation


def create_root() -> py_trees.behaviour.Behaviour:
    """
    Creates a behaviour tree for controlling the state of a single robot.

    Resources:
    - https://arxiv.org/pdf/1709.00084
    - https://py-trees-ros-tutorials.readthedocs.io/en/devel/tutorials.html#before-we-start
    - https://py-trees.readthedocs.io/en/devel/trees.html

    This is kept in its own method so it can be used to generate diagrams with py-trees-render
    """
    # Blackboard static initialisation
    blackboard = py_trees.blackboard.Client(name="Global")
    blackboard.register_key("target_vel", access=py_trees.common.Access.WRITE)
    blackboard.target_vel = np.array([0.0, 0.0, 0.0])

    # Tree building
    root = py_trees.composites.Parallel(
        name="Robocup Controller",
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False),
    )

    # Data gathering (these all run in parallel on every tick)
    velocity_control = VelocityControl(name="Velocity Control")
    vision = py_trees.behaviours.Running(name="Vision Processing")  # placeholder
    localisation = Localisation(name="Localisation")
    debug_ui = DebugUI(name="Debug UI server")

    root.add_children([velocity_control, vision, localisation, debug_ui])

    return root
