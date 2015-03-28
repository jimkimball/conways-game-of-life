import curses
import curses.wrapper
from grid import Grid, OutOfBoundsException
import time
import random
import sys


class CursesScreen(object):

    def __init__(self):
        pass

    def draw_grid(self, win, g):
        for cell in g.live_cells():
            # print >> sys.stderr, "adding %d, %d" % (cell[1], cell[0])
            win.addch(cell[1], cell[0], "o")
        win.refresh()
        
    def add_new_cells(self, win, new_cells):
        for cell in new_cells:
            # print >> sys.stderr, "adding %d, %d" % (cell[1], cell[0])
            win.addch(cell[1], cell[0], "o")
            
            
    def remove_dead_cells(self, win, dead_cells):
        for cell in dead_cells:
            win.addch(cell[1], cell[0], " ")
    
    def create(self, height, width, g):
        stdscr = curses.initscr()
        begin_y = 0
        begin_x = 0
        win = curses.newwin(height, width, begin_y, begin_x)
        self.draw_grid(win, g)
        time.sleep(1)
        while(True):
            (spawning_cells, dying_cells) = g.iterate_grid()
            self.add_new_cells(win, spawning_cells)
            self.remove_dead_cells(win, dying_cells)
            win.refresh()
            time.sleep(.1)
            if g.is_empty():
                stdscr.getch()
                return

def doit(arg):
    grid_y = int(random.random() * 20 + 20)
    grid_x = int(random.random() * 40 + 60)
    # sprint >> sys.stderr, "Creating grid %d by %d" % (grid_x, grid_y)
    g = Grid(grid_x,grid_y)
    number_of_cells = int(random.random() * 200 + 300)
    i = 0
    grid_cells = []
    while i < number_of_cells:
        x = int(random.random() * grid_x)
        y = int(random.random() * grid_y)
        grid_cells.append((x,y))
        i = i + 1
    grid_cells.append((grid_x, grid_y))
    g.create_grid(grid_cells)
    # g.create_grid([(10,10), (11,11), (8,8), (8,9), (9,9), (1,1), (1,2), (0,1), (0,2), (2, 2), (2,1), (5,5), (5,6), (4,4), (4,5), (6,5), (6,6), (6,7), (8,8), (7,5), (7,6), (7,7)])
    cs = CursesScreen()
    # add 2 to x because when we fill in the lower right cell, the cursor wants to move one cell right
    cs.create(grid_y + 1, grid_x + 2, g)
    
if __name__ == "__main__":
    curses.wrapper(doit)
        