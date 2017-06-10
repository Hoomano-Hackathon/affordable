from affordable.spacememory import *
from affordable.signature import *
from affordable.interactions import *
from math import *
from sys import *

spacemem = SpaceMemory()
signatures = Signatures()

robotHunger = 1.0
def getValenceOfEat():
    global robotHunger
    return 50 * robotHunger

drive_distance = 150

theCube = []

interactions = {}
def initializeInteractions(cozmoActions):
    global interactions
    global theCube
    interactions = {
            Interaction.Type.FORWARD: DriveStraight(
                Interaction.Type.FORWARD,
                1,
                lambda: cozmo_actions.move_forward(),
                drive_distance,
                signatures.of(Interaction.Type.FORWARD)),
            Interaction.Type.BUMP: DriveStraight(
                Interaction.Type.BUMP,
                -10,
                lambda: cozmo_actions.move_forward(),
                drive_distance,
                signatures.of(Interaction.Type.BUMP)),
            Interaction.Type.PUSH: DriveStraight(
                Interaction.Type.PUSH,
                1,
                lambda: cozmo_actions.move_forward(),
                drive_distance,
                signatures.of(Interaction.Type.PUSH)),
            Interaction.Type.EAT: Action(
                Interaction.Type.EAT,
                getValenceOfEat,
                lambda: cozmo_actions.eat(theCube),
                signatures.of(Interaction.Type.EAT)),
            Interaction.Type.MISS: Action(
                Interaction.Type.MISS,
                -1,
                lambda: cozmo_actions.animate_lift(),
                signatures.of(Interaction.Type.MISS)),
            Interaction.Type.CHARGE: Action(
                Interaction.Type.CHARGE,
                -1,
                lambda: cozmo_actions.charge(theCube),
                signatures.of(Interaction.Type.CHARGE)),
            Interaction.Type.TURN_LEFT: Rotation(
                Interaction.Type.TURN_LEFT,
                -1,
                lambda angle: cozmo_actions.rotation(angle),
                90),
            Interaction.Type.TURN_RIGHT: Rotation(
                Interaction.Type.TURN_RIGHT,
                -1,
                lambda angle: cozmo_actions.rotation(angle),
                -90),
            Interaction.Type.TURN_DIAG_LEFT: Rotation(
                Interaction.Type.TURN_DIAG_LEFT,
                -1,
                lambda angle: cozmo_actions.rotation(angle),
                45),
            Interaction.Type.TURN_DIAG_RIGHT: Rotation(
                Interaction.Type.TURN_DIAG_RIGHT,
                -1,
                lambda angle: cozmo_actions.rotation(angle),
                -45),
            }

farAwayObjetsInterest = 1
spaceMemoryCoef = 1
cozmoActions = None


def checkForCubesAhead():
    global theCube
    global cozmoActions

    theCube = cozmoActions.checkForCubeAhead()


def utility(loc):
    util = [0 for k in range(10)]
    for inter in range(6):
        for seq in loc[inter]:
            val = interactions[inter].getValence()
            util[seq[-1]] += val * math.exp(
                    -farAwayObjetsInterest * len(seq))
    return util

def mostUsefulAction(enactability, util):
    bestAction = -1
    maximum = float("-inf")
    for i in range(len(util)):
        if enactability[i]:
            if util[i] > maximum:
                maximum = util[i]
                bestAction = i
    return bestAction

def doAction(actionIndex):
    if actionIndex == Interaction.Type.FORWARD \
        or actionIndex == Interaction.Type.BUMP \
        or actionIndex == Interaction.Type.PUSH:
            if interactions[actionIndex]():
                return Interaction.Type.BUMP
    else:
        interactions[actionIndex]()
    return actionIndex

def step(enacted):
    global robotHunger
    spacemem.update(enacted)

    checkForCubesAhead()

    if Interaction.Type.BUMP == enacted:
        spacemem.bumpDetected()
    elif Interaction.Type.EAT == enacted:
        robotHunger = -0.1

    env = spacemem.getMatrix()
    enactability = [False for i in range(10)]
    for i in range(10):
        enactability[i] = signatures.predict(i, env)

    localizations = signatures.getPositions(env)
    util = utility(localizations)
    for i in range(10):
        util[i] = interactions[i].getValence() + spaceMemoryCoef * util[i]

    nextAction = mostUsefulAction(enactability, util)
    if robotHunger < 1.0:
        robotHunger = 0.04
    return nextAction


def start_controller(robot):
    global theCube
    global cozmoActions

    enacted = Interaction.Type.FORWARD
    cozmoActions = robot.CozmoActions(robot)
    initializeInteractions(cozmo_actions)
    checkForCubeAhead()
    exitOrNot = ""
    while exitOrNot != "q":
        enacted = step(enacted)
        exitOrNot = input('Press ENTER to continue.')

