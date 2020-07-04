# -*- coding: utf-8 -*-

import json
import time
from PrintBoard import *
from RobotsandMoves import *
#Heuristic code
import numpy as np

def convert(lst): 
# this function is used to convert the path to a dictionary
    lst=lst.split('-')
    res_dct = {lst[i]: [lst[i + 1],lst[i+2]] for i in range(0, len(lst), 3)} 
    return res_dct 
    
#We initialize the dictionary that is going to contain 
#every path taken from Initial_state to the state indicated by the key
p = 0
#We initialize the Matrix S that is going to contain the Heuristic for every single point inside our playing grid.
s = np.full((16,16), 99 , int)
new_goal_hor = []
hor_wall_N = []
hor_wall_S = []
#We initialize some walls like robot_pos that is going to contain the "walls" created by each of the robots
#except for the one having to get to the goal.
#robot_pos = [(0,0) for x in range(12)]
#This are the walls from our board. Since they are located between two possible squares, their position is
#(Position square 1+ Position square 2)/2. These idea is inspired 
#from the graphical implementation of the board found online.

g_walls = [
    (6.5, 0),  # all vertical walls
    (11.5, 0),
    (2.5, 1),
    (9.5, 1),
    (5.5, 2),
    (14.5, 2),
    (9.5, 4),
    (1.5, 6),
    (12.5, 6),
    (5.5, 7),
    (6.5, 7),
    (8.5, 7),
    (6.5, 8),
    (8.5, 8),
    (2.5, 9),
    (13.5, 9),
    (6.5, 12),
    (1.5, 13),
    (10.5, 13),
    (13.5, 14),
    (3.5, 14),
    (1.5, 15),
    (9.5, 15),

    (0, 3.5),  # all horizontal walls
    (0, 9.5),
    (1, 5.5),
    (1, 13.5),
    (3, 1.5),
    (3, 8.5),
    (4, 14.5),
    (5, 2.5),
    (5, 7.5),
    (6, 11.5),
    (7, 6.5),
    (7, 8.5),
    (8, 6.5),
    (8, 8.5),
    (9, 3.5),
    (10, 1.5),
    (10, 8.5),
    (11, 12.5),
    (13, 5.5),
    (13, 8.5),
    (14, 14.5),
    (14, 2.5),
    (15, 3.5),
    (15, 11.5)

]
#Start of the block of heuristic functions:

#We are defining the functions that are needed for calculating the Heuristic.
#First of all we generate the walls for every robot but our target one with robot_walls
#def robot_walls(new_pos):
#    for i in range(0,len(new_pos),1):
#        (x,y) = new_pos[i-1]
#        #horizontal walls
#        robot_pos[0 + 4*i] =  (x, y - 0.5)
#        robot_pos[1 + 4*i] = (x, y + 0.5)
#        #vertical walls
#        robot_pos[2 + 4*i] = (x - 0.5,y)
#        robot_pos[3 + 4*i] =  (x + 0.5,y)
#    return robot_pos
    
#Then we use 'hor_wall_givenxh' to check horizontal walls on the column of the goal
def hor_wall_givenxh(xh):
    hor_wall = []
    #check the list of the walls
    for y in range(0,15,1):
        y = y + 0.5
        if g_walls.count((xh,y))!= 0 :
            hor_wall.append(y)
    return hor_wall
#Then we use 'ver_wall_givenyh' to check vertical walls on the raw of the goal
def ver_wall_givenyh(yh):
    ver_wall = []
    for x in range(0,15,1):
        x = x + 0.5
        if g_walls.count((x,yh))!= 0 :
            ver_wall.append(x)
    return ver_wall
