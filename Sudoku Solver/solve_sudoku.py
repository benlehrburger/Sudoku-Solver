from display import display_sudoku_solution
from sat import SAT

puzzle_name = 'rows_and_cols'

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:

    sol_filename = puzzle_name + ".sol"

    sat = SAT(puzzle_name + '.cnf')

    result = sat.walksat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)

