from csp import *
from a2_q1 import *
from a2_q2 import *
import random as r
import time as t

""" The code underneath is the entire csp.py file 

from utils import argmin_random_tie, count, first
import search

from collections import defaultdict
from functools import reduce

import itertools
import re
import random


class CSP(search.Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.nunassigns = 0
        self.conflicts = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):

        if var in assignment:
            del assignment[var]
            self.nunassigns += 1

    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        conflict = count(conflict(v) for v in self.neighbors[var])
        self.conflicts += conflict
        return conflict

    def display(self, assignment):
        print(assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var] 

    def infer_assignment(self):
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# ______________________________________________________________________________
# Min-conflicts hillclimbing search for CSPs


def min_conflicts(csp, max_steps=100000):
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None

identity = lambda x: x


def min_conflicts_value(csp, var, current):
    return tieBreaker(csp.domains[var], key=lambda val: csp.nconflicts(var, val, current))

def tieBreaker(seq, key=identity):
    return min(seq, key=key)

# ______________________________________________________________________________
# Constraint Propagation with AC-3


def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

# ______________________________________________________________________________

"""


def constraints(A,a,B,b):
    return a != b
    
def num_teams(solution):
	group = {}
	for x in solution:
		group.setdefault(solution[x],[]).append(x)	#separate into groups
	return len(group)

def solve(graph):

	total_assigned = 0
	total_unassigned = 0
	total_groups = 0
	total_conflicts = 0


	variable = list(range(0,len(graph)))

	domain = {} 

	pos_val = [] 

	for i in range(len(variable)):
		pos_val.append(i)

	for j in range(len(variable)):
		domain.setdefault(j, pos_val)

	ice_break = CSP(variable,domain,graph,constraints)
	grouping = min_conflicts(ice_break)
 
	total_conflicts = ice_break.conflicts
	
	total_groups = num_teams(grouping)

	return grouping, ice_break.nassigns, ice_break.nunassigns, total_groups, total_conflicts

def run_q4():

	for x in range(5):
		print("\n\nTest Round ", x+1)
		graphs = [rand_graph(0.1, 105), rand_graph(0.2, 105), rand_graph(0.3, 105), rand_graph(0.4, 105), rand_graph(0.5, 105), rand_graph(0.6, 105)]
		for i in graphs:
			start_time = t.time()
			solution, total_assigned, total_unassigned, total_groups, total_conflicts = solve(i)
			elapsed_time = t.time()-start_time
			print("---------------------------------------------------------------------------")
			print("Time taken to solve (in seconds) : ", elapsed_time)
			print("Total CSP Varialbes Assigned : ", total_assigned)
			print("Total CSP Variables Unassigned : ", total_unassigned)
			print("Total Conflicts Occurred : ", total_conflicts)
			print("Total Groups : ", total_groups)

if __name__ == "__main__":
    run_q4()