from enum import Enum
import loadparam
p = loadparam.Param()


class Position(Enum):
    OPENED = 1
    CLOSED = 0


def GetDoorPosition():
    with open(p.PositionFile) as f:
        position = f.read()
        return Position.CLOSED if int(position) == 0 else Position.OPENED