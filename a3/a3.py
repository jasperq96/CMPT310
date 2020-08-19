# a3.py
import random as r
import math
import copy as c

""" TESTING CODE

Code to test display()
test_boards = [rand_board(9),rand_board(9),rand_board(9),rand_board(9)]
display(default)
for boards in test_boards:
	print("\n")
	display(boards)

"""

""" GAME INSTRUCTIONS
	-Player is X, value 1
	-Computer is O, value 0
	-Board is displayed, with tiles showing up as integers from 1-9, respectively.
	-Player inputs an integer corresponding to their desired spot, if there's no conflicts an "X" will be placed and the computer
	 will then take its turn. If a conflict occurs with player chosen tile, they will be asked to choose again.
	-Computer Wins heuristic value is 1, loss -1, tie 0.
"""

# def rand_board(nodes): 	#for testing board display
#     board = {}

#     for i in range(nodes):
#     	state = r.random()
#     	if state <= 0.3:
#     		tile_state = -1
#     	elif state > 0.3 and state <= 0.6:
#     		tile_state = 0
#     	else:
#     		tile_state = 1
#     	board.setdefault(i+1, tile_state)
           
#     return board 

def display(state):
	counter = 0
	rows = 0
	print("\n")
	for x in state:
		if state[x] == -1:
			if counter == 2:
				print("", x)
			else:
				print("", x,"|", end='')

		elif state[x] == 0:
			if counter == 2:
				print(" O")
			else:
				print(" O |", end='')

		elif state[x] == 1:
			if counter == 2:
				print(" X")
			else:
				print(" X |", end='')

		counter += 1

		if counter == 3 and rows < 2:
			print("\n---+---+---\n")
			counter = 0
			rows += 1

def valid_move(move, state):
	if not move.isdigit():
		return False
	move = int(move)
	if move < 1 or move > 9 or state[move] != -1:
		return False
	return True

def result(tile, state):
	state[tile] = 1
	return state

def AI_result(tile, state, playouts):
	if not playouts:
		print("It is the Computer's turn, it chose: ", tile)
	state[tile] = 0
	return state

def legal_moves(state):
	moves = []
	for x in state:
		if state[x] == -1:
			moves.append(x)
	return moves


def AI_move(moves, state): #implement AI future moves
	best_move = Monte_Carlo_Tree_Search(moves, state)
	board = AI_result(best_move, state, False)
	#board = AI_result(moves[r.randint(0, len(moves)-1)],state) #for testing random moves by AI
	return board

def gameOver(state, playouts):
	occupied_tiles = 0
	for x in state:
		tile_val = state[x]
		verdict = False
		if tile_val != -1:
			occupied_tiles += 1
			if x == 1:
				if (state[x+1] == tile_val and state[x+2] == tile_val) or (state[x+3] == tile_val and state[x+6] == tile_val) or (state[x+4] == tile_val and state[x+8] == tile_val): 
					verdict =  True
					break
			if x == 2 or x == 3:
				if (state[x+3] == tile_val and state[x+6] == tile_val) or (x == 3 and state[x+2] == tile_val and state[x+4] == tile_val):
					verdict =  True
					break
			if x == 4 or x == 7:
				if(state[x+1] == tile_val and state[x+2] == tile_val):
					verdict = True
					break
	if verdict:
		if tile_val == 0:
			if not playouts:
				print("Computer Wins! Better Luck Next Time!")
			return True, 1
		else:
			if not playouts:
				print("You Win! Congratulations!")
			return True, -1
	elif occupied_tiles == 9:
		if not playouts:
			print("Looks like it's a Tie!")
		return True, 9

	return False, 0

def Monte_Carlo_Tree_Search(moves, state):
	# moves = list of all avaiable spots
	# state is the current board state

	move_score = {}
	player_turn = True

	for x in moves:
		move_score.setdefault(x,0) #dict keys represent tiles that are legal

	for move in moves:
		#print("On Tile: ", move)
		for x in range(2000):
			copy_moves = c.deepcopy(moves)
			copy_state = c.deepcopy(state)
			#initial_random_move = r.randint(0,len(copy_moves)-1)
			copy_state = AI_result(move, copy_state, True)
			copy_moves.remove(move)
			game , game_value = gameOver(copy_state, True)
			#print("Game is: ", game)
			while len(copy_moves) > 0 and not game:
				#print("Current Copy: ", copy_moves)
				if player_turn:
					random_player_move = r.randint(0,len(copy_moves)-1)
					copy_state = result(copy_moves[random_player_move],copy_state)
					#print("Player chose", copy_moves[random_player_move])
					copy_moves.pop(random_player_move)
					player_turn = False
				else:
					random_AI_move = r.randint(0,len(copy_moves)-1)
					copy_state = AI_result(copy_moves[random_AI_move], copy_state, True)
					#print("Computer chose", copy_moves[random_AI_move])
					copy_moves.pop(random_AI_move)
					player_turn = True
				
				#print(copy_moves)

				game , game_value = gameOver(copy_state, True)

			move_score[move] += game_value * (len(copy_moves)+1)

	#print("Scores: ", move_score)
	return max(move_score, key = move_score.get)

def play_a_new_game():
	board = {1:-1, 2:-1, 3:-1,
			 4:-1 ,5:-1, 6:-1,
			 7:-1, 8:-1, 9:-1,}

	#playing = True
	player_turn = True
	turns = 0
	end = False
	useless = 0

	start = input("Would you like to go First (1) or Second (2)? (input number): ")
	while not start.isdigit() or (start != '1' and start != '2'):	#fix arguments
		start = input("Please Type '1' to go first, or '2' to go second: ")

	if start == "2":
		player_turn = False

	print("Starting Board")
	display(board)


	while not end:
		if player_turn:
			player_move = input("Choose an Empty Tile (Has a number 1-9): ")
			while not valid_move(player_move, board):
				player_move = input("Please Choose a valid Empty Tile (Has a number 1-9): ")
			board = result(int(player_move), board)
			player_turn = False
		else:
			moves = legal_moves(board)
			board = AI_move(moves, board)
			player_turn = True

		turns += 1
		display(board)
		end, useless = gameOver(board, False)

if __name__ == '__main__':
  play_a_new_game()