import csv


""" Global Variables """
rows = range(0, 9)
cols = range(0, 9)
grids = range(0, 9)
values = range(1, 10)
recursion = 0
""" ---------------- """


def solve(path):
    input_sudoku = read_sudoku(path)
    print(f'\n### Input Sudoku ###\n')
    print_matrix(input_sudoku)
    print('\n####################\n')

    solved_sudoku = backtrack(input_sudoku)
    print(f'\n### Solved Sudoku ###\n')
    print_matrix(solved_sudoku)
    print('\n####################\n')

    output_path = f"out/{path.split('/')[-1].split('.csv')[0]}_solved_bt.csv"
    write_sudoku(path=output_path, solved_sudoku=solved_sudoku)
    print(f'Solved sudoku results have been written to "{output_path}"')


def read_sudoku(path):
    with open(path, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        return [[int(value) for value in row] for row in csv_reader]


def print_matrix(solved_sudoku):
    for row in rows:
        print(' '.join([f'{value}' for value in solved_sudoku[row]]))


def write_sudoku(path, solved_sudoku):
    with open(path, mode='w', newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
        csv_writer.writerows(solved_sudoku)


def backtrack(input_sudoku):
    for row in rows:
        for col in cols:
            if input_sudoku[row][col] == 0:
                for guess in values:
                    if guess_is_valid(input_sudoku, row, col, guess):
                        input_sudoku[row][col] = guess
                        if backtrack(input_sudoku) is not None:
                            return input_sudoku
                        input_sudoku[row][col] = 0
                return None
    return input_sudoku


def guess_is_valid(input_sudoku, row, col, guess):
    """ Check Rows """
    if guess in input_sudoku[row]:
        return False

    """ Check Columns """
    if guess in [input_sudoku[r][col] for r in rows]:
        return False

    """ Check Grid """
    grid_row_start = (row // 3) * 3
    grid_col_start = (col // 3) * 3
    for grid_row in range(0,3):
        for grid_col in range(0,3):
            if input_sudoku[grid_row_start + grid_row][grid_col_start + grid_col] == guess:
                return False
    return True


if __name__ == '__main__':
    solve(path='in/hard_sudoku.csv')

