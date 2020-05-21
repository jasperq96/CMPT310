#a1.py
from search import *
import random
import time

"""Changes to search.py code

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    nodes_removed = 0 #added
    while frontier:
        node = frontier.pop()
        nodes_removed += 1 #added
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node, nodes_removed #added nodes_removed
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, nodes_removed #added nodes_removed
"""

#Question 1---------------------------------------------------------------------
    
def make_rand_8puzzle():  
    board = [0,1,2,3,4,5,6,7,8]
    random.shuffle(board)
    
    puzzle = EightPuzzle(tuple(board))
    
    while not puzzle.check_solvability(board):
        random.shuffle(board)
        
    puzzle = EightPuzzle(tuple(board))
    
    return puzzle

def display(state):
    for x in range(0,9,3):
       if state[x] == 0:
           print("*",state[x+1],state[x+2])
       elif state[x+1] == 0:
           print(state[x],"*",state[x+2])
       elif state[x+2] == 0:
           print(state[x],state[x+1],"*")
       else:
           print(state[x],state[x+1],state[x+2])


#------------------------------------------------------------------------------

#Question 2--------------------------------------------------------------------

#https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
def man_dist(board):
    current = board.state
    goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    current_spot = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    dist = 0

    for i in range(len(current)):
        current_spot[current[i]] = index[i]

    for i in range(1,9):
        x_dist = abs(goal[i][0] - current_spot[i][0])
        y_dist = abs(goal[i][1] - current_spot[i][1])
        dist = dist + x_dist + y_dist

    return dist

def max_both(board):
    current_board = EightPuzzle(board.state)
    return max(man_dist(board), current_board.h(board))

for trial in range(15):
    print("Trial # : ", trial+1)
    eight_puz = make_rand_8puzzle()
    man_puz = eight_puz
    max_of_both = eight_puz

    #misplaced tile heuristic-----------------------------------
    display(eight_puz.initial)
    start_time = time.time()
    answer , removed = astar_search(eight_puz)
    elapsed_time = time.time() - start_time

    print('A*-search using the misplaced tile heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)
    #------------------------------------------------------------

    #manhattan distance heuristic--------------------------------

    start_time = time.time()
    answer , removed = astar_search(eight_puz, h=man_dist)
    elapsed_time = time.time() - start_time

    print('\n A*-search using Manhattan Distance heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)
    #------------------------------------------------------------

    #max of both-------------------------------------------------
    start_time = time.time()
    answer , removed = astar_search(eight_puz, h=max_both)
    elapsed_time = time.time() - start_time

    print('\n A*-search using max of misplaced heuristic and manhattan heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)

    #------------------------------------------------------------

#Question 3
#Class EightPuzzle from aima-python search.py was copied and modified to fit DuckPuzzle
class DuckPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)
        
        if blank < 3:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank == 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """
        top_check = [0,1,2,3]
        one = state.index(1)
        two = state.index(2)
        three = state.index(3)
        
        #check 2x2
        if one < 4 and two < 4 and three < 4:
            top_check.remove(one)
            top_check.remove(two)
            top_check.remove(three)
            if state[top_check[0]] != 0:
                return False
            if one == 0 and two != 1:
                return False
            elif one == 1 and two != 3:
                return False
            elif one == 2 and two != 0:
                return False
            elif one == 3 and two != 2:
                return False
            
            #check 2x3 even passes odd fails
            inversion = 0
            for i in range(3,len(state)):
                for j in range(i + 1, len(state)):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            return inversion % 2 == 0
        else:
            return False

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
    
    def display(self):
        for x in range(9):
            if x == 2:
                print("\n",end='')
            elif x == 6:
                print("\n",end = '  ')
            if self.initial[x] == 0:
                print("*",end = ' ')
            else:
                print(self.initial[x],end = ' ')
        print("\n")

def man_dist_duck(board):
    current = board.state
    goal = {0:[2,3], 1:[0,0], 2:[0,1], 3:[1,0], 4:[1,1], 5:[1,2], 6:[1,3], 7:[2,1], 8:[2,2]} #[row,col]
    current_spot = {}
    index = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [2,3]]
    dist = 0

    for i in range(len(current)):
        current_spot[current[i]] = index[i]

    for i in range(1,9):
        x_dist = abs(goal[i][0] - current_spot[i][0])
        y_dist = abs(goal[i][1] - current_spot[i][1])
        dist = dist + x_dist + y_dist

    return dist

def max_both_duck(board):
    current_board = EightPuzzle(board.state)
    return max(man_dist_duck(board), current_board.h(board))

def make_rand_dpuzzle():
    #Pass
    #[3,0,2,1,7,6,4,8,5]
    #[3,0,2,1,8,4,7,5,6]
    #[3,0,2,1,8,7,6,5,4]
    #[3,0,2,1,8,5,7,6,4]
    
    #Fail
    #[3,6,2,0,1,5,4,7,8]
    #[0,1,2,3,4,5,6,7,8]
    #[3,1,8,2,5,6,4,0,7]
    
    board = [0,1,2,3,4,5,6,7,8]
    random.shuffle(board)
    puzzle = DuckPuzzle(tuple(board))

    while not puzzle.check_solvability(board):
        random.shuffle(board)
        
    puzzle = DuckPuzzle(tuple(board))
    puzzle.display()
    return puzzle

print("DUCK PUZZLE BELOW\n")

for trial in range(15):
    print("Trial # : ", trial+1)
    duck_puz = make_rand_dpuzzle()
    man_puz = duck_puz
    max_of_both = duck_puz

    #misplaced tile heuristic-----------------------------------
    start_time = time.time()
    answer , removed = astar_search(duck_puz)
    elapsed_time = time.time() - start_time

    print('A*-search using the misplaced tile heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)
    #------------------------------------------------------------

    #manhattan distance heuristic--------------------------------

    start_time = time.time()
    answer , removed = astar_search(duck_puz, h=man_dist_duck)
    elapsed_time = time.time() - start_time

    print('\n A*-search using Manhattan Distance heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)
    #------------------------------------------------------------

    #max of both-------------------------------------------------
    start_time = time.time()
    answer , removed = astar_search(duck_puz, h=max_both_duck)
    elapsed_time = time.time() - start_time

    print('\n A*-search using max of misplaced heuristic and manhattan heuristic')
    print('Time Taken : ',elapsed_time,'s')
    print('Length of Solution : ', len(answer.solution()))
    print('Total # of nodes removed from frontier : ', removed)
