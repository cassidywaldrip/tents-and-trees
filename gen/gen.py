import numpy as np
import random
import csv
import copy

board_size = 8
empty = 0
tree = 1
tent = 2

def tree_available_space(board, i, j):
    if board[i][j] != 0:
        return False
    if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == 2:
        return False
    if i - 1 >= 0 and board[i - 1][j] == 2:
        return False
    if i - 1 >= 0 and j + 1 < 8 and board[i - 1][j + 1] == 2:
        return False
    if j - 1 >= 0 and board[i][j - 1] == 2:
        return False
    if j + 1 < 8 and board[i][j + 1] == 2:
        return False
    if i + 1 < 8 and j - 1 >= 0 and board[i + 1][j - 1] == 2:
        return False
    if i + 1 < 8 and board[i + 1][j] == 2:
        return False
    if i + 1 < 8 and j + 1 < 8 and board[i + 1][j + 1] == 2:
        return False
    return True

def tent_available_space(board, i, j):
    if board[i][j] != 0:
        return False
    if i - 1 >= 0 and tree_available_space(board, i - 1, j):
        return True
    if i + 1 < 8 and tree_available_space(board, i + 1, j):
        return True
    if j - 1 >= 0 and tree_available_space(board, i, j - 1):
        return True
    if j + 1 < 8 and tree_available_space(board, i, j + 1):
        return True
    return False

def get_available_tent_spaces(board, i, j):
    available_spaces = []
    if i - 1 >= 0 and tree_available_space(board, i - 1, j):
        available_spaces.append([i-1, j])
    if i + 1 < 8 and tree_available_space(board, i + 1, j):
        available_spaces.append([i+1, j])
    if j - 1 >= 0 and tree_available_space(board, i, j - 1):
        available_spaces.append([i, j-1])
    if j + 1 < 8 and tree_available_space(board, i, j + 1):
        available_spaces.append([i, j+1])
    return available_spaces

def calculate_constraints(board):
    constraints = []
    constraints.append(0)
    for i in range(len(board[0])):
        col = board[:,i]
        constraints.append(np.count_nonzero(col == 2))
    for row in board:
        constraints.append(np.count_nonzero(row == 2))

    return constraints

# returns the completed board and its constraints
def create_complete_board():
    board = np.zeros((8, 8))
    for i in range(len(board)):
        for j in range(len(board[0])):
            # place tree
            if random.uniform(0,1) < 0.3 and tent_available_space(board, i, j):
                board[i][j] = 1
                # place tent
                available_spaces = get_available_tent_spaces(board, i, j)
                choice = random.randint(0, len(available_spaces) - 1)
                board[available_spaces[choice][0], available_spaces[choice][1]] = 2

    return board, calculate_constraints(board)

# be careful - this overwrites the original board
def get_unsolved_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 2:
                board[i][j] = 0
    return board

def rotate_board_90_degrees(board):
    cp = copy.deepcopy(board)
    return np.rot90(cp)

def consolidate_data(board, constraints):
    consolidated = ""
    for i in range(9):
        consolidated += str(constraints[i])
    for i in range(len(board)):
        consolidated += str(constraints[i + 9])
        for j in range(len(board[0])):
            consolidated += str(int(board[i][j]))
    return consolidated

def main():
    all_s_boards = []
    all_u_boards = []
    for _ in range(250000):
        # Get all boards from this iteration
        board1, constraints1 = create_complete_board()
        board2 = rotate_board_90_degrees(board1)
        constraints2 = calculate_constraints(board2)
        board3 = rotate_board_90_degrees(board2)
        constraints3 = calculate_constraints(board3)
        board4 = rotate_board_90_degrees(board3)
        constraints4 = calculate_constraints(board4)

        s1_board = consolidate_data(board1, constraints1)
        all_s_boards.append(s1_board)
        unsolved_board_1 = get_unsolved_board(board1)
        u1_board = consolidate_data(unsolved_board_1, constraints1)
        all_u_boards.append(u1_board)

        s2_board = consolidate_data(board2, constraints2)
        all_s_boards.append(s2_board)
        unsolved_board_2 = get_unsolved_board(board2)
        u2_board = consolidate_data(unsolved_board_2, constraints2)
        all_u_boards.append(u2_board)

        s3_board = consolidate_data(board3, constraints3)
        all_s_boards.append(s3_board)
        unsolved_board_3 = get_unsolved_board(board3)
        u3_board = consolidate_data(unsolved_board_3, constraints3)
        all_u_boards.append(u3_board)

        s4_board = consolidate_data(board4, constraints4)
        all_s_boards.append(s4_board)
        unsolved_board_4 = get_unsolved_board(board4)
        u4_board = consolidate_data(unsolved_board_4, constraints4)
        all_u_boards.append(u4_board)

    list3 = [list(a) for a in zip(all_u_boards, all_s_boards)]
    header = ['puzzle', 'solution']

    with open("data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(list3)

if __name__ == "__main__":
    main()