"""
Affordable project setup module.

Copyright (C) 2017

This file is part of Affordable.

Affordable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Affordable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Affordable.  If not, see <http://www.gnu.org/licenses/>.
"""

import time
from affordable import cozmo_actions, interactions
from cozmo.objects import LightCube1Id
import cozmo


def affordable_program(robot: cozmo.robot.Robot):
    cube1 = robot.world.get_light_cube(LightCube1Id)

    if cube1 is not None:
        cube1.set_lights(cozmo.lights.green_light)

    cozmo_robot = cozmo_actions.CozmoActions(robot, cube1)
    cozmo_robot.move(interactions.Interaction.Type.FORWARD)
    cozmo_robot.move(interactions.Interaction.Type.TURN_LEFT)
    cozmo_robot.move(interactions.Interaction.Type.FORWARD)
    cozmo_robot.move(interactions.Interaction.Type.EAT)
    cozmo_robot.move(interactions.Interaction.Type.CHARGE)
    cozmo_robot.move(interactions.Interaction.Type.TURN_RIGHT)
    cozmo_robot.move(interactions.Interaction.Type.FORWARD)
    cozmo_robot.move(interactions.Interaction.Type.MISS)
    time.sleep(3)


def main():
    cozmo.run_program(affordable_program)
