import eel
import numpy  as np
import pandas as pd
import random as rd

eel.init("web")
sudoku_csv = pd.read_csv("files/sudoku.csv")

@eel.expose
def generate_sudoku():
    gen_sudoku    = []
    random_sudoku = rd.randint(0, 1000000)
    chosen_sudoku = sudoku_csv.iloc[random_sudoku]['quizzes']
    for i in range(len(chosen_sudoku)):
        if chosen_sudoku[i] == "0":
            gen_sudoku.append("")
        else:
            gen_sudoku.append(chosen_sudoku[i])
    return gen_sudoku

@eel.expose
def define_fixed_pieces(init_sudoku):
    return [piece for piece in init_sudoku if piece[0] != 0]

@eel.expose
class Piece:
    def __init__(self, value, i, j):
        self.value = value
        self.i = i
        self.j = j
        
    def check_valid(self, sudoku, fixed):
        # not 0
        if self.value == 0 or self.value > 9:
            return False
        if [self.value, self.i, self.j] in fixed:
            return True
        else:
            # test for line
            for j_aux in range(9):
                if j_aux != self.j:
                    if self.value == sudoku[self.i*9 + j_aux].value:
                        return False
            
            # test for column
            for i_aux in range(9):
                if i_aux != self.i:
                    if self.value == sudoku[i_aux*9 + self.j].value:
                        return False
            
            # test for box
            box_i, box_j = int(np.ceil((self.i+1)/3)), int(np.ceil((self.j+1)/3))
            for i_aux in range(3*(box_i - 1), 3*box_i):
                for j_aux in range(3*(box_j - 1), 3*box_j):
                    if i_aux != self.i or j_aux != self.j:
                        if self.value == sudoku[i_aux*9 + j_aux].value:
                            return False
            return True

@eel.expose         
def sudoku_solver_aux(piece, sudoku, fixed):
    num, last_value = 0, piece.value
    if last_value != 0:
        piece.value += 1
        num = last_value
    while not piece.check_valid(sudoku, fixed):
        num += 1
        if num >= 10:
            return False
        piece.value = num
    return True

@eel.expose
def sudoku_creator_aux(arr):
    final_arr = []
    for i in range(9):
        for j in range(9):
            final_arr.append([arr[i*9 + j], i, j])
    return final_arr

@eel.expose
def sudoku_solver(arr):
    sudoku_aux, sudoku, pos = sudoku_creator_aux(arr), [], 0
    for char in sudoku_aux:
        sudoku.append(Piece(char[0], char[1], char[2]))
    fixed = define_fixed_pieces(sudoku_aux)
    sudoku_change = [piece for piece in sudoku if [piece.value, piece.i, piece.j] not in fixed]
    while not sudoku_change[-1].check_valid(sudoku, fixed): 
        if sudoku_solver_aux(sudoku_change[pos], sudoku, fixed):
            pos += 1
        else:
            sudoku_change[pos].value = 0
            pos -= 1
    return [piece.value for piece in sudoku]

sudoku_board = generate_sudoku()

eel.defineSudoku(sudoku_board)()

eel.start("main.html", size=(490, 640))
