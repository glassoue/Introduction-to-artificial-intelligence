# -*- coding: utf-8 -*-

import json
#from resource import *
import time
#import resource
from RobotsandMoves import *
from PrintBoard import *
time_start =time.perf_counter()

#You need to change manually the initial State, goal and robot_goal (color)
Initial_state={'red': (1, 5), 'green': (5, 6), 'blue': (1, 6), 'yellow': (13, 10)} # the starting position of all 4 robots
frontier=[Initial_state]
goal=(14,14)
expanded=[] #expanded nodes
loops=0
robot_goal='yellow'
path_dictionary={json.dumps(Initial_state):''}
del path_dictionary
path_dictionary={json.dumps(Initial_state):''}
possible_directions=['left','right','up','down']
possible_robots=['red','green','blue','yellow']
#solution==False or 
cutoff=10
while loops <cutoff:
    #We increase the number of steps (loops) in 1 every time we explore a new level of depth in the graph
    loops+= 1
    a=0
    #We loop for every position in the frontier
    for robot_positions in frontier:
        #In order to copy the frontier into a temporal saving space (frontier_temp)
        a+=1
        #We distinguish the first run of the loop to the rest of them.
        if a==1:
            frontier_temp=frontier.copy()
        #We delete from frontier the position that we have just explored
        frontier_temp.remove(robot_positions)
        #We add to the expanded nodes the position that just have been explored
        expanded.append(robot_positions)
        #For every color and every direction
        for robot in possible_robots:
            for direction in possible_directions:

                #Compute the movement of the robots
                new_state=move_robots(robot,direction,robot_positions,global_walls,16)
                #If this new state is not contained in expanded and not contained in frontier then 
                if new_state not in expanded and new_state not in frontier_temp : 
                  frontier_temp.append(new_state)
                  #We add the new state to the frontier
                  if loops==1:
                      #If it was the Initial_state then save the number of steps, color moved and direction
                      path=str(loops)+'-' + robot + '-' + direction
                  else:
                      #If it was not the initial state then take the path taken to that position and add the new step
                      path=path_dictionary[json.dumps(robot_positions)]+ ', ' + str(loops)+'-' + robot + '-' + direction 
                  path_dictionary[json.dumps(new_state)]=path
                  #If the goal is reached we stop all loops and show path, number of nodes expanded,
                  #number of nodes in the frontier and the time it took to reach it.
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
    #We change the frontier after the loop is ran completely with the new states.
    frontier=frontier_temp.copy()
