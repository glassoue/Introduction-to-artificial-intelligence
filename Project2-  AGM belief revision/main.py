# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:44:25 2020

@author: Dario
"""
import sys
from Belief_Revision import *
from time import sleep

def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

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
        if i==0:
              print("")
        print("{:d}. {:s}".format(i+1, options[i]))
        # Get a valid menu choice
    menu = 0
    while not(np.any(menu == np.arange(len(options))+1)):
        menu = inputNumber("Please choose a menu item: ")
        print("")
  
    return menu

print('Welcome to the Belief Agent\n')
print('At the moment your belief base is empty\n')
menuStart = np.array(["Initialize belief base","Print Belief Base","Check entailment","Empty belief base", "Help", "Exit"])
base = []

while True: 
    menu=display(menuStart)
    if menu==1:
        if len(base) == 0:
            m= input('Input the belief base: ')
            new_belief = Belief(m)
            base = add(new_belief,base)
            menuStart = np.array(["Add new belief","Print Belief Base","Check entailment","Empty belief base", "Help", "Exit"])
        else:
            m= input('Input the new belief: ')
            new_belief = Belief(m)
            print("Revision is running")
            # for i in range(101):
            #     progress(i)
            #     sleep(0.01)
            base = belief_revision(base,new_belief)        
              
    elif menu==2:
       
        
        print('At the moment, your belief base is:')
        print_belief_base(base)
        
    elif menu==3:
        if len(base)>0:
            entail= input('Input the sentence to entail: ')
            entail= to_cnf(entail)
            if not resolution(base,entail):
                print("The formula is not entailed")
            else:
                print("The formula is entailed")
            
        else:
            print("Input the belief base first")
    elif menu==4:  
         base.clear()
         menuStart = np.array(["Initialize belief base","Print Belief Base","Empty belief base", "Help", "Exit"])
         print("The belief base was successfully cleared")
    elif menu==5:
          print("You should input a number (1-5) in order to select an option from the menu.\
                \nIf you want to input a new belief, use small or capital letters and combine them\nwith & (AND), | (OR), ~ (NOT), >>(Implication)\
                    \nAttention the propositions in the menu base have to be input clause by clause.")
    else:
        print("Exiting...")
        sys.exit()
        