import numpy as np

from RobotsandMoves import *
from PrintBoard import *
import time
import random
import sys
import importlib
import multiprocessing
from typing import Callable

        
def random_pos():
    
     
    goalsList=[(4, 14), (6,12), (3,1),(9,4),(5,2),(13,9),(1,13),(0,4),(14,14),(1,6),(11,13),(6,0),(3,9),(5,7),(10,1),(13,6)]
    center= [(14,2),(7,7),(8,7),(7,8),(8,8)]
    initial_state=[]
    while len(initial_state)<4:
       initial_position= np.random.randint(low=0,high=16,size=2 )
       # array_of_tuples = map(tuple, initial_position)
    
       tuple_of_tuples = tuple(initial_position.tolist())
       if tuple_of_tuples not in center and tuple_of_tuples not in goalsList:
           initial_state.append(tuple_of_tuples)
    Initial_state={'red': ( int(initial_state[0][0]), int(initial_state[0][1]) ) , 'green':  (int(initial_state[1][0]), int(initial_state[1][1])), 'blue':  (int(initial_state[2][0]), int(initial_state[2][1]) ), 'yellow':  (int(initial_state[3][0]), int(initial_state[3][1]))  } # the starting position of all 4 robots
    return Initial_state
# Initial_state={'red': (1, 5), 'green': (5, 6), 'blue': (1, 6), 'yellow': (13, 10)} # the starting position of all 4 robots


def print_StepByStep(path,Initial_state,global_walls,goal=None):
    
    """ display the moves in path step-by-step
    

    Parameters
    ----------
    path : Dictionary. Optimal path from Astar.""" 
    for key, [i,j] in path.items():
    
        a=move_robots(i, j, Initial_state, global_walls, BOARD_SIZE)
        print_board(a,global_walls,goal)
        print("This was move number {:s}".format(key))
        print("Robot {:s} is moving {:s}".format(i,j))
        time.sleep(6)
        Initial_state=a
    Initial_state=Initial_stateCopy
# this is just to dislpay errors
def inputNumber(prompt):

    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            print('Input invalid, please try again. You should input a number')
            pass
    return num

def display(options):

# Display menu options
    
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
        # Get a valid menu choice
    menu = 0
    while not(np.any(menu == np.arange(len(options))+1)):
        menu = inputNumber("Please choose a menu item: ")
  
    return menu

print ('Welcome to RICOCHET ROBOTS!!')
print('...')
print('A random position for robots is being generated')
print()
menuStart = np.array(["View board","Pick up a disk","Generate new robots positions", "Quit"])
list_goals=['yellow triangle','yellow planet','yellow star','yellow moon','blue triangle','blue planet','blue star','blue moon','red triangle','red planet','red  star','red  moon','green triangle','green planet','green star','green moon'] #this is what we have to modify to add more goals and also in the class
Initial_state=random_pos()
Initial_stateCopy= Initial_state.copy()


while True:
    
    
    exec(open('PrintBoard.py', encoding="utf-8").read()) #added
    #print("goal_color_shape:     ",goal_color_shape)

    menu= display(menuStart)
    
    if menu==1:
        print_board(Initial_state, global_walls)
        
        
    elif menu==2:
        
        ##picked=random.choice(list_goals)  7
        picked=goal_color_shape
        print('You picked up the ',picked )
        
        target = goals([3,1],"yellow")
        
        target.select_goal(picked)
        goal = target.p
        robot_goal = target.colour
        print ('The goal is in ',goal)
        
        print_board(Initial_state,global_walls,goal)
        print('...')
        print('Finding optimal solution...')
        print('...')
       
        print("Sorry, I didn't have coffee this morning")
        print()
        exec(open("Astar.py").read())
        
        print()
        print('Computer solved it in '+str(round(time_elapsed,3))+' s' ' and in '+str(loops)+' moves. Can you beat it?')
        decision= display(["Yes","Same moves","No"])
        
        if decision==1:
            print('Sorry, we failed. You beated a computer. THE GAME IS OVER!!')
            time.sleep(3)
            sys.exit()
        elif decision==2:
            print("Ok, let's compare our moves")
            print("I used these moves")
            print(path)
            menuStart = np.array(["View board","Pick up another disk","Generate new robots positions", "Quit"])
            print_StepByStep(path_conv,Initial_state,global_walls,goal)
            
        else:
            print()
            print('I used these moves')
            print(path)
            # print(str(len(expanded))+' nodes expanded, ' + str(len(frontier))+ ' nodes in the frontier')
            print()
            time.sleep(5)
            print('Press 4 to display every moves')
            menuStart = np.array(["View board","Pick up a disk","Generate new robots positions","Step-by-step", "Quit"])
            

            
            
    elif menu==3:
        Initial_state=random_pos()
        Initial_stateCopy= Initial_state.copy()
        print("Generating new positions...")
        print()
        time.sleep(5)
        
    elif menuStart[int(menu)-1]=="Quit":
        
        print('Exit the game...')
        time.sleep(5)
        sys.exit()
    else :
        
        print_StepByStep(path_conv,Initial_state,global_walls,goal)
        menuStart = np.array(["View board","Pick up another disk","Generate new robots positions", "Quit"])
        
    