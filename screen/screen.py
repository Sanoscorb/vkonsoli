import curses
import curses.panel as panel

from .callback import *
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
        self.hlt = 0
        self.pages = []
        self.names = names
        self.callbacks = callbacks
        self.screen = curses.initscr()
        self.height, self.width = self.screen.getmaxyx()

        cols = curses.COLS
        lines = curses.LINES

        curses.raw()
        curses.nonl()
        curses.noecho()
        curses.curs_set(0)
        curses.set_escdelay(1)
        self.screen.keypad(True)

        for i in range(len(names)):
            win = curses.newwin(lines-2, cols-self.MENU_WIDTH-1, 1, self.MENU_WIDTH)
            self.pages.append(panel.new_panel(win))
            self.callbacks[i].window = win

        self.screen.box()
        self.menu_border()
        self.screen.addstr(0, self.MENU_WIDTH, names[self.hlt])
        self.pages[self.hlt].top()

        panel.update_panels()
        curses.doupdate()
        list_output(self.screen, 1, 1, names, -1)

    def __del__(self):
        curses.endwin()

    def __getitem__(self, i):
        return self.pages[i]
    
    def loop(self):
        code = ExitCode.none
        while code != ExitCode.endOfLoop:
            ch = self.screen.getch()
            match ch:
                case curses.KEY_RESIZE:
                    self.resize()
                case 9:
                    self.switch()
                case _:
                    curses.ungetch(ch)
                    code = self.callbacks[self.hlt].action()

            curses.flushinp()

    def menu_border(self):
        acs_ttee = curses.ACS_TTEE
        acs_btee = curses.ACS_BTEE
        acs_vline = curses.ACS_VLINE

        self.screen.addch(0, self.MENU_WIDTH - 1, acs_ttee)
        self.screen.vline(1, self.MENU_WIDTH - 1, acs_vline, self.height - 2)
        self.screen.addch(self.height - 1, self.MENU_WIDTH - 1, acs_btee)

    def menu_process(self) -> int:
        hlt = self.hlt
        ch = 0
        while ch not in [9, 13, 27]:
            list_output(self.screen, 1, 1, self.names, hlt)
            ch = self.screen.getch()

            match ch:
                case curses.KEY_UP:
                    if hlt > 0:
                        hlt -= 1
                case curses.KEY_DOWN:
                    if hlt < len(self.names) - 1:
                        hlt += 1

        if ch == 13:
            self.hlt = hlt

        list_output(self.screen, 1, 1, self.names, -1)
        return hlt

    def resize(self):
        try:
            self.screen.hline(self.height - 1, 0, ' ', self.width)
            self.screen.vline(0, self.width - 1, ' ', self.height)
            self.screen.hline(0, 0, ' ', self.width)
            self.screen.vline(0, 0, ' ', self.height)
        except curses.error:
            pass

        self.height, self.width = self.screen.getmaxyx()
        curses.resizeterm(self.height, self.width)
        self.screen.box()
        self.menu_border()
        self.screen.addstr(0, self.MENU_WIDTH, self.names[self.hlt])

        for page in self.pages:
            page.window().resize(self.height-2, self.width-self.MENU_WIDTH-1)

        panel.update_panels()
        curses.doupdate()

    def switch(self):
        hline = curses.ACS_HLINE

        self.screen.hline(0, self.MENU_WIDTH, hline, len(self.names[self.hlt]))
        self.menu_process()
        self.pages[self.hlt].top()
        self.screen.addstr(0, self.MENU_WIDTH, self.names[self.hlt])
        panel.update_panels()
        curses.doupdate()

    def current(self):
        return self.pages[self.hlt]

    def highlight(self):
        return self.hlt
