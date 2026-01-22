# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from math import prod
from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    size = cagey_grid[0]
    dom = list(range(1,size+1))

    cells = createCellVariables(size,dom)
    csp = CSP("binaryCSP",cells)

    #provides something like [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
    #these are the possible permutations of EACH TWO CELLS in same row or column
    permutations = list(itertools.permutations(dom, 2)) 

    #create constraints - row and then columns
    counter = 0 
    for i in range(size):
        row = collectCells(i,True,cells,size)
        #creates combinations of each two variable in the row
        combinations =list(itertools.combinations(row, 2))
        for pair in combinations:
            first = pair[0]
            second = pair[1]
            constraint = Constraint(f"Row{counter}",[first,second])
            constraint.add_satisfying_tuples(permutations)
            csp.add_constraint(constraint)
            counter +=1

    counter = 0 
    for j in range(size):
        column = collectCells(j,False,cells,size)
        #creates combinations of each two variable in the column
        combinations =list(itertools.combinations(column, 2)) 
        for pair in combinations:
            first = pair[0]
            second = pair[1]
            constraint = Constraint(f"Col{counter}",[first,second])
            constraint.add_satisfying_tuples(permutations)
            csp.add_constraint(constraint)
            counter +=1
    
    return csp, cells


def nary_ad_grid(cagey_grid):
    size = cagey_grid[0]
    dom = list(range(1,size+1))

    cells = createCellVariables(size,dom)
    csp = CSP("binaryCSP",cells)

    #these are the possible permutations of ALL cells in same row or column
    #[(1,2,3),(1,3,2),(2,1,3)...]
    permutations = list(itertools.permutations(dom)) 

    #create constraints - row and then columns
    for i in range(size):
        row = collectCells(i,True,cells,size)
        constraint = Constraint(f"Row{i}",row)
        constraint.add_satisfying_tuples(permutations)
        csp.add_constraint(constraint)

    for j in range(size):
        column = collectCells(j,False,cells,size)
        constraint = Constraint(f"Col{j}",column)
        constraint.add_satisfying_tuples(permutations)
        csp.add_constraint(constraint)

    return csp, cells


def cagey_csp_model(cagey_grid):
    csp, cells = nary_ad_grid(cagey_grid)
    size = cagey_grid[0]
    cages = cagey_grid[1]

    cage_domain = ['+','-','*','/','%']
    counter=0
    for cage in cages:
        cage_value = cage[0]
        cage_cells = cage[1]
        cage_op = cage[2]

        #cutting unnecessary calculations... if only one cell in cage, default to *
        #and if target is higher than what addition could provide, then it must be * too
        if cage_op == '?' and ((cage_value > len(cage_cells)*size) or (len(cage_cells) ==1)):
            cage_op = '*'
        
        #sets up constraints for cage op
        if cage_op == '?':
            csp.add_var(Variable(f"Cage{counter}",cage_domain))
        else:
            csp.add_var(Variable(f"Cage{counter}",[cage_op]))
        
        #add cage constraints

        #create domain based on size of cage, operation and target

        #create constraint: get relevant cells and the cageop, and place with domains in csp

        counter+=1


#Helper functions

#creates a list of variables for each cell, with domain based on board
def createCellVariables(size,dom):
    list = []
    for i in range(1,size+1):
        for j in range(1,size+1):
            list.append(Variable(f"Cell({i},{j})",dom))

    return list

#rowOrCol - if true means row, if false means column
#number - which row or column we want, from 0 to n-1
def collectCells(number, rowOrCol, cells, n):
    if rowOrCol:
        return cells[number*n : (number*n + n)]
    else:
        toReturn = []
        for i in range(number, 1 + number + (n*(n-1)), n):
            toReturn.append(cells[i])
        return toReturn

#get specific cell based on row and column  
def getCell(row, column, cells, n):
    return cells[(row-1)*n + column-1]


#====== Domain Creation for cages =======

#create a domain for a cage based on size of cage, operation and target
def getCageDomain(dom, cageSize, op, target):
    domain = []
    if op == '+' or op=='*':
        options = itertools.combinations_with_replacement(dom,cageSize)
    else:
        options = itertools.product(dom, repeat=cageSize)
    
    if op == '?':
        for option in options:
            for oper in ['+','*','-','/','%']:
                if checkOp(oper,target,option):
                    for perm in itertools.permutations(option):
                        domain.append((*perm, oper))
    else:
        for option in options:
            if checkOp(op,target,option):
                for perm in itertools.permutations(option):
                    domain.append((*perm, op))

#set for permutations
#optimize for + and * in the ? case
#finish - / %

def checkOp(op, target, values):
    if op == '+' and sum(values) == target:
        return True
    elif op == '*' and prod(values) == target:
        return True
    elif op == '-':
        pass
    elif op == '/':
        pass
    elif op == '%':
        pass
    return False
