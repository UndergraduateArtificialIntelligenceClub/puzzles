// Author: Justin Stevens
// Date: November 12th, 2019
// Purpose: Solves 8 queens puzzle from any starting location using stochastic hill-climbing algorithm
// Possible Improvements: ASCII Art for printing out the solution :-)
// Possible Bug Tests: With the randomness, I doubt it would get stuck in a loop, but would be good to check possible starting configs
// References: Peter Norvig's "AI: A Modern Approach" 

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#define SIZE 8

int conflict_check(int board[SIZE]){
	int counter=0;
	for(int i=0; i<SIZE; i++){
		for(int j=i+1; j<SIZE; j++){
			if(board[i]==board[j]){
				// if they lie in the same row
				counter++;
			}
			else if(abs(board[i]-board[j])==(j-i)){
				// if they lie on the same diagonal
				counter++;
			}
		}
	}
	return counter;
}

void find_best_neighbor(int board[SIZE]){
	// make a shallow copy to avoid pointers
	int neighbor[SIZE];
	for(int i=0; i<SIZE; i++){
		neighbor[i]=board[i];
	}
	// this saved variable will be used as the starting position of the column
	int saved=0;
	int best_heuristic=28; // worst possible heuristic to start

	// best_col and best_row are used as pointers for the best rows and columns
	int* best_col=(int *)malloc(1*sizeof(int));
	int* best_row=(int *)malloc(1*sizeof(int));
	// length of array is the length of the above pointers
	int length_array=1;
	for(int col=0; col<SIZE; col++){
		// start by saving the current value of the column
		saved=neighbor[col];
		for(int row=0; row<SIZE; row++){
			// for all rows that are *not* the original one
			if(row!=saved){
				// try updating it
				neighbor[col]=row;
				// check how many conflicts now
				if(conflict_check(neighbor)<best_heuristic){
					// if it decreased strictly reset array to 1
					length_array=1;
					// reset heuristic
					best_heuristic=conflict_check(neighbor);
					best_col=realloc(best_col, length_array*sizeof(int));
					best_col[0]=col;
					best_row=realloc(best_row, length_array*sizeof(int));
					best_row[0]=row;
				}
				else if(conflict_check(neighbor)==best_heuristic){
					length_array++;
					// no need to update heuristic
					best_col=realloc(best_col, length_array*sizeof(int));
					best_col[length_array-1]=col;
					best_row=realloc(best_row, length_array*sizeof(int));
					best_row[length_array-1]=row;
				}
			}
		}
		// back to what it was originally
		neighbor[col]=saved;
	}
	// initializes random number generator
	int random_swap=rand() % length_array;
	// adds some stochasticity in how we swap things up :-)
	board[best_col[random_swap]]=best_row[random_swap];	
}

bool validate_board(int board[SIZE]){
	// Make sure user enters valid input; otherwise returns false
	for(int i=0; i<SIZE; i++){
		if(board[i]<0 || board[i]>7){
			return false;
		}
	}
	return true;
}

void input_board(int board[SIZE]){
	// Prompts user to enter in a board as 8 integers
	printf("Please enter a board: ");
	for(int i=0; i<SIZE; i++){
		scanf("%d", &board[i]);
	}
}

int main(int argc, char ** argv){
	int board[SIZE];
	// Continually ask user for a new board while they haven't entered valid
	do{
		input_board(board);
	} while(!validate_board(board));
	// Track the number of times through the loop
	int iteration=0;
	// While there still are conflicts
	while(conflict_check(board) && iteration<1000){
		// Locally improve using stochastic hill-climbing algorithm
		find_best_neighbor(board);
		iteration++;
	}
	if(!conflict_check(board)){
		// Print out solution (Zeb, can you improve below here??)
		printf("Solution found on %d iteration: \n", iteration);
		for(int i=0; i<SIZE; i++){
			printf("Column %d: %d\n", i, board[i]);
		}
	}
	else{
		printf("Error: bad starting position\n");
	}
	return 0;
}