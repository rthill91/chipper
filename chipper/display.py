import logging
import sys
import curses
import numpy as np


KEY_MAP = {
    '1': '1', '2': '2', '3': '3', '4': 'c',
    'q': '4', 'w': '5', 'e': '6', 'r': 'd',
    'a': '7', 's': '8', 'd': '9', 'f': 'e',
    'z': 'a', 'x': '0', 'c': 'b', 'v': 'f'
}



class Display:
    def __init__(self, width, height):
        self._logger = logging.getLogger(__name__)
        self._screen_size = (width, height)
        self._screen = curses.initscr()
        self._screen.nodelay(True)
        curses.noecho()
        self._buffer = np.zeros([width, height], dtype=bool)
        self.clear()

    def deinit(self):
        curses.nocbreak()
        self._screen.keypad(False)
        curses.echo()

    def clear(self):
        """
        Clear Display
        """
        self._screen.clear()
        for i in range(self._screen_size[0]):
            for j in range(self._screen_size[1]):
                self._screen.addstr(j, i, ' ')
        self._screen.refresh()

    def draw_pixel(self, x, y, value):
        """
        Draw value at provided (x,y) coords
        """
        self._logger.debug(f'{x=}, {y=}, {value=}')
        collision = self._buffer[x][y] & value
        value ^= self._buffer[x][y]
        if value:
            self._screen.addstr(y, x, '\u2588')
        else:
            self._screen.addstr(y, x, ' ')
        self._buffer[x][y] = value
        return collision

    def get_key_down(self):
        try:
            return KEY_MAP.get(self._screen.getkey(), None)
        except curses.error:
            return None
