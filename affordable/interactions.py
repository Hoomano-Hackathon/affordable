from enum import IntEnum

class Interaction:
    def __init__(self, identifier, valence, signature=None):
        self.id = identifier
        self.valence = valence
        self.signature = signature

    class Type(IntEnum):
        FORWARD = 0
        BUMP = 1
        PUSH = 2
        EAT = 3
        MISS = 4
        CHARGE = 5
        TURN_LEFT = 6
        TURN_RIGHT = 7
        TURN_DIAG_LEFT = 8
        TURN_DIAG_RIGHT = 9

class Action(Interaction):
    def __init__(self, identifier, valence, actionFunctor, signature=None):
        Interaction.__init__(self, identifier, valence, signature)
        self.action = actionFunctor

    def __call__(self):
        self.action()

class Rotation(Action):
    def __init__(self, identifier, valence, actionFunctor, angle, signature=None):
        Action.__init__(self, identifier, valence, actionFunctor, signature)
        self.angle = angle

    def __call__(self):
        self.action(self.angle)


if __name__ == "__main__":
    a = Action(Interaction.Type.CHARGE, -1, (lambda: print(-1)))
    r = Rotation(
            Interaction.Type.TURN_DIAG_LEFT,
            -2,
            lambda ang: print(ang),
            45)
    a()
    r()
