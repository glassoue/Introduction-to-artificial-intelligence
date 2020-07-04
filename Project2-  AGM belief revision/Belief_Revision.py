import numpy as np
import pandas as pd
from sympy import *
from sympy import symbols
from sympy.logic.boolalg import to_cnf, Xor, And
from sympy.logic import simplify_logic
import itertools
from more_itertools import sort_together

        
class Belief():
    def __init__(self, belief):
      self.belief = to_cnf(belief)
      self.elements = self.belief.atoms()
            
    def check_eq(self, other):
        if self.belief == other.belief : 
            return True
        else :
            return False

def list_overlap(a, b):
    if type(a) == Symbol:
        w = []
        w.append(a)
        a = w

    if type(b) == Symbol:
        w = []
        w.append(b)
        b = w
    c = [*a,*b]
    
    if len(c) == len(set(c)):
        return False
    else :
        return True
def conjunction(b_base):
    a=True
    for i in range(len(b_base)):
        a=to_cnf(And(a,b_base[i].belief))
    return a
def disjunction(b_base):
    a=False
    for i in range(len(b_base)):
        a=to_cnf(Or(a,b_base[i].belief))
    return a
def conjunctionlist(blist):
    if type (blist)==Symbol:
        w=[]
        w.append(blist)
        blist=w
    a=True
    for i in range(len(blist)):
        a=to_cnf(And(a,blist[i]))
    return a
def disjunctionlist(blist):
    if type (blist)==Symbol:
        w=[]
        w.append(blist)
        blist=w
    a=False
    for i in range(len(blist)):
        a=to_cnf(Or(a,blist[i]))
    return a
                    

def add(new_bel,b_base):
    if check_newbelief(new_bel,new_bel) == False:
        print ('the new sentence is inconsistent')
        #add return to menu
        return b_base
    if b_base == []:
        b_base.append(new_bel)
        return b_base
    for i in range(len(b_base)):
        if new_bel.belief == b_base[i].belief :
            return b_base
    b_base.append(new_bel)
    return b_base

def take_elements_of_and(belief):
    if len(list(belief.atoms(And)))==0:
        return []
    expression=str(list(belief.atoms(And))[0])
    expression=expression.split("&")
    expression=sympify(expression)
    return expression

def take_elements_of_or(belief):
    if len(list(belief.atoms(Or)))==0:
        return []
    expression=str(list(belief.atoms(Or))[0])
    expression=expression.split("|")
    expression=sympify(expression)
    return expression

def resolution_elements(belief):
    operand=type(belief)
    if operand not in (And,Or):
        if operand==Not:
            expression=list(belief.atoms(Not))
            return expression
        else:
            expression=list(belief.atoms())
            return expression
    elif operand==And:
        expression=take_elements_of_and(belief)
        for i in range(len(expression)):
            if type(expression [i])==Or:
                expression[i]=take_elements_of_or(expression[i])
    else:
        expression=[take_elements_of_or(belief)]
    return expression
def resolve(ci,cj):
    #ci,cj are either lists or elements
    if type(ci)!=list:
        ci=[ci]
    if type(cj)!=list:
        cj=[cj]
    base=[]
    new=[]
    for el1 in ci:
        for el2 in cj:
            #print(ci,cj)
            if el1==Not(el2) or Not(el1)==el2:
                cw=list(filter(lambda p: p!=el1 ,ci))
                ck=list(filter(lambda p: p!=el2 ,cj))
                #print(cw,ck)
                new=cw+ck
                if len(new)==1:
                    base=base+new
                else:
                    base.append(new)
    return base
    
                
    
def take_elements_of_not(belief):
    if len(list(belief.atoms(Not)))==0:
        return []
    expression=str(list(belief.atoms(Not))[0])
    expression=expression.split("~")
    expression=sympify(expression)
    return expression


#Function to print the Belief Base  
def print_belief_base(b_base):
     if len(b_base)==0:
           print ("Empty. Try to input some new beliefs")
     else:
      for i in range(len(b_base)):
        print(b_base[i].belief)
     return True

#BELIEF REVISION FUNCTION

def belief_revision(b_base,new_bel):
    n=len(b_base)
    if n == 0:
        add(new_bel,b_base)
        return b_base
    #Check entailment of new_belief in belief base
    #Add new belief if not entailed
    if resolution(b_base,new_bel.belief) != True:
        b_base = add(new_bel,b_base)
        print('The new belief has been added to the belief base')
        print('The Belief Base is now:')

    #Call the check_newbelief function 
    for bel in b_base[0:-1]:
        if list_overlap(new_bel.elements, bel.elements ) == True:#checking which lines have elements in common
            if (check_newbelief(bel,new_bel)) == False :#calling check_newbelief just for those lines
                b_base.remove(bel)
                
    #Calling the printing function
    print ('The revised belief base is :')
    print_belief_base(b_base)
    #print('The order of the revised belief base is:')
    if len(b_base)<2:
        return b_base
    kostas = take_elements_of_and(conjunction(b_base))
    ordenk = order(kostas)
    #print(order(kostas))
    if ordenk[1][0] == len(kostas):
        print('The most plausible combination of literals is', ordenk[0][0])
        return b_base
    else:
        for j in range(len(ordenk[0])):
            b=True
            for i in range(len(ordenk[0][0])):
                b = And(b,ordenk[0][j][i])
            b = Belief(b)
            if (check_newbelief(b,b_base[-1])) == True:
                break
            
        n=len(b_base)
        for bel in b_base:
            print(bel.belief)
            if list_overlap(b.elements, bel.elements ) == True:#checking which lines have elements in common
                if (check_newbelief(b,bel)) == False :#calling check_newbelief just for those lines
                    b_base.remove(bel)
        kostas=take_elements_of_and(conjunction(b_base))
        ordenk=order(kostas)
        #print('Final order is')
        #print(order(kostas))
        print('The most plausible combination of literals is', ordenk[0][0])
        return b_base
        
