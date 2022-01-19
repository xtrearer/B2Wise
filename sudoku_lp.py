import pulp as plp
import csv

""" Global Variables """
rows = range(0, 9)
cols = range(0, 9)
grids = range(0, 9)
values = range(1, 10)
""" ---------------- """


def solve(path):
    input_sudoku = read_sudoku(path=path)
    print(f'\n### Input Sudoku ###\n')
    print_matrix(input_sudoku)
    print('\n####################\n')

    solved_sudoku = solve_sudoku_lp(input_sudoku)
    print(f'\n### Solved Sudoku ###\n')
    print_matrix(solved_sudoku)
    print('\n####################\n')

    output_path = f"out/{path.split('/')[-1].split('.csv')[0]}_solved_lp.csv"
    write_sudoku(path=output_path, solved_sudoku=solved_sudoku)
    print(f'Solved sudoku results have been written to "{output_path}"')


def print_matrix(solved_sudoku):
    for row in rows:
        print(' '.join([f'{value}' for value in solved_sudoku[row]]))


def read_sudoku(path):
    with open(path, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        return [[int(value) for value in row] for row in csv_reader]


def write_sudoku(path, solved_sudoku):
    with open(path, mode='w', newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
        csv_writer.writerows(solved_sudoku)


def solve_sudoku_lp(input_sudoku):
    problem = plp.LpProblem("sudoku")

    """ There is no Min / Max Objective for this, so the Objective is set to a Dummy Function of 0. """
    objective = plp.lpSum(0)
    problem.setObjective(objective)

    """
    Creates a LpVariable for each possible value, for each cell of the 9x9 grid, represented as a Binary (0 or 1). 
    So for the first cell, there will be 9 Binary LpVariables, each representing the possible values of 1 through 9.
    These LpVariables acts as the unknowns that will be solved by the CBC Algorithm to reach the Optimal solution 
    for the Constraints we will be providing. 
    """
    grid_vars = plp.LpVariable.dicts("grid_value", (rows, cols, values), cat='Binary')

    """
    Constraint 1: 

    Checks that each cell may only have 1 value. Since it is possible for some Sudoku puzzles to have more than one 
    solution, this constraint is used to stick to the first one it finds. It does this by setting the constraint as 
    a formula, that Sums the Binary values for each of the potential values for each cell. The aim of the constraint 
    is that this Sum should be equal to 1, indicating that only one of the potential 9 values has been set for that cell.

    More on how this works below.
    """
    for row in rows:
        for col in cols:
            problem += (plp.lpSum([grid_vars[row][col][value] for value in values]) == 1, f"constraint_sum_{row}_{col}")

    """
    Constraint 2:

    Ensures that values from 1 to 9 is filled only once in a row. This is done by Summing the product of
    the Binary value of each cell of the row, for the given value, with the value itself. The constraint is met if this
    Sum equals the input value. This is best understood with a short example:

    Let's say the row is [1,    2,    3].

    The representation of this row using our LpVariable Dictionary with Binary Values would look like this:

    [cell0           ,  cell1          , cell2             ]
    [{1: 1, 2:0, 3:0},  {1:0, 2:1, 3:0},    {1:0, 2:0, 3:1}]

    In the first element of the list, Value=1 has a binary value of 1. This represents that it is the active value for that position.
    So the constraint here will do the following:

    cell0[value=1] = Binary Value of 1.
    cell1[value=1] = Binary Value of 0.
    cell2[value=1] = Binary Value of 0.

    So the constraint below would Sum...
    -> cell0[value=1] x value=1 + cell1[value=1] x value=1 + cell2[value=1] x value=1
    -> 1 x 1 + 0 x 1 + 0 x 1 = 1 which equals the input value of 1.

    The Constraint is setup so that the formula should be solved that it equals the Value. 
    """
    for row in rows:
        for value in values:
            problem += (plp.lpSum([grid_vars[row][col][value] * value for col in cols]) == value, f"constraint_uniq_row_{row}_{value}")

    """
    Constraint 3:

    Ensures that values from 1 to 9 is filled only once in a column. Same as Constraint 3, just on the columns.
    """
    for col in cols:
        for value in values:
            problem += (plp.lpSum([grid_vars[row][col][value] * value for row in rows]) == value, f"constraint_uniq_col_{col}_{value}")

    """
    Constraint 4:

    Ensures that values from 1 to 9 is filled only once in the 3x3 sub grids. The same Summing of the product of the Value and its 
    corresponding Binary Value is made for each each cell in the sub grid.
    """
    for grid in grids:
        grid_row = int(grid / 3)
        grid_col = int(grid % 3)

        for value in values:
            problem += (plp.lpSum([grid_vars[grid_row * 3 + row][grid_col * 3 + col][value] * value for col in range(0, 3) for row in range(0, 3)]) == value, f"constraint_uniq_grid_{grid}_{value}")

    """
    Starting Constraint:

    Here we feed in the values from the input sudoku matrix. This constraint says that these specific cells have to have the values
    from the input sudoku matrix. So if the first cell from the input sudoku matrix is 3, it must always be 3. It will only solve
    the LpVariables that map to Cells where the values have not been set by this Constraint, i.e. all of the cells with a 0 value.
    """
    for row in rows:
        for col in cols:
            if input_sudoku[row][col] != 0:
                problem += (plp.lpSum([grid_vars[row][col][value] * value for value in values]) == input_sudoku[row][col], f"constraint_prefilled_{row}_{col}")

    """
    Very nice little paramater to supress the CBC output of PuLP
    """
    problem.solve(plp.PULP_CBC_CMD(msg=False))

    print(f'Solution Status = {plp.LpStatus[problem.status]}')

    """
    The LpVariable object contains the solutions to our problem. However, since it is a Binary based Dictionary for each potential
    value for a cell, a more "user-friendly" representation of the matrix needs to be extracted.
    """
    solved_sudoku = [[0 for col in cols] for row in rows]
    for row in rows:
        for col in cols:
            for value in values:
                if plp.value(grid_vars[row][col][value]):
                    solved_sudoku[row][col] = value
    return solved_sudoku


if __name__ == '__main__':
    solve(path='in/hard_sudoku.csv')

