BOARD_SIZE = 16
DEBUG = True

# (X, Y) location robot is trying to get to
default_goal = (6,1)
default_robot = "red"
#
## dict from robot color to (x,y) tuple
starting_robots = {
    "red": (1,1), 
    "green":(5,6), 
    "blue":(1,6), 
    "yellow":(0,10)
}
class goals:
 
    def __init__(self,position,colour):
      self.p = position
      self.colour=colour
      self.allp = [(4, 14), (6,12), (3,1),(9,4),(5,2),(1,6),(1,13),(0,4),(14,14),(13,9),(11,13),(6,0),(3,9),(5,7),(10,1),(13,6)]
        
        
    def select_goal(self,x):
            if x == 'yellow triangle' : 
                self.p = self.allp[0]
                self.colour="yellow"
            if x == 'yellow planet' : 
                self.p = self.allp[1]
                self.colour="yellow"
            if x == 'yellow star' : 
                self.p = self.allp[2]
                self.colour="yellow"
            if x == 'yellow moon' : 
                self.p = self.allp[3]
                self.colour="yellow"
            if x == 'blue triangle' : 
                self.p = self.allp[4]
                self.colour="blue"
            if x == 'blue planet' : 
                self.p = self.allp[5]
                self.colour="blue"
            if x == 'blue star' : 
                self.p = self.allp[6]
                self.colour="blue"
            if x == 'blue moon' : 
                self.p = self.allp[7]
                self.colour="blue"
            if x == 'red triangle' : 
                self.p = self.allp[8]
                self.colour="red"
            if x == 'red planet' : 
                self.p = self.allp[9]
                self.colour="red"
            if x == 'red  star' : 
                self.p = self.allp[10]
                self.colour="red"
            if x == 'red  moon' : 
                self.p = self.allp[11]
                self.colour="red"
            if x == 'green triangle' : 
                self.p = self.allp[12]
                self.colour="green"
            if x == 'green planet' : 
                self.p = self.allp[13]
                self.colour="green"
            if x == 'green star' : 
                self.p = self.allp[14]
                self.colour="green"
            if x == 'green moon' : 
                self.p = self.allp[15]  
                self.colour="green"


