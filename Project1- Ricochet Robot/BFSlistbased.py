# -*- coding: utf-8 -*-

import json
#from resource import *
import time
from RobotsandMoves import *
from PrintBoard import *
time_start =time.perf_counter()

#You need to change manually the initial State, goal and robot_goal (color)

Initial_state={'red': (1, 5), 'green': (5, 6), 'blue': (1, 6), 'yellow': (13, 10)} # the starting position of all 4 robots

robot_goal='green'
goal=(14,14)
#Since the dictionaries are not being optimal lists are going to be used now 
possible_directions=['left','right','up','down']
possible_robots=['red','green','blue','yellow']
Initial_state_fr=[]
Initial_state={'red': (1, 5), 'green': (5, 6), 'blue': (1, 6), 'yellow': (13, 10)} # the starting position of all 4 robots
for i in range(len(Initial_state)):
    if i==len(Initial_state):
        Initial_state_fr.append((s[Initial_state[robot_goal][0],Initial_state[robot_goal][1]],0))
    else:
        Initial_state_fr.append(Initial_state[possible_robots[i]])

frontier=[]
frontier.append(Initial_state_fr)


expanded=[] #expanded nodes
loops=0
no_of_moves=0

path_dictionary={json.dumps(Initial_state):''}
del path_dictionary
path_dictionary={json.dumps(Initial_state):''}

robot_positions=Initial_state.copy()
#The code is basically the same as BFS (see comments in BFS.py)
#solution==False or 
while loops <8:
    loops+=1
    a=0
    #A loop for the whole frontier in i
    for i in range(len(frontier)):
        #A loop for the 4 robots in every frontier [i] state
        for j in range(len(frontier[i])-1):
            robot_positions[possible_robots[j]]=frontier[i][j]
        a+=1
        if a==1:
            frontier_temp=frontier.copy()
        frontier_temp.remove(frontier[i])
        expanded.append(frontier[i])
        for robot in possible_robots:
            for direction in possible_directions:
                new_state=move_robots(robot,direction,robot_positions,g_walls,16)
                new_pos=[]
                #We save the data from the dictionary into a list
                new_state_fr=[]
                for k in range(len(new_state)):
                    if k==len(new_state):
                        new_state_fr.append((s[new_state[robot_goal][0],new_state[robot_goal][1]],frontier[i][4][1]+1))
                    else:
                        new_state_fr.append(new_state[possible_robots[k]])
                #It is checked if the new_state is inside the expanded nodes or the frontier
                if new_state_fr not in expanded and new_state_fr not in frontier_temp: 
                    frontier_temp.append(new_state_fr)
                    if loops==1:
                        path=str(loops)+'-' + robot + '-' + direction
                    else:
                        path=path_dictionary[json.dumps(robot_positions)]+ ', ' + str(loops)+'-' + robot + '-' + direction 
                        
                    path_dictionary[json.dumps(new_state)]=path
                        
                    if new_state[robot_goal] == goal:
                        #Break the loop
                        solution=True
                        time_elapsed = (time.perf_counter() - time_start)
                        print('Computer solved it in '+str(round(time_elapsed,3))+' s. Can you beat it?')
                        print(path)
                        print(str(len(expanded))+' nodes expanded, ' + str(len(frontier))+ ' nodes in the frontier')
                        break 
                if new_state[robot_goal] == goal:
                         break
                    
                if new_state[robot_goal] == goal:
                    break
            if new_state[robot_goal] == goal:
                break
        if new_state[robot_goal] == goal:
            break
    if new_state[robot_goal] == goal:
        break

    frontier=frontier_temp.copy()
