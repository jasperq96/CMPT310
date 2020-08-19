# a2_q1.py

from csp import *
import random as r

def rand_graph(probability,nodes):
    graph = {}

    for i in range(nodes):
        graph.setdefault(i,[])

    for x in range(nodes-1):
        for y in range(x+1, nodes):
            friend = r.random()
            if friend < probability:
                graph.get(x).append(y)
                graph.get(y).append(x)
                
    return graph
