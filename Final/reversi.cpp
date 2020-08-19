#include <algorithm> //to use fill_n
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <time.h>

using namespace std;

// 1 is white | 0 is black

class reversi {
public:	
	reversi(){ //Constructor to initialize the board | Don't know how to solve the green line, but still works
		for (int row = 0; row < 8; row++) {
			for (int col = 0; col < 8; col++) {
				if ((row == 3 && col == 3) ||(row == 4 && col == 4)) {
					board[row][col] = 1;
				}
				else if ((row == 3 && col == 4) || (row == 4 && col == 3)) {
					board[row][col] = 0;
				}
				else {
					board[row][col] = -1;
				}
			}
		}
	}

	void boardPrint() { 
		puts("    1   2   3   4   5   6   7   8");
		puts("  _________________________________\n");
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				if (j == 0) { printf("%d ",i+1); };
				if (board[i][j] == -1) {
					printf("|   ");
				}
				else {
					if (board[i][j] == 1) {
						printf("| W ");
					}
					else {
						printf("| B ");
					}
					
				}
			}
			puts("|");
			puts("  _________________________________\n");
		}
	}

	void play(int row, int col, bool player) {
		int num_flipped = 0;
		if ((row > 0 && col > 0) && board[row-1][col-1] == -1) { //checking if move is inside board
			if (player) {
				board[row - 1][col - 1] = 1; //player == true (represents white (1))
				num_flipped = update(row-1, col-1, player);
			}
			else {
				board[row - 1][col - 1] = 0; //player == false (represents black(0))
				num_flipped = update(row-1, col-1, player);
			}
		}
	}

	int update(int row, int col, bool player) { 
		/*
		- updates the current board, only changes colors based on current placement, 
		does not do for the tiles that get flipped as well
		- can assume move is valid
		*/
		int conquered = 0;

		int mycolor = (player) ? 1 : 0; //set mycolor to 1 if player is true, else its 0
		int opcolor = (player) ? 0 : 1;
		if (row < 7) {
			if (board[row + 1][col] == opcolor) { //downward check
				int check = 2;
				while (row + check < 8) {
					if (board[row + check][col] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row + flip][col] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (row > 0) {
			if (board[row - 1][col] == opcolor) { //upward check
				int check = 2;
				while (row - check >= 0) {
					if (board[row - check][col] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row - flip][col] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (col < 7) {
			if (board[row][col + 1] == opcolor) { //right check
				int check = 2;
				while (col + check < 8) {
					if (board[row][col + check] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row][col+flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (col > 0) {
			if (board[row][col - 1] == opcolor) { //left check
				int check = 2;
				while (col - check >= 0) {
					if (board[row][col - check] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row][col-flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (row > 0 && col < 7) {
			if (board[row - 1][col + 1] == opcolor) { //top-right check
				int check = 2;
				while (row - check >= 0 && col + check < 8) {
					if (board[row - check][col + check] == mycolor) { //dont know why, but it works for now lol
						for (int flip = 1; flip < check; flip++) {
							board[row - flip][col + flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (row > 0 && col > 0) {
			if (board[row - 1][col - 1] == opcolor) {//top-left check
				int check = 2;
				while (row - check >= 0 && col - check >= 0) {
					if (board[row - check][col - check] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row - flip][col - flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (row < 7 && col > 0) {
			if (board[row + 1][col - 1] == opcolor) {//bottom-left check
				int check = 2;
				while (row + check <= 7 && col - check >= 0) {
					if (board[row + check][col - check] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row + flip][col - flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		if (row < 7 && col < 7) {
			if (board[row + 1][col + 1] == opcolor) {//bottom-right checl
				int check = 2;
				while (row + check <= 7 && col + check <= 7) {
					if (board[row + check][col + check] == mycolor) {
						for (int flip = 1; flip < check; flip++) {
							board[row + flip][col + flip] = mycolor;
							conquered++;
						}
						break;
					}
					check++;
				}
			}
		}
		return conquered;
	}

	vector<pair<int, int>> valid_moves(bool player) { //legal move needs to flip at least one chip
		int mycolor = (player) ? 1 : 0;
		int opcolor = (player) ? 0 : 1;
		vector<pair<int, int>> moves;
		for (int row = 0; row < 8; row++) {
			for (int col = 0; col < 8; col++) {
				if (board[row][col] == -1) {
					if (row < 7) {
						if (board[row + 1][col] == opcolor) { //downward check
							int check = 2;
							while (row + check < 8) {
								if (board[row + check][col] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row + check][col] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (row > 0) {
						if (board[row - 1][col] == opcolor) { //upward check
							int check = 2;
							while (row - check >= 0) {
								if (board[row - check][col] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row - check][col] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (col < 7) {
						if (board[row][col + 1] == opcolor) { //right check
							int check = 2;
							while (col + check < 8) {
								if (board[row][col + check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row][col + check] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (col > 0) {
						if (board[row][col - 1] == opcolor) { //left check
							int check = 2;
							while (col - check >= 0) {
								if (board[row][col - check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row][col - check] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (row > 0 && col < 7) {
						if (board[row - 1][col + 1] == opcolor) { //top-right check
							int check = 2;
							while (row - check >= 0 && col + check < 8) {
								if (board[row - check][col + check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row - check][col + check] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (row > 0 && col > 0) {
						if (board[row - 1][col - 1] == opcolor) {//top-left check
							int check = 2;
							while (row - check >= 0 && col - check >= 0) {
								if (board[row - check][col - check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row - check][col - check] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (row < 7 && col > 0) {
						if (board[row + 1][col - 1] == opcolor) {//bottom-left check
							int check = 2;
							while (row + check <= 7 && col - check >= 0) {
								if (board[row + check][col - check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row + check][col - check] == -1) {
									break;
								}
								check++;
							}
						}
					}
					if (row < 7 && col < 7) {
						if (board[row + 1][col + 1] == opcolor) {//bottom-right checl
							int check = 2;
							while (row + check <= 7 && col + check <= 7) {
								if (board[row + check][col + check] == mycolor) {
									moves.push_back(make_pair(row + 1, col + 1));
									break;
								}
								else if (board[row + check][col + check] == -1) {
									break;
								}
								check++;
							}
						}
					}
				}
			}
		}
		return moves;
	}

	bool gameOver() { //returns true if game is over, false otherwise
		bool game = true;
		vector<pair<int,int>> legal_moves_p1, legal_moves_p2;
		for (int row = 0; row < 8; row++) {
			for (int col = 0; col < 8; col++) {
				if (board[row][col] == -1) {
					game = false;
				}
			}
		}
		legal_moves_p1 = valid_moves(true);
		legal_moves_p2 = valid_moves(false);
		if (legal_moves_p1.empty() && legal_moves_p2.empty()) {
			game = true;
		}

		return game;
	}

	int mypoints(bool player) {
		int mycolor = (player) ? 1 : 0;
		int points = 0;
		for (int row = 0; row < 8; row++) {
			for (int col = 0; col < 8; col++) {
				if (board[row][col] == mycolor) {
					points++;
				}
			}
		}
		return points;
	}

	void reset(int copy_board[8][8]){
		for(int i=0; i< 8; i++){
			for(int j = 0; j <8; j++){
				board[i][j] = copy_board[i][j];
			}
		}

	}

	int max_index(vector<int> move_score, int size){
		int max = move_score[0];
		int max_i = 0;
		for(int i = 0; i< size; i++){
			if(move_score[i] > max){
				max = move_score[i];
				max_i = i;
			}
		}
		vector<int> max_range;
		for(int i =0; i< size; i++){
			if(move_score[i]== move_score[max_i]){
				max_range.push_back(i);			
			}
		}
		srand(time(NULL));
		int index = rand() % max_range.size();
		return max_range[index];
	}

	int min_index(vector<int> num_conquered, int size){
		int min = num_conquered[0];
		int min_i = 0;
		for(int i = 0; i< size; i++){
			if(num_conquered[i] < min){
				min = num_conquered[i];
				min_i = i;
			}
		}
		vector<int> min_range;
		for(int i =0; i< size; i++){
			if(num_conquered[i]== num_conquered[min_i]){
				min_range.push_back(i);			
			}
		}
		srand(time(NULL));
		int index = rand() % min_range.size();
		//printf("The index picked is, %d", index);
		return min_range[index];
	}

	int space_left(){
		int taken = 0;
		for (int row = 0; row < 8; row++) {
			for (int col = 0; col < 8; col++){
				if(board[row][col] == 0){
					taken += 1;
				}
				if(board[row][col] == 1){
					taken += 1;
				}
			}

		}

		return (64 - taken);
	}






	pair<int,int> mcts(vector<pair<int,int>> pos_moves, bool player) {
	//pass in list of legal moves, dont need board since its in the class
		/*for (int i = 0; i < pos_moves.size(); i++) { //for testing purpose
			cout << pos_moves[i].first << ", " << pos_moves[i].second << endl;
		}*/

		if (pos_moves.empty()) {
			return (make_pair(-1, -1));
		}
		
		vector<int> move_score(pos_moves.size());
		int copy_board[8][8];
		vector<pair<int, int>> moves;
		bool ai = player; //this is the MCTS AI
		int ai_point;
		int player_point; //player point is actually talking about Evaporation 
		


		//copying current board contents to copy board
		for(int i=0; i< 8; i++){
			for(int j = 0; j <8; j++){
				copy_board[i][j] = board[i][j];
			}
		}

		for (int i = 0; i < pos_moves.size(); i++){
			play(pos_moves[i].first, pos_moves[i].second, player);
				

			for(int j = 0; j<500; j++){
				while(!gameOver()){
					player = !player;
					moves = valid_moves(player);
					if (moves.size()!=0){
						int index = rand() % moves.size();
						play(moves[index].first, moves[index].second, player);
					}
				}
				ai_point = mypoints(ai);
				player_point = mypoints(!ai);
				if (ai_point < player_point){
					player_point = 64 - ai_point;
				}
				else{
					ai_point = 64 - player_point;
				}
				move_score[i] += (ai_point - player_point);
				//testing purposes
				//cout << (ai_point) <<"," << (player_point) << endl;
				//for(int i =0; i< sizeof(move_score)/sizeof(move_score[0]); i++){
				//	cout << move_score[i] << endl;
				//}
				//cout <<("Completed playout") << endl;
				//boardPrint(board); // when using this function make sure to change boardPrint to accept a board, but this will cause problem in printing in main.
				reset(copy_board);	
				//boardPrint(board);			
			}
     
	}
     int n = move_score.size();
     return pos_moves[max_index(move_score, n)];
}



	pair<int,int> evaporation(vector<pair<int,int>> pos_moves, bool player){
		vector<int> num_conquered;
		int copy_board[8][8];
		int min = 0;

		if (pos_moves.empty()){
			return make_pair(-1,-1);
		}
		//copying current board state
		for(int i=0; i< 8; i++){
			for(int j = 0; j <8; j++){
				copy_board[i][j] = board[i][j];
			}
		}


		for (int i = 0; i < pos_moves.size(); i++){
			int value = update((pos_moves[i].first-1), (pos_moves[i].second-1), player);
			num_conquered.push_back(value);
			reset(copy_board);
			}
        int n = num_conquered.size();
        if(space_left() > 48){
        	return pos_moves[min_index(num_conquered, n)];
        }
	    else{
	    	return  pos_moves[max_index(num_conquered, n)];
	    }
	}
private:
	int board[8][8];	


};
