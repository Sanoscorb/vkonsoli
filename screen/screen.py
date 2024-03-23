import curses
import curses.panel as panel

from .callback import Callback
from .constants import *


def list_output(win: curses.window, begy: int, begx: int, lst: list[str], index: int):
    maxsize = 0
    y, x = begy, begx
    maxy, _ = win.getmaxyx()
    win.move(begy, begx)

    for i in range(len(lst)):
        cursy, _ = win.getyx()
        if cursy == maxy - 1:
            x += maxsize + 1
            y = begy

        if maxsize < len(lst[i]):
            maxsize = len(lst[i])

        if i == index:
            win.attron(curses.A_REVERSE)
        win.addstr(y, x, lst[i])
        win.attroff(curses.A_REVERSE)
        y += 1

    win.refresh()


class Screen:
    MENU_WIDTH = 15 + 2
    
    def __init__(self, names: list[str], callbacks: list[Callback]):
        self.__hlt = 0
        self.__pages = []
        self.__names = names
        self.__callbacks = callbacks
        self.__screen = curses.initscr()
        self.__height, self.__width = self.__screen.getmaxyx()

        cols = curses.COLS
        lines = curses.LINES

        curses.raw()
        curses.nonl()
        curses.noecho()
        curses.curs_set(0)
        curses.set_escdelay(1)
        self.__screen.keypad(True)

        for i in range(len(names)):
            win = curses.newwin(lines-2, cols-self.MENU_WIDTH-1, 1, self.MENU_WIDTH)
            self.__pages.append(panel.new_panel(win))
            self.__callbacks[i].window = win

        self.__screen.box()
        self.menu_border()
        self.__screen.addstr(0, self.MENU_WIDTH, names[self.__hlt])
        self.__pages[self.__hlt].top()

        panel.update_panels()
        curses.doupdate()
        list_output(self.__screen, 1, 1, names, -1)

    def __del__(self):
        curses.endwin()

    @property
    def highlight(self):
        return self.__hlt
    
    @highlight.setter
    def highlight(self, hlt):
        if hlt < len(self.__names):
            self.__hlt = hlt
        
        self.__pages[self.__hlt].top()

    def loop(self):
        code = ActionCode.NoAction
        while code != ActionCode.EndOfLoop:
            ch = self.__screen.getch()
            match ch:
                case curses.KEY_RESIZE:
                    self.resize()
                case Keys.Tab:
                    self.switch()
                case _:
                    curses.ungetch(ch)
                    code = self.__callbacks[self.__hlt].action()

            curses.flushinp()

    def menu_border(self):
        acs_ttee = curses.ACS_TTEE
        acs_btee = curses.ACS_BTEE
        acs_vline = curses.ACS_VLINE

        self.__screen.addch(0, self.MENU_WIDTH - 1, acs_ttee)
        self.__screen.vline(1, self.MENU_WIDTH - 1, acs_vline, self.__height - 2)
        self.__screen.addch(self.__height - 1, self.MENU_WIDTH - 1, acs_btee)

    def menu_process(self) -> int:
        hlt = self.__hlt
        ch = 0
        while ch not in [Keys.Enter, Keys.Escape, Keys.Tab]:
            list_output(self.__screen, 1, 1, self.__names, hlt)
            ch = self.__screen.getch()

            match ch:
                case curses.KEY_UP:
                    if hlt > 0:
                        hlt -= 1
                case curses.KEY_DOWN:
                    if hlt < len(self.__names) - 1:
                        hlt += 1

        if ch == Keys.Enter:
            self.__hlt = hlt

        list_output(self.__screen, 1, 1, self.__names, -1)
        return hlt

    def resize(self):
        try:
            self.__screen.hline(self.__height - 1, 0, ' ', self.__width)
            self.__screen.vline(0, self.__width - 1, ' ', self.__height)
            self.__screen.hline(0, 0, ' ', self.__width)
            self.__screen.vline(0, 0, ' ', self.__height)
        except curses.error:
            pass

        self.__height, self.__width = self.__screen.getmaxyx()
        curses.resizeterm(self.__height, self.__width)
        self.__screen.box()
        self.menu_border()
        self.__screen.addstr(0, self.MENU_WIDTH, self.__names[self.__hlt])

        for page in self.__pages:
            page.window().resize(self.__height-2, self.__width-self.MENU_WIDTH-1)

        panel.update_panels()
        curses.doupdate()

    def switch(self):
        hline = curses.ACS_HLINE

        self.__screen.hline(0, self.MENU_WIDTH, hline, len(self.__names[self.__hlt]))
        self.highlight = self.menu_process()
        self.__screen.addstr(0, self.MENU_WIDTH, self.__names[self.__hlt])
        panel.update_panels()
        curses.doupdate()
