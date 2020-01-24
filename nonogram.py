import pygame as pg
import numpy as np

class Board:
    grid = []
    size = 0
        
    def __init__(self, size, top_values, left_values):
        self.size = size
        self.top_values = top_values
        self.left_values = left_values
        
        self.init_grid(size)
        self.values_sum = np.zeros((2, size), np.int8) #top - 0 row, left - 1 row
        self.total_sum = np.zeros((2, size), np.int8) #top - 0 row, left - 1 row
        self.solved = np.zeros((2, size), np.int8) #top - 0 row, left - 1 row
        self.init_count_vals()
            
    def init_grid(self, size):
        self.grid = np.zeros((size, size), np.int8)
        
    def init_count_vals(self):
        self.count_vals = np.zeros((2, self.size), np.int8)
        for i in range(self.size):
            self.count_vals[0][i] = len(self.top_values[i])
            
        for i in range(self.size):
            self.count_vals[1][i] = len(self.left_values[i])
            
        
    def draw_grid (self, gameDisplay, color):
        width = 50
        offset = 5
        for row in range (self.size):
            for col in range (self.size):
                pg.draw.rect(gameDisplay, color, (col * width + offset, row * width + offset , width, width), 1)
        for row in range (self.size):
            for col in range (self.size):
                if self.grid[row][col] == 1:
                    pg.draw.rect(gameDisplay, color, (col * width + offset, row * width + offset, width, width))
                if self.grid[row][col] == -1:
                    pg.draw.line(gameDisplay, color, (col * width + offset, row * width + offset), (col * width + 50 + offset, row * width + 50 + offset))
                    pg.draw.line(gameDisplay, color, (col * width + offset, row * width + 50 + offset), (col * width + 50 + offset, row * width + offset))
                    
    
    def fillColumn (self, col, start, number):
        for i in range(start, number + start):
            self.grid[i][col] = 1
        self.solved[0][col] = self.solved[0][col] + number
        
    def fillRow (self, row, start, number):
        for i in range(start, number + start):
            self.grid[row][i] = 1
        self.solved[1][row] = self.solved[1][row] + number
        
    def fill_blanks_vertical (self, col):
        for row in range(self.size):
            if self.grid[row][col] == 0:
                self.grid[row][col] = -1
                
    def fill_blanks_horizontal (self, row):
        for col in range(self.size):
            if self.grid[row][col] == 0:
                self.grid[row][col] = -1
        
    def solve_vertical (self, col, vals):
        pointer = 0
        
        for val in vals:
            self.fillColumn (col, pointer, val)
            pointer +=val
            if pointer < self.size:
                self.grid[pointer][col] = -1
            pointer +=1
        
        self.solved[0][col] = self.size
    
    def solve_horizontal (self, row, vals):
        pointer = 0
        for val in vals:
            self.fillRow(row, pointer, val)
            pointer +=val
            if pointer < self.size:
                self.grid[row][pointer] = -1
            pointer +=1
        self.solved[1][row] = self.size
        
    def solveEdgeRow (self):
        #top row
        first = 0
        #last = self.size - 1
        for col in range(self.size):
            if self.solved[0][col] != self.size and self.grid[first][col] == 1:
                val = self.top_values[col][first]
                self.fillColumn(col, 0, val)
                if val != self.size:
                    self.grid[col][val] == -1
        #bottom row
        for col in range(self.size):
            if self.solved[0][col] != self.size and self.grid[self.size - 1][col] == 1:
                num_values = len(self.top_values[col])
                val = self.top_values[col][num_values - 1]
                self.fillColumn(col, self.size - val, val)
                if val != self.size:
                    self.grid[col][self.size - val - 1] == -1
                    
    def solveEdgeColumn(self):
        #left column
        first = 0
        last = self.size - 1
        for row in range(self.size):
            if self.solved[1][row] != self.size and self.grid[row][first] == 1:
                val = self.left_values[row][first]
                self.fillRow(row, first, val)
                if val != self.size:
                    self.grid[row][val] == -1
                    
        for row in range(self.size):
            if self.solved[1][row] != self.size and self.grid[row][last] == 1:
                num_values = len(self.left_values[row])
                val = self.left_values[row][num_values - 1]
                self.fillRow(row, self.size - val, val)
                if val != self.size:
                    self.grid[row][self.size - val - 1] == -1
            
    def solveIntersectionMultNumbers(self):
        #top_values
        
        for col in range(self.size):
            offset = self.size - self.total_sum[0][col]            
            prev_sum = 0
            for val in self.top_values[col]:
                pos = offset
                pos += prev_sum                
                if offset < val:                    
                    self.fillColumn(col, pos, val - offset)
                prev_sum += val + 1
        
        #left_values        
        for row in range(self.size):
            offset = self.size - self.total_sum[1][row]            
            prev_sum = 0
            for val in self.left_values[row]:
                pos = offset
                pos += prev_sum                
                if offset < val:                    
                    self.fillRow(row, pos, val - offset)
                prev_sum += val + 1
                   
        
    def isSolved (self):
        solution = False
        for row in range (len(self.solved)):
            for val in self.solved[row]:
                if val == self.size:
                    solution = True
                    continue
                else:
                    solution = False
                    break
            if not solution:
                break
        return solution
    
    #Function counts number of cells that has value 1
    def countSolvedInRow(self, row):
        count = 0
        for col in range (self.size):
           if self.grid[row][col] == 1:
               count += 1
        return count
    
    def countSolvedInColumn(self, col):
        count = 0
        for row in range(self.size):
            if self.grid[row][col] == 1:
                count += 1
        
        return count
    
    def countTotalSolvedInRow(self, row):
        count = 0
        for col in range (self.size):
           if self.grid[row][col] != 0:
               count += 1
        return count
    
    def countTotalSolvedInColumn(self, col):
        count = 0
        for row in range(self.size):
            if self.grid[row][col] != 0:
                count += 1
        
        return count

    def updateSolution (self):
        for col in range(self.size):
            count = self.countTotalSolvedInColumn(col)
            self.solved[0][col] = count
        for row in range(self.size):
            count = self.countTotalSolvedInRow(row)
            self.solved[1][row] = count


    def presolver (self):
        
        #Fill intersection of single number in top_values               
        for col in range(self.size):
            sum_vals = 0
            for number in range (len(self.top_values[col])):
                #if number == 0 and self.top_values[col][number] > self.size / 2:
                   # blanks = self.size - self.top_values[col][number]
                    #self.fillColumn(col, blanks, self.top_values[col][number] - blanks)
                #calculate sum of values
                sum_vals += self.top_values[col][number]
            self.values_sum[0][col] = sum_vals
            self.total_sum[0][col] = sum_vals + self.count_vals[0][col] - 1           
        
        #Fill intersection of single number in left_values
        for row in range(self.size):
            sum_vals = 0
            for number in range (len(self.left_values[row])):
               # if number == 0 and self.left_values[row][number] > self.size / 2:
                    #blanks = self.size - self.left_values[row][number]
                    #self.fillRow (row, blanks, self.left_values[row][number] - blanks)
                sum_vals += self.left_values[row][number]
            self.values_sum[1][row] = sum_vals
            self.total_sum[1][row] = sum_vals + self.count_vals[1][row] - 1
        
        
        self.solveIntersectionMultNumbers()
                 
        #Solve edge cases
        self.solveEdgeRow()
        self.solveEdgeColumn()
        
        #Fill blanks in columns    
        for col in range(self.size):
            if self.countSolvedInColumn(col) == self.values_sum[0][col]:
                self.fill_blanks_vertical(col)
        #Fill blanks in rows
        for row in range(self.size):
            if self.countSolvedInRow(row) == self.values_sum[1][row]:
                self.fill_blanks_horizontal(row)
       
        
        
        self.updateSolution()
            
        
        
                        
    def solver (self):
        while not self.isSolved():
            
            
            self.solveEdgeRow()
            self.solveEdgeColumn()
            self.updateSolution()
            
            


        