# Function to check if the new belief can be True in the model    
def is_true(belief, model):
      op=type(belief)
      arg=list(belief.atoms())#only one clause
      negative = list(belief.atoms(Not))
      argmod=list(model.atoms())
      positive=[]
      submod=model
      for a in negative:
          a=list(a.atoms())
          a=a[0]
          positive.append(a)
      if op == Or:
            for a in arg:
                if list_overlap(positive, a) == True:
                    submod1=model.subs(a,0)
                else:
                    submod1=model.subs(a,1)
                if submod==True:
                    return True
                if submod!=False and submod!=True:
                    return None
                if a not in argmod:
                    submod=model
                else:
                    submod=submod1
            if submod== True:
                      return True
            elif submod == False:
                      return False
            else:
                      return True
                    
      elif op == And:
          for a in arg:
              if list_overlap(positive, a) == True:
                  submod1=submod.subs(a,0)
              else:
                  submod1=submod.subs(a,1)
              if a not in argmod:
                  if list_overlap(arg,argmod)==True:
                      
                      submod=submod
                  else:
                    return None
              else:
                    submod=submod1
          if submod !=False:
                submod=True
          return submod
      elif op == Not:
          #Only no operands 
          for a in arg:
              submod=submod.subs(a,0)
          if (submod != False and submod!=True):
             submod=None
          return submod
      else:
          #Only no operands 
          for a in arg:
              submod=submod.subs(a,1)
          if (submod != False and submod!=True):
             submod=None
          return submod
          

def check_newbelief(belief, new_belief):
    resrow=[]
    clauses = belief.belief
    new_belief = new_belief.belief
    a=take_elements_of_and(clauses)
    tipo='And'
    if len(a)==0:
        a=take_elements_of_or(clauses)
        tipo='Or'
        if len(a)!=0:
#            for i in range(len(a)):
#                a[i]=Not(a[i])
            a=[disjunctionlist(a)]    
    if len(a)==0:
        a=list(clauses.atoms(Not))
        tipo='And'
    
    if len(a)==0:
        a=list(clauses.atoms())
        tipo='And'
    a=[conjunctionlist(a)]
    

    for i in range(len(a)) :
        resrow.append(is_true(a[i],new_belief))
        #we store the result of is_true to know which sentence in the beliefbase has to be deleted
    if all([x==True or x==None for x in resrow]):
        return True
    else:
        return False

def order(b_base):
    b = b_base[0]
    truth = []
    sumtrue=[]
    elements=[]
    n=b_base[0]
    for i in range(len(b_base)):
        b = And(b,b_base[i])
    b = list(b.atoms())
    table = list(itertools.product([False, True], repeat=len(b)))
    for i in range(len(b_base)):
        truth.append([])
        
        for j in range(len(table)):
            if i==0:    
                  elements.append([])
            for k in range(len(table[j])):
                if k==0:
                    n = b_base[i].subs(b[k],table[j][k])
                else:
                    n=n.subs(b[k],table[j][k])
                if i==0:
                      if table [j][k]==False:
                            elements[j].append(Not(b[k]))
                      else:
                            elements[j].append(b[k])

            truth[i].append(n)

        if i==len(b_base)-1:
            for i, k in enumerate(truth):
             for j, item in enumerate(k):
                  if truth[i][j]==True:
                        truth[i][j]=1
                  else:
                        truth[i][j]=0
                                       
            for z in zip(*truth):
                  sumtrue.append(sum(z))
               
    m = b + table
    Z = sort_together([sumtrue,elements])[1]
    Z = Z[::-1]
    return Z,sorted(sumtrue,reverse=True)
def negation_list(listel):
    newlistel=[]
    for i in range(len(listel)):
        if type(listel[i])==list:
            newlistel.append([])
            for j in range(len(listel[i])):
                newlistel[i].append(Not(listel[i][j]))
        else:
            newlistel.append(Not(listel[i]))
    return newlistel


#CHECK IF THE NEW BELIEF IS ENTAILED IN OUR BELIEF BASE    
    
def resolution(b_base,alpha):
    base=b_base.copy()
    base.append(Belief(to_cnf(Not(alpha))))
    resolve_elements=resolution_elements(conjunction(base))
    N=len(resolve_elements)
    N1=len(resolve_elements)+1
    resolve_elements_new=resolve_elements.copy()
    l=0
    while True:
        l=l+1
        resolve_elements=resolve_elements_new.copy()
        N=len(resolve_elements)
        p=[]
        new_base=[]
        for i in range(N):
            for cj in resolve_elements[i+1:]:
                p.append((resolve_elements[i],cj))
        for (ci,cj) in p:
            b=resolve(ci,cj)
            bc=b.copy()
            print()
            if b!=None:
                if [] in b:
                    print('The function is already entailed!')
                    return True
                for r in b:
                    if r in resolve_elements:
                        bc.remove(r)
                new_base=new_base+bc
        
        if len(new_base)==0:
            return False
        resolve_elements_new=resolve_elements+new_base
        N1=len(resolve_elements_new)
    return resolve_elements
            
   
# # # a = Belief('~r|p |s')
# c= Belief('a')
# b= Belief('a|b')
# # c = Belief('~p|r')   
# # d = []   
# # # b = Belief('~s|r')
# # # e=Belief('~r')
# # f = Belief('~p')
# d = add(c,[])   
# # d = add(b,d) 
# # # d = add(b,d) 
# # # d = add(e,d) 
# # # d = add(f,d)

# d = belief_revision(d,b)
# # d = belief_revision(d,c)
# # # print(print_belief_base(d))
