

# manage Green house position

from enum import Enum

class Position(Enum):
    OPENED = 1
    CLOSED = 0


import loadparam
p = loadparam.Param()


def GetDoorPosition():
    with open(p.PositionFile) as f:
        position = f.read()
        return Position.CLOSED if int(position) == 0 else Position.OPENED