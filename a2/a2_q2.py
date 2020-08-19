# a2_q1.py

from csp import *
from a2_q1 import *
import random as r

def check_teams(graph, csp_sol):
    check = {}  # ordered by group number
    for x in csp_sol:   # x is grabbing 'key'
        check.setdefault(csp_sol[x],[]).append(x)

    for n in check:  
        group = check[n] # returns members in group n
        length = len(group)
        for i in range(length-1):
            person1 = graph[group[i]]  # grab friends list of person i in current group
            for j in range(i+1,length):
                person2 = graph[group[j]]  # grab friends list of person j in current group
                if len(person1) != 0 and len(person2) != 0: # if either has an empty list, guaranteed not friends
                    if group[j] in person1:
                        return False
    return True