def main():
    size = 15
    top_values = [[2, 2, 3], [2, 2, 2, 1], [6, 2, 3], [3, 1, 3, 2], [1, 3, 2, 1], [1, 3, 1, 1], [1, 4, 1, 2], [1, 2, 3, 1], [1, 1, 2, 2, 2], [2, 1, 3, 1], [4, 3, 2], [6, 5], [2, 2, 2, 1], [2, 4], [2, 1]]
    left_values = [[8], [2, 2], [5, 1, 2], [3, 4, 4], [7, 4], [2, 2, 4, 2], [4, 2, 3], [1, 2, 6], [8, 2], [3, 1], [1, 4], [3, 3], [1, 4], [2, 3, 2], [4, 2]]
    
    #size = 10
    #top_values = [[1], [1], [5, 4], [4, 2], [4, 2], [8], [1, 6], [4], [7], [6]]
    #left_values = [[5], [4], [6], [7], [1, 5], [5], [1, 5, 2], [6, 2], [1, 2], [1, 2]]
    
    board = Board(size, top_values, left_values)
    board.presolver()
    board.updateSolution()
    print (board.total_sum)

    white = (255,255,255)
    black = (0,0,0)
    
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    
    gameDisplay = pg.display.set_mode((800,800))
    gameDisplay.fill(white)
    
    board.draw_grid(gameDisplay, black)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                pg.quit()
                quit()
                
        
        pg.display.update()
    
    
if __name__== "__main__":
  main()