#We use heur_ver to calculate the heuristic based only on the vertical movement.
def heur_ver(goal_ver, p):
    xh = goal_ver[0]
    yh = goal_ver[1]
    new_goal_hor = []
    hor_wall_N =[]
    hor_wall_S =[]
    pos_N = yh
    pos_S = yh
    i = 0
    p = p + 1
    hor_wall = hor_wall_givenxh(xh)
    #CONSIDER MOVING NORTH
    hor_wall_N = sorted(x for x in hor_wall if x > yh)
    #considering first of all the case of no walls up on this column
    if len(hor_wall_N) == 0 : 
        while pos_N < 15:
         pos_N = pos_N + 1
         if s[xh,pos_N] > p:
           s[xh,pos_N] = p
           new_goal_hor.append((xh,pos_N))
    else:
        N = min(hor_wall_N)
    #case with a wall above goal
        while pos_N < (N - 1):
         pos_N = pos_N + 1
         if s[xh,pos_N] > p:
           s[xh,pos_N] = p
           new_goal_hor.append((xh,pos_N))

    #CONSIDER MOVING SOUTH
    hor_wall_S = sorted(x for x in hor_wall if x < yh)
    if len(hor_wall_S) == 0 : 
        while pos_S > 0:
         pos_S = pos_S - 1
         if s[xh,pos_S] > p:
           s[xh,pos_S] = p
           new_goal_hor.append((xh,pos_S))
    else :
        S = max(hor_wall_S)
        while pos_S > (S + 0.5 ):
         pos_S = pos_S - 1
         if s[xh,pos_S] > p:
           s[xh,pos_S] = p
           new_goal_hor.append((xh,pos_S))
    #iterating for all the board
    while i < len(new_goal_hor):
        heur_hor(new_goal_hor[i], p)
        i = 1+i
        
    return s

#After calculating the heuristic for the vertical movement, we check for the heuristic with horizontal movement.
def heur_hor(goal_hor, p):
    xh = goal_hor[0]
    yh = goal_hor[1]
    new_goal_ver = []
    ver_wall = []
    ver_wall_E =[]
    ver_wall_W =[]
    pos_W = xh
    pos_E = xh
    p = p + 1
    i = 0
    ver_wall = ver_wall_givenyh(yh)
    #CONSIDER MOVING EAST
    ver_wall_E = sorted(x for x in ver_wall if x > xh)
    #considering first of all the case of no walls left on this raw
    if len(ver_wall_E) == 0 : 
        while pos_E < 15:
         pos_E = pos_E + 1
         if s[pos_E, yh] > p:
          s[pos_E, yh] = p
          new_goal_ver.append((pos_E, yh))
    else: #case with some wall on the left 
        E = min(ver_wall_E)
        while pos_E < (E - 1):
         pos_E = pos_E + 1
         if s[pos_E, yh] > p:
          s[pos_E, yh] = p
          new_goal_ver.append((pos_E, yh))

    #CONSIDER MOVING WEST
    ver_wall_W = sorted(x for x in ver_wall if x < xh)
    #considering first of all the case of no walls right on this raw
    if len(ver_wall_W) == 0 : 
        while pos_W > 0:
         pos_W = pos_W - 1
         if s[pos_W, yh] > p:
          s[pos_W, yh] = p
          new_goal_ver.append((pos_W, yh))
    else: #case with some wall on the right
        W = max(ver_wall_W)
        while pos_W > (W + 0.5):
         pos_W = pos_W - 1
         if s[pos_W, yh] > p:
          s[pos_W, yh] = p
          new_goal_ver.append((pos_W, yh)) 
    #iterating for all the board
    while i < len(new_goal_ver):
        heur_ver(new_goal_ver[i], p)
        i = 1+i
    return s

#End of the block of heuristic functions
 

#We create a function to increase the heuristic if we start at the goal or the robot is one move away from the goal.
    
