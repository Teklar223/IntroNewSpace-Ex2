import pygame as pg

pg.init()
pg.font.init()

from Src.SpaceGame import SpaceGame

import sys

if sys.platform.startswith('win'):
    # Windows platform
    # Use the Windows-specific method to get screen size
    import ctypes

    def get_screen_size():
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

elif sys.platform.startswith('linux'):
    # Linux platform
    # Use the Linux-specific method to get screen size
    import subprocess

    def get_screen_size():
        command = "xrandr | grep '*' | awk '{print $1}'"
        output = subprocess.check_output(command, shell=True).decode().strip()
        screen_width, screen_height = map(int, output.split("x"))
        return screen_width, screen_height

else:
    # Unsupported platform
    raise NotImplementedError("Unsupported platform: " + sys.platform)


def main():
    '''
        lazy start
    '''
    pg.display.set_caption("Space Game")
    screen_width, screen_height = get_screen_size()
    fullscreen_flag= pg.FULLSCREEN
    game = SpaceGame(screen_width, screen_height, fullscreen_flag)
    game.start()


if __name__ == "__main__":
    main()
