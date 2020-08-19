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
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        conflict = count(conflict(v) for v in self.neighbors[var])
        self.conflicts += conflict
        return conflict

    def display(self, assignment):
        # Subclasses can print in a prettier way, or display with a GUI
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
# Constraint Propagation with AC-3


def AC3(csp, queue=None, removals=None):
    arc_removed = 0
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        arc_removed += 1
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, arc_removed


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

# ______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering


def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    return argmin_random_tie(
        [v for v in csp.variables if v not in assignment],
        key=lambda var: num_legal_values(csp, var, assignment))


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0
                     for val in csp.domains[var])

# Value ordering


def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)


def lcv(var, assignment, csp):
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))

# Inference


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    return AC3(csp, {(X, var) for X in csp.neighbors[var]}, removals)

# The search, proper


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

# ______________________________________________________________________________
# Min-conflicts hillclimbing search for CSPs


def min_conflicts(csp, max_steps=100000):
    # Generate a complete assignment for all variables (probably with conflicts)
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
    return argmin_random_tie(csp.domains[var],
                             key=lambda val: csp.nconflicts(var, val, current))

def argmin_tie(seq, key=identity):
    # not random shuffle people in a random group 
    return min(seq, key=key)

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


	variable = list(range(0,len(graph)))

	domain = {} 

	pos_val = [] 

	for i in range(len(variable)):
		pos_val.append(i)

		for j in range(len(variable)):
			domain.setdefault(j, pos_val)

		ice_break = CSP(variable,domain,graph,constraints)
		arcs_removed = AC3(ice_break)
		grouping = backtracking_search(ice_break, mrv, lcv, mac)
		total_assigned += ice_break.nassigns
		total_unassigned += ice_break.nunassigns
		if grouping != None:
			break
	
	total_groups = num_teams(grouping)

	return grouping, total_assigned, total_unassigned, total_groups, arcs_removed

def run_q3():

	for x in range(5):
		print("Test Round ", x+1)
		graphs = [rand_graph(0.1, 31), rand_graph(0.2, 31), rand_graph(0.3, 31), rand_graph(0.4, 31), rand_graph(0.5, 31), rand_graph(0.6, 31)]
		for i in graphs:
			start_time = t.time()
			solution, total_assigned, total_unassigned, total_groups, arcs_removed = solve(i)
			elapsed_time = t.time()-start_time
			print("---------------------------------------------------------------------------")
			print("Graph: ", i)
			print("sol:", solution)
			print("Time taken to solve (in seconds) : ", elapsed_time)
			print("Total CSP Varialbes Assigned : ", total_assigned)
			print("Total CSP Variables Unassigned : ", total_unassigned)
			print("Total Arcs Removed from Domain : ", arcs_removed[1])
			print("Total Groups : ", total_groups)

if __name__ == "__main__":
	run_q3()