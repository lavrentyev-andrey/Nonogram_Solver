# Nonogram Solver
## Game Rules
Nonogram is a puzzle game where player have to solve grid by NxM size. Given set of numbers above and on the left of the grid, player has to determine how many squares can be placed along certain row or column. Typically, solution to the puzzle is a picture of object/person.

## Solver
Solver is divided into to parts. First part, Presolver makes following steps:
* Determines intersection where certain number always be in that position
* Uses numbers that starts from edges of the grid
* Fills row/column that fully completes that set of numbers

Second part is an actual solver in terms of the loops. The idea is to determine logic of filling rows/columns based on gaps and squares.
This part is not implemented because I cant figure out how to make this algorimn work logically. 
