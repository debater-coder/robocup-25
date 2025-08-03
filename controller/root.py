import py_trees

from behaviours import VelocityControl


def create_root() -> py_trees.behaviour.Behaviour:
    """
    Creates a behaviour tree for controlling the state of a single robot.

    Resources:
    - https://arxiv.org/pdf/1709.00084
    - https://py-trees-ros-tutorials.readthedocs.io/en/devel/tutorials.html#before-we-start
    - https://py-trees.readthedocs.io/en/devel/trees.html

    This is kept in its own method so it can be used to generate diagrams with py-trees-render
    """
    root = py_trees.composites.Parallel(
        name="Robocup Controller",
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False),
    )

    # Data gathering (these all run in parallel on every tick)
    velocity_control = VelocityControl(name="Velocity Control")
    vision = py_trees.behaviours.Running(name="Vision Processing")
    localisation = py_trees.behaviours.Running(name="Localisation")

    root.add_children([velocity_control, vision, localisation])

    return root
