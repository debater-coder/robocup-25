import argparse
import py_trees
import sys
import time

from components.mocks.command_mock import CommandMock
from components.serial_command import SerialCommand
from components.robocup_posetree import RobocupPoseTree

from interfaces.command import SupportsCommand
from root import create_root


parser = argparse.ArgumentParser(
    prog="Robocup controller",
    description="Controls a single Raspberry Pi to execute Robocup strategy.",
)
parser.add_argument("-r", "--render", action="store_true")
parser.add_argument("-s", "--sim", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
args = parser.parse_args()

root = create_root(args.debug)

if args.render:
    py_trees.display.render_dot_tree(root, with_blackboard_variables=True)
    sys.exit()


def create_tree() -> py_trees.trees.BehaviourTree:
    tree = py_trees.trees.BehaviourTree(root)

    command: SupportsCommand = CommandMock() if args.sim else SerialCommand()
    posetree = RobocupPoseTree()

    tree.setup(timeout=15, command=command, posetree=posetree)
    return tree


last_log = time.time()


def post_tick(tree):
    global last_log

    if time.time() - last_log < 3:
        return

    last_log = time.time()

    print(py_trees.display.unicode_blackboard())


py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
tree = create_tree()
tree.tick_tock(period_ms=100, post_tick_handler=post_tick)