def increase_heuristic(state,s,robot_goal,g_walls,path_dictionary):
    possible_directions=['left','right','up','down']
    if path_dictionary[json.dumps(Initial_state)]=='': #If the path is empty to the state that we are the increasing the heuristic of
        #then it means that it is the first time that we are using this function, therefore, we want to save the move as the first one
        #loops indicates the number of the step we are taking.
        loops=1
    else:
        #If the path is not empty then it means that the function has already been used once
        #and jwe need to indicate that it is the second step that we are taking.
        loops=2
    for direction in possible_directions:
        #we loop for all posible directions
        new_state=move_robots(robot_goal,direction,state,g_walls,16)
        #We generate a new state by moving our robot_goal to a new position saved in new_state
        if s[new_state[robot_goal][0],new_state[robot_goal][1]]>s[state[robot_goal][0],state[robot_goal][1]]:
            #If the heuristic has increased, then you can stop looping for directions
            if loops==1:
                #If it is the first move then save the no_of_step+robot that is moving+direction in which is moving
                #to then be able to show the full solution to our user
                path=str(loops)+'-' + robot_goal + '-' + direction
            else:
                #If it is not the first move then, take the move already been made from 'path_dictionary[json.dumps(state)]'
                #and add the new move.
                path=path_dictionary[json.dumps(state)]+ ', ' + str(loops)+'-' + robot + '-' + direction 
            path_dictionary[json.dumps(new_state)]=path #Path dictionary is going to save state ever explored or put into the frontier in their keys
            #and the path on how to get to it from the original state on its values.
                       
            break
    return new_state,path_dictionary
     

 
#Initial_state is going to have a format like:
# Initial_state={'red': (1, 5), 'green': (5, 6), 'blue': (1, 6), 'yellow': (13, 10)} # the starting position of all 4 robots
#where we save in a dictionary every robot color and its position.
# robot_goal='green'
#We 
# goal=(0,3)
#From Heuristic
#new_pos=[]
##We are generating "walls" for the robots that are not the robot goal
## in order to generate the heuristic. First of all we save those robot positions.
#for key in Initial_state:
#    if key != robot_goal:
#        new_pos.append(Initial_state[key])
#
#      
#robot_pos = [(0,0) for x in range(12)]
#s[goal[0],goal[1]] = 0
##Generate walls
#robot_pos=robot_walls(new_pos)
#Run heuristic.
s= heur_ver(goal, p) 
s= heur_hor(goal, p) 
#Start time counter for A* process
time_start =time.perf_counter()
#We specify posible robots and directions
possible_directions=['left','right','up','down']
possible_robots=['red','green','blue','yellow']
Initial_state_fr=[]
#In order for it to always be Initialized as empty we do this
path_dictionary={json.dumps(Initial_state):''}
del path_dictionary
path_dictionary={json.dumps(Initial_state):''}
#The number of initial moves has to be 0 if we haven't done anything
Initial_number_of_moves=0
#According to the rules, if the robot_goal is already on goal OR it is only one move away
#It cannot go directly to goal, it has to move on at least two different directions.
#In order to check this possible scenario we are going to check if the heuristic is 0 or 1
# Heuristic=0->robot_goal in goal
# Heuristic=1->robot_goal is one move away from goal.
#We need to check whether the Heuristic is 0 or 1
Initial_heuristic=s[Initial_state[robot_goal][0],Initial_state[robot_goal][1]]
#If it is bigger than 2 we don't run this part
while Initial_heuristic<2:
    if Initial_heuristic<1:
        #If it  is equal to 0 then we need to tell the user that the goal was already in the goal position
        #and in order for the program to work properly we modify the "Initial_state" to a state where the heuristic is =1
        Initial_state,path_dictionary=increase_heuristic(Initial_state,s,robot_goal,g_walls,path_dictionary)
        Initial_number_of_moves+=1
        #We increase the initial number of moves so we take into account that our original
        #initial position had been modified
        print('The robot that needed to reach the goal was already in the goal position')
        #The initial state "must" change for the A* to work properly following the rules of the game
    else:
        #If it is equal to 1 we still need to further increase the heuristic.
        if path_dictionary[json.dumps(Initial_state)]=='':
            #If the path is empty that means that  the original Initial state was 1 move away of goal
            print('The robot that needed to reach the goal was one move away from the goal position')
        #If this was not the case that would mean that  the heuristic was 0 and we had already shown
        #a message indicating that the robot_goal was in the goal position
        Initial_state,path_dictionary=increase_heuristic(Initial_state,s,robot_goal,g_walls,path_dictionary)
        Initial_number_of_moves+=1
        
    Initial_heuristic=s[Initial_state[robot_goal][0],Initial_state[robot_goal][1]]
    #We modify the Initial Heuristic 
#We create a list saving the position of the robots from the dictionary Initial_state
for i in range(len(Initial_state)):
    Initial_state_fr.append(Initial_state[possible_robots[i]])
