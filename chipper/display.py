import curses

class Display:
    def __init__(self, width, height):
        self._screen_size = (width, height)
        self._screen = curses.initscr()
        self.clear()

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
        self._screen.addstr(y, x, value)


if __name__ == '__main__':
    d = Display(32, 64)
    d.draw_pixel(0, 1, 'T')
    d._screen.getch()
