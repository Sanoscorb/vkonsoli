import screen


class Example(screen.Callback):
    def setup(self):
        self.window.addstr(0, 0, "Press any key.")
        self.window.move(1, 0)
        self.window.refresh()

    def action(self):
        ch = self.window.getch()
        self.window.deleteln()
        self.window.addstr(1, 0, f"You press: {ch}")
        self.window.refresh()


class Exit(screen.Callback):
    def setup(self):
        self.window.addstr(0, 0, "Press Enter to exit.")
        self.window.refresh()

    def action(self) -> int:
        if self.window.getch() == screen.Keys.enter:
            return screen.ExitCode.endOfLoop


def main():
    screen.Screen.MENU_WIDTH = 11
    pages = ["Main Page", "Exit"]
    callbacks = [Example(), Exit()]
    scr = screen.Screen(pages, callbacks)
    scr.loop()


if __name__ == "__main__":
    main()