#We initialize the frontier
frontier=[]
#We add the Initial_state to the frontier
frontier.append(Initial_state_fr)
        
#We initialize the heuristic
Heuristic=[]
#We add the initial heuristic to the Heuristic list
Heuristic.append(Initial_heuristic)
        
#We initialize the no_of_moves function, which in our case is the COST FUNCTION
No_of_moves=[]
#We add the initial number of moves to our cost function list
No_of_moves.append(Initial_number_of_moves)
#%%



#We initialize lists for the expanded nodes, expanded nodes Heuristic and expanded nodes number of moves
expanded=[] #expanded nodes
expandedH=expanded.copy()
expandedN=expanded.copy()

#Loops is going to save the number of moves being performed in each path
loops=0



robot_positions=Initial_state.copy()
#We initialize the path
path=[]
Solution=False
cutoff_no_of_moves=10
#This should be while solution==False but in order to avoid extremely time consuming 
#runs we have put a cutoff into the number of moves, which 
while loops < cutoff_no_of_moves:
    #We increase the number of moves by one
    loops=No_of_moves[0]+1
    #We always check the first state in the frontier therefore i=0
    i=0
    #Save the positions of the robot from the frontier
    for j in range(len(frontier[i])):
        robot_positions[possible_robots[j]]=frontier[i][j]
    
    #We add to the expanded nodes and remove from the frontier the node being expanded
    expanded.append(frontier[i])
    expandedH.append(Heuristic[i])
    expandedN.append(No_of_moves[i])
        
    Heuristic.remove(Heuristic[i])
    No_of_moves.remove(No_of_moves[i])
    frontier.remove(frontier[i])

    
    for robot in possible_robots:
        #We perform every possible action onto the state being expanded
        for direction in possible_directions:
            
            new_state=move_robots(robot,direction,robot_positions,g_walls,16)
            new_state_fr=[]
            for k in range(len(new_state)):
                new_state_fr.append(new_state[possible_robots[k]])
            #If the new state has not been expanded and is not in the frontier then
            if new_state_fr not in expanded and new_state_fr not in frontier:
                #Add the state to the frontier
                frontier.append(new_state_fr)
                Heuristic.append(s[new_state[robot_goal][0],new_state[robot_goal][1]])
                No_of_moves.append(loops)
            
                if loops==1:
                    #If it is the first move then you don't need to look for the moves prior to the one
                    #we are performing.
                    path=str(loops)+'-' + robot + '-' + direction
                    
                   
                else:
                    path=path_dictionary[json.dumps(robot_positions)]+ '-' + str(loops)+'-' + robot + '-' + direction 
                    
                #We create a path_dictionary saving every possible path reaching every possible node expanded
                #or in the frontier
                path_dictionary[json.dumps(new_state)]=path 
                #If we find a solution then break the loop
                if new_state[robot_goal] == goal:
                    #Break the loop
                    
                    solution=True
                    #In addition to breaking the loop, show the time it took you to find it
                    time_elapsed = (time.perf_counter() - time_start)
                    path_conv=convert(path)
                      
                      #break all?
                    break
            if new_state[robot_goal] == goal:
                break
        if new_state[robot_goal] == goal:
            break
    if new_state[robot_goal] == goal:
        break
    #We create F as the sum of Heuristic and No_of_moves
    F=[x+y for x,y in zip(Heuristic, No_of_moves)]
    zipped=zip(frontier,Heuristic,No_of_moves)
    zipped=[x for _,x in sorted(zip(F,zipped))]
    #We order the three lists (frontier, heuristic,no_of_moves) at the same time
    frontier_sort_t,Heuristic_sort_t,No_of_moves_sort_t=zip(*zipped)
    frontier_sort=list(frontier_sort_t)
    Heuristic_sort=list(Heuristic_sort_t)
    No_of_moves_sort=list(No_of_moves_sort_t)
    #We save our frontier again after ordering it and we run the while loop again
    frontier=frontier_sort.copy()
    Heuristic=Heuristic_sort.copy()
    No_of_moves=No_of_moves_sort.copy()
