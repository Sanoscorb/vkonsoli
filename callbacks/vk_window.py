import curses
import screen
import vk_api


class VkWindow(screen.Callback):
    def __init__(self, api: vk_api.VkApi, window: curses.window = None):
        self.api = api
        super().__init__(window)

    def setup(self):
        pass

    def action(self) -> int:
        pass
