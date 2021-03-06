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


from affordable import cozmo_actions, controller, interactions
import cozmo


def affordable_program(robot: cozmo.robot.Robot):
    controller.start_controller(robot)


def main():
    cozmo.run_program(affordable_program)
