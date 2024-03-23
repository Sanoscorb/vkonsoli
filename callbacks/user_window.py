import curses
from .vk_window import VkWindow

VKUSERINFOFIELDS = "bdate,city,country,domain,sex,status,online"
VKDICTUSERKEYS = ["id", "domain", "status", "online", "first_name", "last_name"]


def userprint(win: curses.window, user: dict) -> bool:
    for key in VKDICTUSERKEYS:
        if key not in user:
            return False

    win.clear()

    win.move(0, 0)
    win.addstr("https://vk.com/{} ".format(user["domain"]))
    win.addstr("(ID: {})".format(user["id"]))

    win.move(1, 0)
    win.addstr("{} ".format(user["first_name"]))
    win.addstr("{} ".format(user["last_name"]))
    online = "(Online)" if user["online"] else "(Offline)"
    win.addstr(online)

    win.move(2, 0)
    win.attron(curses.A_ITALIC)
    if len(user["status"]) > 0:
        win.addstr("- \"{}\"".format(user["status"]))
    else:
        win.addstr("Status is empty.")
    win.attroff(curses.A_ITALIC)

    win.move(3, 0)
    if user["sex"] != 0:
        sex = "Female. " if user["sex"] == 1 else "Male. "
        win.addstr(sex)
    if "bdate" in user:
        win.addstr("Born in {}. ".format(user["bdate"]))
    if "country" in user:
        win.addstr("Lives in ")
        if "city" in user:
            win.addstr("{}, ".format(user["city"]["title"]))
        win.addstr("{}.".format(user["country"]["title"]))


class UserWindow(VkWindow):
    def setup(self):
        vk = self.api.get_api()
        users = vk.users.get(fields=VKUSERINFOFIELDS)
        userprint(self.window, users[0])

    def action(self):
        pass
