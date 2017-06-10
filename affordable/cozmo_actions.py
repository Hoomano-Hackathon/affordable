"""
Affordable project Cozmo actions.

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

import cozmo
import time
from affordable import interactions
from cozmo.util import degrees


class CozmoActions(object):
    def __init__(self, robot):
        self.robot = robot
        self.robot.set_lift_height(1.0).wait_for_completed()

    def move(self, move_type):
        if move_type == interactions.Interaction.Type.FORWARD:
            self.move_forward()
        elif move_type == interactions.Interaction.Type.TURN_LEFT:
            self.robot.turn_in_place(degrees(90)).wait_for_completed(),
        elif move_type == interactions.Interaction.Type.TURN_RIGHT:
            self.robot.turn_in_place(degrees(-90)).wait_for_completed(),
        elif move_type == interactions.Interaction.Type.EAT:
            self.animate_lift()
            self.cube1.set_lights(cozmo.lights.red_light)
        elif move_type == interactions.Interaction.Type.CHARGE:
            self.animate_lift()
            self.cube1.set_lights(cozmo.lights.green_light)
        elif move_type == interactions.Interaction.Type.MISS:
            self.animate_lift()

    def move_forward(self):
        self.robot.drive_wheels(50, 50)
        t = 0
        cliff_detected = False

        while t < 25 and not cliff_detected:
            t += 1
            time.sleep(0.1)
            if self.robot.is_cliff_detected:
                cliff_detected = True

        self.robot.drive_wheels(0, 0)

        if cliff_detected:
            self.robot.drive_wheels(-50, -50)
            time.sleep(2)
            self.robot.drive_wheels(0, 0)

    def animate_lift(self):
        self.robot.set_lift_height(0.7).wait_for_completed()
        time.sleep(0.5)
        self.robot.set_lift_height(1.0).wait_for_completed()

    def checkForCubeAhead(self):
        cube = self.robot.world.wait_for_observed_light_cube(timeout=-1)
        if cube is not None:
            print(cube)
            line=str(cube.pose).split(" ")
            return [cube.object_id, float(line[3]) / 10, float(line[5]) / 10, float(line[21].replace('(', ''))]

        return None

