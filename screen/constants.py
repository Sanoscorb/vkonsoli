import enum


class Keys(enum.IntEnum):
    Tab = 9
    Enter = 13
    Escape = 27


class ActionCode(enum.IntEnum):
    NoAction = 0
    EndOfLoop = 1
