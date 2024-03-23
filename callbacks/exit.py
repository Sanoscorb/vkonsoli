from screen import Callback
from screen.constants import *


class Exit(Callback):
    def setup(self):
        self.window.addstr(0, 0, "Press Enter to exit.")
        self.window.refresh()
    
    def action(self) -> int:
        if self.window.getch() == Keys.Enter:
            return ActionCode.EndOfLoop
