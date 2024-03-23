import abc
import curses


class Callback(abc.ABC):
    def __init__(self, window: curses.window = None):
        self.__window = window
        if self.__window is not None:
            self.setup()

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, win: curses.window):
        self.__window = win
        if self.__window is not None:
            self.setup()

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def action(self) -> int:
        pass
