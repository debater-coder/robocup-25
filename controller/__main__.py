import argparse
import py_trees
import sys

from components.mocks.command_mock import CommandMock
from interfaces.command import SupportsCommand
from root import create_root

parser = argparse.ArgumentParser(
    prog="Robocup controller",
    description="Controls a single Raspberry Pi to execute Robocup strategy.",
)
parser.add_argument("-r", "--render", action="store_true")
args = parser.parse_args()

root = create_root()

if args.render:
    py_trees.display.render_dot_tree(root, with_blackboard_variables=True)
    sys.exit()


def create_tree() -> py_trees.trees.BehaviourTree:
    tree = py_trees.trees.BehaviourTree(root)

    command: SupportsCommand = CommandMock()

    tree.setup(timeout=15, command=command)
    return tree


def post_tick(tree):
    print(
        py_trees.display.unicode_tree(
            tree.root,
        ),
        py_trees.display.unicode_blackboard(),
    )


tree = create_tree()
tree.tick_tock(period_ms=16, post_tick_handler=post_tick)
