#!/usr/bin/python3

from random import randint
from click.termui import clear

board = []

for x in range(10):
    board.append(["O"] * 10)
def print_board(board):
    for row in board:
        print(" ".join(row))

print_board(board)
print("The above board is the ocean and Battleships are ready for war! Provide the ships with coordiates on possible enemy vessels.\nIf it hits, you won. You have 6 missiles.")
input("\n\n\nPress Enter to continue")
clear()
def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

[ship_row,ship_col] = [random_row(board), random_col(board)]

for turn in range(7):
    if turn==6:
        print("Game Over")
        board[ship_row][ship_col] = "*"
        print_board(board)
        print([ship_row,ship_col])
        break
    print("Deploying missile %s" % (turn+1))
    guess_row = int(input("Guess Row: "))
    guess_col = int(input("Guess Col: "))

    if (guess_row == ship_row or guess_row==ship_row+1) and guess_col == ship_col:
        print("Congratulations! You sunk my battleship!")
        board[guess_row][guess_col] = "*"
        break
    
    else:
        if (guess_row < 0 or guess_row > 9) or (guess_col < 0 or guess_col > 9):
            print("Wrong guess : Out of bounds")
        elif (board[guess_row][guess_col] == "X"):
            print("This slot is already hit")
        else:
            print("You missed the battleship!")
            board[guess_row][guess_col] = "X"
        print(turn+1)
    print_board(board)    