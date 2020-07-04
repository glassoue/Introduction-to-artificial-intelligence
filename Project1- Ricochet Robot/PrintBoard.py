#Graphical Implementation of Ricochet Robot based on https://github.com/sharonzhou/ricochet:
#with some modification to fit color of goal
import random

BOARD_SIZE = 16
DEBUG = True

#list_goal=['green','blue','red','yellow'] #this is what we have to modify to add more goals and also in the class
list_goal=['yellow triangle','yellow planet','yellow star','yellow moon','blue triangle','blue planet','blue star','blue moon','red triangle','red planet','red  star','red  moon','green triangle','green planet','green star','green moon']
goal_color_shape=random.choice(list_goal)
if   goal_color_shape[0] =='y':
    goal_color='yellow'
elif goal_color_shape[0] =='b':
    goal_color='blue'  
elif goal_color_shape[0] =='r':
    goal_color='red'    
elif goal_color_shape[0] =='g':
    goal_color='green'


def render_item(name):
    """Print a robot or goal name and color"""
    # color defs
    HEADER = '\033[95m'
    BLUE = '\033[1;34m'
    GREEN = '\033[1;32m'
    YEL = '\033[1;33m'
    RED = '\033[1;31m'
    ENDC = '\033[0m'
    CYAN  = "\033[1;36m"

    if name == "goal":
        
        if goal_color=='green':
            color= GREEN
        if goal_color=='red':
            color= RED
        if goal_color=='blue':
            color= BLUE
        if goal_color=='yellow':
            color= YEL
        ##color = CYAN
    elif name == "green":
        color = GREEN
    elif name == "red":
        color = RED
    elif name == "blue":
        color = BLUE
    elif name == "yellow":
        color = YEL
    else:
        color = ""
        
    return color + name[0:2].upper() + ENDC

def get_empty_board(n):
    """Render empty board, to add stuff to later"""
    board = []
    for y in range(BOARD_SIZE * 2 - 1):
        board.append([])
        for x in range(BOARD_SIZE * 2 - 1):
            if x % 2 == 0 and y % 2 == 0:
                board[y].append(" ·")  # mark a spot for a robot
            else:
                board[y].append("  ")

    return board

def draw_frame(board):
    """Draws a nice pipe boarder around a board"""
    n_rows = len(board)
    n_cols = len(board[0])
    top_row = [" ┌"] + ["——"] * n_cols + ["—┐"]
    bottom_row = [" └"] + ["——"] * n_cols + ["—┘"]

    new_board = []
    for row in board:
        new_row = [" |"] + row + [" |"]
        new_board.append(new_row)
    return [top_row] + new_board + [bottom_row]

def draw_corners(board):
    """Inserts fancy corner pipe characters"""
    for y in range(2, len(board)-2):
        for x in range(2, len(board[0])-2):
            if board[y+1][x] == " │" and board[y][x+1] == "——":
                board[y][x] = " ┌"
            elif board[y-1][x] == " │" and board[y][x+1] == "——":
                board[y][x] = " └"
            elif board[y+1][x] == " │" and board[y][x-1] == "——":
                board[y][x] = "—┐"
            elif board[y-1][x] == " │" and board[y][x-1] == "——":
                board[y][x] = "—┘"

    # handle frames as special cases
    for y in range(1, len(board)-1):
        if board[y][-2] == "——":
            board[y][-1] = "—┤"
        if board[y][1] == "——":
            board[y][0] = " ├"

    for x in range(1, len(board[2])-1):
        if board[-2][x] == " │":
            board[-1][x] = "—┴"
        if board[1][x] == " │":
            board[0][x] = "—┬"

    return board


def print_board(robots, walls, goal=None):
    """Draw the board with ascii art in a pretty way.
    There is a 'location' every 0.5 spacing.
    Each 'location' is rendered with two chars.
    robots: dictionary of name: (x,y)
    walls: list of (x,y) tuples
    goal: optional (x,y)"""
    board = get_empty_board(BOARD_SIZE)
        
    # add walls
    for x, y in walls:
        if x != int(x):  # change render based on whether x or y is between ints
            wall = " │"
        else:
            wall = "——"
        board[int(y * 2)][int(x * 2)] = wall
        
    # add goal
    if goal is not None:
        x, y = goal
        board[int(y * 2)][int(x * 2)] = render_item("goal")
        
    # add robots
    for  key, (x, y) in robots.items():
        board[int(y * 2)][int(x * 2)] = render_item(key)
        
    board.reverse()  # because list indexing is upside down
    board = draw_frame(board)
    board = draw_corners(board)

    # combine into nice string and print
    for row in board:
        print("".join(row))