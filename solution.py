
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], 
    ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]

unitlist = unitlist + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """

    for unit in unitlist:
        # find boxes with exact two same digits in its value
        two_digits_boxes = [box for box in unit if len(values[box]) == 2]
        number_pairs_to_eliminate = []

        for box in two_digits_boxes:
            twin = [s for s in two_digits_boxes if s != box and values[s] == values[box]]
            if len(twin) == 1:
                number_pairs_to_eliminate.append(values[box])

        # eliminate twin digits from the rest of the unit
        for number_pair in number_pairs_to_eliminate:
            boxes_to_eliminate = [box for box in unit if values[box] != number_pair]
            for box in boxes_to_eliminate:
                # remove the digits 
                for num in number_pair:
                    values[box] = values[box].replace(num, '')
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    assigned_value_boxes = [s for s in boxes if len(values[s]) == 1]

    for box in assigned_value_boxes:
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box], '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    digits = '123456789'
    for unit in unitlist:
        for d in digits:
            cells_with_d = [s for s in unit if d in values[s]]

            # assign the digit to the only cell that have the available value
            if len(cells_with_d) == 1:
                values[cells_with_d[0]] = d

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
   
    stalled = False

    while not stalled:
        solved_boxes_before = [box for box in values.keys() if len(values[box]) == 1]

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_boxes_after = [box for box in values.keys() if len(values[box]) == 1]

        failed_boxes = [s for s in values.keys() if len(values[s]) == 0]
        if len(failed_boxes) > 0:
            return False

        stalled = solved_boxes_before == solved_boxes_after

    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values = reduce_puzzle(values)

    # Check if final state
    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!

    # start with the cells that will least possibilities
    min_num,cell_with_min_possibilities = min((len(values[box]), box) for box in values.keys() if len(values[box]) > 1)

    for digit in values[cell_with_min_possibilities]:
        new_values = values.copy()
        new_values[cell_with_min_possibilities] = digit

        new_values = search(new_values)
        if new_values:
            return new_values 

    return False

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
