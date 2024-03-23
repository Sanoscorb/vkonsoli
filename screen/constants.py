import enum


class Keys(enum.IntEnum):
    tab = 9
    enter = 13
    escape = 27


class ExitCode(enum.IntEnum):
    none = 0
    endOfLoop = 1
    exitToSwitch = 2
    resize = 3
    error = 4
