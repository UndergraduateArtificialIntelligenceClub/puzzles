#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

int conflict_check(int board[8]){
	int counter=0;
	for(int i=0; i<8; i++){
		for(int j=i+1; j<8; j++){
			if(board[i]==board[j]){
				// printf("row: %d=%d, %d %d", board[i], board[j], i, j);
				// if they lie in the same row
				counter++;
			}
			else if(abs(board[i]-board[j])==(j-i)){
				// if they lie on the same diagonal
				// printf("%d-%d=%d-%d\n", board[i], board[j], j, i);
				//printf("diag: %d %d", i, j);
				counter++;
			}
		}
	}
	// printf("Number of conflicts is: %d\n", counter);
	return counter;
}

void find_best_neighbor(int board[8]){
	// make a shallow copy to avoid pointers
	int neighbor[8];
	for(int i=0; i<8; i++){
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
	for(int col=0; col<8; col++){
		// start by saving the current value of the column
		saved=neighbor[col];
		for(int row=0; row<8; row++){
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
	// printf("Heuristic: %d\n", best_heuristic);
	
}

bool validate_board(int board[8]){
	for(int i=0; i<8; i++){
		if(board[i]<0 || board[i]>7){
			return false;
		}
	}
	return true;
}

void input_board(int board[8]){
	printf("Please enter a board: ");
	for(int i=0; i<8; i++){
		scanf("%d", &board[i]);
	}
}

int main(int argc, char ** argv){
	int board[8];
	do{
		input_board(board);
	} while(!validate_board(board));
	int iteration=0;
	while(conflict_check(board)){
		find_best_neighbor(board);
		iteration++;
	}
	printf("Solution found on %d iteration: \n", iteration);
	for(int i=0; i<8; i++){
		printf("Column %d: %d\n", i, board[i]);
	}
	return 0;
}