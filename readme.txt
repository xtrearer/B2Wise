==================
   GENERAL INFO
==================

    There are 2 python scripts, suffixed with "bt" for Backtracking and "lp" for Linear Programming.

    Both Scripts can be executed from your IDE.

    However, "sudoku_lp.py" needs an external library to be installed, called Pulp. I've not setup a venv for this as
    I'm a little stretched for time.

    The main function, <solve> takes a string variable called "path". "path" is used to point to one of the two CSV files
    on the ./in/ folder. There is a Normal difficulty sudoku puzzle, as well as one that I specifically found to point out
    the weakness of the Backtracking method.

    The solved sudoku puzzles are written to the ./out/ folder.