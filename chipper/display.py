import curses
import numpy as np


class Display:
    def __init__(self, width, height):
        self._screen_size = (width, height)
        self._screen = curses.initscr()
        self._screen.nodelay(True)
        self._buffer = np.zeros([height, width], dtype=bool)
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
                self._screen.addstr(i, j, ' ')
        self._screen.refresh()

    def draw_pixel(self, x, y, value):
        """
        Draw value at provided (x,y) coords
        """
        collision = self._buffer[x][y] & value
        value ^= self._buffer[x][y]
        if value:
            self._screen.addstr(x, y, '\u2588')
        else:
            self._screen.addstr(x, y, ' ')
        self._buffer[x][y] = value
        return collision

    def get_key_down(self):
        try:
            return self._screen.getkey()
        except curses.error:
            return None
