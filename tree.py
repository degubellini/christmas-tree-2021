#!/usr/bin/env python3
import curses
from curses import wrapper
import numpy as np
import time
import random


def display_matrix(screen, m, x, y):
    rows, cols = m.shape
    for row in range(rows):
        for col in range(cols):
            screen.addstr(row+x, col+y+1, "%s" % (m[row, col]))

def display_star(screen, m, x, y, mode=None):
    rows, cols = m.shape
    if mode is None:
        mode = 0
    if (mode != 1) and (mode != 0):
        mode = 0

    # if mode = 1 => light up even column on odd rows
    if mode == 1:
        for row in range(rows):
            for col in range(cols):
                if (m[row,col] != " ") and ((row % 2) != 0) and ((col % 2) == 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.COLOR_WHITE + curses.A_BOLD)
                elif (m[row,col] != " ") and ((row % 2) != 0) and ((col % 2) != 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.A_DIM)
                elif (m[row,col] != " ") and ((row % 2) == 0) and ((col % 2) != 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.COLOR_WHITE + curses.A_BOLD)
                elif (m[row,col] != " ") and ((row % 2) == 0) and ((col % 2) == 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.A_DIM)
                if m[row,col] == "O":
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.color_pair(3) + curses.A_BOLD)
                if ((m[row,col] == "/") or (m[row,col] == "\\") )and (row == 4):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.color_pair(2))

    else:
        for row in range(rows):
            for col in range(cols):
                if (m[row,col] != " ") and ((row % 2) != 0) and ((col % 2) == 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.A_DIM)
                elif (m[row,col] != " ") and ((row % 2) != 0) and ((col % 2) != 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.COLOR_WHITE + curses.A_BOLD)
                elif (m[row,col] != " ") and ((row % 2) == 0) and ((col % 2) != 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.A_DIM)
                elif (m[row,col] != " ") and ((row % 2) == 0) and ((col % 2) == 0 ):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.COLOR_WHITE + curses.A_BOLD)
                if ((m[row,col] == "/") or (m[row,col] == "\\") )and (row == 4):
                    screen.addstr(row+x, col+y+1, "%s" % (m[row, col]), curses.color_pair(2))

def display_string (screen, y, half_x, line, colors_line):
    x = half_x  - (len(line) // 2)
    line_l = list(line)
    colors_line_l = list(colors_line)

    for idx, ch in enumerate(line_l):    
        if ch != " ":
            screen.addstr(y, x, ch, curses.color_pair(int(colors_line_l[idx])) + curses.A_BOLD)
        else:
            screen.addstr(y, x, ch)
        x += 1


def random_change_ball(line, colors_line):
    perc = 10
    num_balls = ((len(line) * perc) // 100)
    if num_balls == 0:
        num_balls = 1
    indexes = random.sample(range(1, len(line)), num_balls)
    string = list(line)
    colors_string = list(colors_line)

    for idx in indexes:
        if string[idx] == " ":
            string[idx] = "o"
            colors_string[idx] = str(random.sample(range(1,8), 1)[0])

    for idx in range(1,len(line)-1):
        if idx in indexes:
            pass
        else: 
            string[idx] = " "
            colors_string[idx] == "0"
            
    line = ''.join(string)
    colors_line = ''.join(colors_string)
    return line, colors_line

def display_trunk(screen,y,half_x,tree_trunk,colors_trunk):

    for idx, line in enumerate(tree_trunk):
        (a, b) = random_change_ball(line,colors_trunk[idx])
        tree_trunk[idx] = a
        colors_trunk[idx] = b
        display_string (screen, y, half_x, line,colors_trunk[idx])
        y += 1

def build_trunk(y):

    tree_trunk = []
    colors_trunk = []

    begin = '/'
    end = '\\'
    middle = '     '
    pattern = '    '

    y_window = curses.LINES
    x_window = curses.COLS

    line = ""

    j = 1
    counter = 2
    while (y < (y_window - 2)) and ((len(line)+2) < (x_window -1)):
        counter += 1
        old_middle = middle
        if counter != 1:
            middle = middle + pattern
        line = begin + middle + end
        colors_line = '2' + middle + '2'
        colors_line = colors_line.replace(' ', '0')
        tree_trunk.append(line)
        colors_trunk.append(colors_line)
        y += 1
        if counter == 4:
            counter = 0
            middle = old_middle

    return tree_trunk, colors_trunk

def main(stdscr):
    stdscr = curses.initscr()
    curses.start_color()
    screen = stdscr
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    star = np.array(
        [
            [" "," "," ","|"," "," "," "],
            [" "," ","\\","|","/"," "," "],
            ["-","-","=","O","=","-","-"],
            [" "," ","/","|","\\"," "," "],
            ["/"," "," ","|"," "," ","\\"]
        ]
            )

    x_window = curses.COLS
    y_window = curses.LINES
    previous_x_window = x_window
    previous_y_window = y_window
    if ((x_window // 2) % 2) == 0:
        half_x = (x_window // 2) + 1
    else:
        half_x = x_window // 2

    start_star = half_x -4
    stdscr.clear()
    tree_trunk = []
    start_y = 6
    tree_trunk, colors_trunk = build_trunk(start_y)
    while True:
        try:
            y_window , x_window = stdscr.getmaxyx()
            if (previous_x_window != x_window) or (previous_y_window != y_window):
                curses.resizeterm(y_window, x_window)
                if ((x_window // 2) % 2) == 0:
                    half_x = (x_window // 2) + 1
                else:
                    half_x = x_window // 2

                start_star = half_x -4
                stdscr.clear()
                screen.refresh()
                tree_trunk = []
                start_y = 6
                tree_trunk, colors_trunk = build_trunk(start_y)
            display_star(screen, star, 1, start_star, 1)
            display_trunk(screen,start_y,half_x,tree_trunk,colors_trunk)
            screen.refresh()
            time.sleep(1)
            display_star(screen, star, 1, start_star, 0)
            display_trunk(screen,start_y,half_x,tree_trunk,colors_trunk)
            screen.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
            break

    stdscr.getkey()
    curses.nocbreak()
    curses.echo()

wrapper(main)