# x, y tuples
# we use .5 to denote a wall between two spaces for the robot
global_walls = [
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



        
       
   
def move_robots(robot_moving, direction, robots,walls,SIZE):
    #We need to check which robot, which direction and where is it going to end
    for key, (x,y) in robots.items():
        #Counter to check if the position has been changed at any point
        n=0
        if robot_moving==key:
            #These are debugging comments
#            print("We are moving "+key+", which is in "+str((x,y))+", in the "+direction+ " direction")
            #We save the original position
            original_position=(x,y)
            #We initialise the new_position as the original one at first
            new_position=(x,y)
            if direction == "up" or direction=="down":
                #If we are moving up or down we only need to check for horizontal walls
                for (xw,yw) in global_walls[23:len(global_walls)]:
                    if direction == "up":
#                        print(str((xw,yw)))
                        if (xw==x and yw>=y):
                            if (n==0):
                                #If we haven't changed the original position and we have a wall with a higher y than our initial position
                                #in the same column, then change the position
                                    #print("The ending position is "+str((xw,int(yw-0.5))))
                                n+=1
                                new_position=(xw,int(yw-0.5))
                            elif (new_position[1]>yw>=y):
                                #If there is more than one wall in the same row we need to make sure that 
                                #the robot is stopping in the correct position.
                                #That means that we may have skipped a wall with the way our movement works
                                #If that happened then we change the position again
                                    #print("The ending position is "+str((xw,int(yw-0.5))))
                                n+=1
                                new_position=(xw,int(yw-0.5))
                        elif xw==x:
                            #If there is no wall in our row with a higher y than our original, then we stop at the board's border
                            #print("The ending position is ("+str(SIZE-1)+","+ str(yw)+")")
                            #If we had changed the position n>0 then you don't do a thing and your stop the code with the break
                            if n>=1:
                                break
                            #The board has tiles from 0,0 to SIZE-1, SIZE-1
                            new_position=(xw,SIZE-1)
                        elif xw==x+1:
                            #print("The ending position is ("+ str(x)+","+str(SIZE-1)+")")
                            #If we had changed the position n>0 then you don't do a thing and your stop the code with the break
                            if n>=1:
                                break
                            #If not, we need to change the position for it to stop at the board's border
                            new_position=(x,SIZE-1)
                            
                            break
                        elif xw==x+2:
                            #print("The ending position is ("+ str(x)+","+str(SIZE-1)+")")
                            #If we had changed the position n>0 then you don't do a thing and your stop the code with the break
                            if n>=1:
                                break
                            #If not, we need to change the position for it to stop at the board's border
                            new_position=(x,SIZE-1)
                            
                            break
                        elif xw==SIZE-1:
                            #print("The ending position is ("+ str(x)+","+str(SIZE-1)+")")
                            #If we had changed the position n>0 then you don't do a thing and your stop the code with the break
                            if n>=1:
                                break
                            #If not, we need to change the position for it to stop at the board's border
                            new_position=(x,SIZE-1)
                            break
                    else:
                        #We do exactly the same but with opposite conditions for going down instead of up
                        if (xw==x and yw<=y):
                            
                            if (n==0):
                                n+=1
                                #print("The ending position is "+str((xw,int(yw+0.5))))
                                new_position=(xw,int(yw+0.5))
                            elif (new_position[1]<yw<=y):
                                n+=1
                                #print("The ending position is "+str((xw,int(yw+0.5))))
                                new_position=(xw,int(yw+0.5))
                        elif xw==x:
                            #print("The ending position is ("+ str(xw)+",0)")
                            if n>=1:
                                break
                            new_position=(xw,0)
                            
                        elif xw==x+1:
                            if n>=1:
                                break
                            #print("The ending position is ("+ str(x)+",0)")
                            new_position=(x,0)
                            break
                        elif xw==x+2:
                            if n>=1:
                                break
                            #print("The ending position is ("+ str(x)+",0)")
                            new_position=(x,0)
                            break
                        elif xw==SIZE-1:
                            if n>=1:
                                break
                            #print("The ending position is ("+ str(x)+",0)")
                            new_position=(x,0)
                            break
            else:
                for (xw,yw) in global_walls[0:23]:
                    #We only check for vertical walls when going right or left
                    if direction == "right":

#                        print(str((xw,yw)))
                        if (xw>=x and yw==y):
                            #We do exactly the same as in up/down but changing x for y basically
                            
                            if (n==0):
                                n+=1
                                new_position=(int(xw-0.5),yw)
#                                print(n)
#                                print(new_position)
#                                print(original_position)
                            elif (new_position[0]>xw>=x):
                                #print("The ending position is "+str((int(xw-0.5),yw)))
                                n+=1
                                new_position=(int(xw-0.5),yw)
#                                print(n)
#                                print(new_position)
#                                print(original_position)

                        elif yw==y:
                            #print("The ending position is ("+str(SIZE)+","+ str(yw)+")")
                            if n>=1:
                                break
                            new_position=(SIZE-1,yw)

                            
                        elif yw==y+1:
                            #print("The ending position is ("+str(SIZE)+","+ str(y)+")")
                            if n>=1:
                                break

                            new_position=(SIZE-1,y)

                            break
                        elif yw==y+2:
                            #print("The ending position is ("+str(SIZE)+","+ str(y)+")")
                            if n>=1:
                                break

                            new_position=(SIZE-1,y)

                            break
                        elif yw==SIZE-1:
                            #print("The ending position is ("+str(SIZE)+","+ str(y)+")")
                            if n>=1:
                                break

                            new_position=(SIZE-1,y)

                            break
                    else:
                        if (xw<=x and yw==y):
                            if (n==0):
                                #print("The ending position is "+str((int(xw+0.5),yw)))
                                n+=1
                                new_position=(int(xw+0.5),yw)
                            elif  (new_position[0]<xw<=x):
                                #print("The ending position is "+str((int(xw+0.5),yw)))
                                n+=1
                                new_position=(int(xw+0.5),yw)

                        elif yw==y:
                            #print("The ending position is (0,"+ str(yw)+")")
                            if n>=1:
                                break
                            new_position=(0,yw)
                            
                        elif yw==y+1:
                            #print("The ending position is (0,"+ str(y)+")")
                            if n>=1:
                                break
                            new_position=(0,y)
                            break
                        elif yw==y+2:
                            #print("The ending position is (0,"+ str(y)+")")
                            if n>=1:
                                break
                            new_position=(0,y)
                            break
                        elif yw==SIZE-1:
                            #print("The ending position is ("+str(SIZE)+","+ str(y)+")")
                            if n>=1:
                                break

                            new_position=(0,y)

                            break
    #After we have all positions accordingly, we need to check if we are finiding another robot in our path, if so, stop before the robot. 
    for key, (x,y) in robots.items():
        #Checking for all robots but the one we are moving....
        if robot_moving!=key:
            
            if direction == "up" and original_position[0]==x:
                if y<=new_position[1] and y>original_position[1]:
                    new_position=(original_position[0],y-1)
                
                
            elif direction=="down" and original_position[0]==x:
                if y>=new_position[1] and y<original_position[1]:
                    new_position=(original_position[0],y+1)
                    
                
            elif direction=="right" and original_position[1]==y:
                if x<=new_position[0] and x>original_position[0]:
                    new_position=(x-1,original_position[1])
            
            elif direction=="left" and original_position[1]==y:
                if x>=new_position[0] and x<original_position[0]:
                    new_position=(x+1,original_position[1])
    #print("The real ending position is "+ str(new_position))
    
    new_robots=robots.copy()
    new_robots[robot_moving]=new_position
    
    #We output the new positions of our robots
    return new_robots
    
            

    #Example
a=move_robots("yellow","down", starting_robots,global_walls,16)
