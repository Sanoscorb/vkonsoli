import enum
import screen
import vk_api
from .user_window import *


class VisiblePage(enum.Enum):
    Choice = 0
    Profile = 1


class FriendsWindow(UserWindow):
    def __init__(self, window: curses.window = None, api=vk_api.VkApi):
        self.hlt = 0
        self.users = []
        self.names = []
        self.page_is = VisiblePage.Choice
        super().__init__(api, window)

    def setup(self):
        vk = self.api.get_api()
        users = vk.friends.get(order="name")
        user_ids = ""
        for user in users["items"]:
            user_ids += str(user) + ","
        self.users = vk.users.get(fields=VKUSERINFOFIELDS, user_ids=user_ids)
        
        for user in self.users:
            self.names.append(user["first_name"] + " " + user["last_name"])
        
        screen.list_output(self.window, 0, 0, self.names, self.hlt)

    def action(self):
        ch = self.window.getch()
        if self.page_is == VisiblePage.Choice:
            match ch:
                case curses.KEY_UP:
                    if self.hlt > 0:
                        self.hlt -= 1
                    screen.list_output(self.window, 0, 0, self.names, self.hlt)

                case curses.KEY_DOWN:
                    if self.hlt < len(self.names) - 1:
                        self.hlt += 1
                    screen.list_output(self.window, 0, 0, self.names, self.hlt)

                case screen.Keys.Enter:
                    self.window.clear()
                    userprint(self.window, self.users[self.hlt])
                    self.window.refresh()
                    self.page_is = VisiblePage.Profile

        if self.page_is == VisiblePage.Profile:
            if ch == screen.Keys.Escape:
                self.window.clear()
                screen.list_output(self.window, 0, 0, self.names, self.hlt)
                self.window.refresh()
                self.page_is = VisiblePage.Choice
