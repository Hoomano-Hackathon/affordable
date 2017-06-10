from spacememory import *
from signature import *
from interactions import *
# from cozmo_actions import *

spacemem = SpaceMemory()
signatures = Signatures()

drive_distance = 150
interactions = {
        Interaction.Type.FORWARD: DriveStraight(
            Interaction.Type.FORWARD,
            1,
            None,
            drive_distance,
            signatures.of(Interaction.Type.FORWARD)),
        Interaction.Type.BUMP: DriveStraight(
            Interaction.Type.BUMP,
            -10,
            None,
            drive_distance,
            signatures.of(Interaction.Type.BUMP)),
        Interaction.Type.PUSH: DriveStraight(
            Interaction.Type.PUSH,
            1,
            None,
            drive_distance,
            signatures.of(Interaction.Type.PUSH)),
        Interaction.Type.EAT: Interaction(
            Interaction.Type.EAT,
            None, #functor in agent 
            None,
            signatures.of(Interaction.Type.EAT)),
        Interaction.Type.MISS: Interaction(
            Interaction.Type.MISS,
            -1,
            None,
            signatures.of(Interaction.Type.MISS)),
        Interaction.Type.CHARGE: Interaction(
            Interaction.Type.CHARGE,
            -1,
            None,
            signatures.of(Interaction.Type.CHARGE)),
        Interaction.Type.TURN_LEFT: Rotation(
            Interaction.Type.TURN_LEFT,
            -1,
            None,
            90,
            signatures.of(Interaction.Type.TURN_LEFT)),
        Interaction.Type.TURN_RIGHT: Rotation(
            Interaction.Type.TURN_RIGHT,
            -1,
            None,
            -90,
            signatures.of(Interaction.Type.TURN_RIGHT)),
        Interaction.Type.TURN_DIAG_LEFT: Rotation(
            Interaction.Type.TURN_DIAG_LEFT,
            -1,
            None,
            45,
            signatures.of(Interaction.Type.TURN_DIAG_LEFT)),
        Interaction.Type.TURN_DIAG_RIGHT: Rotation(
            Interaction.Type.TURN_DIAG_RIGHT,
            -1,
            None,
            -45,
            signatures.of(Interaction.Type.TURN_DIAG_RIGHT)),
        }

def main():
    print('wow')

def checkForCubesAhead():
    print('wow')


def step(enacted):
    spacemem.update(enacted)

    checkForCubesAhead()

    if enacted.id == Interaction.Type.BUMP:
        spacemem.bumpDetected()

    env = spacemem.getMatrix()
    enactability = [false for i in range(10)]
    for i in range(10):
        enactability[i] = signatures.predict(i, env)

main()
