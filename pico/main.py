from command import CommandInput
from kinematics import Kinematics


command_input = CommandInput()
kinematics = Kinematics()

while True:
    if command := command_input.poll():
        kinematics.set_speed(*command)
    kinematics.update()
