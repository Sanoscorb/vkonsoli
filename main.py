import screen
import vk_api

from callbacks import *


def main():
    pages = "Profile Friends Exit".split()

    token = "" # insert a token here
    api = vk_api.VkApi(token=token, api_version="5.154")
    callbacks = [UserWindow(api=api), FriendsWindow(api=api), Exit()]
    scr = screen.Screen(pages, callbacks)
    scr.loop()


if __name__ == "__main__":
    main()
