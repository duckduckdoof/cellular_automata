#-----------------------------[ automata_utils.py ]--------------------------------
#
# This contains the utility classes for the different kinds of cellular automata.
#
#----------------------------------------------------------------------------------



#----------------------------------[ IMPORTS ]-------------------------------------

import numpy as np
from typing import List

#----------------------------------[ CLASSES ]-------------------------------------


# Cellular automata: 1-dimensional
class Automata1D:
    
    # Constructor for class
    # For initial conditions of the automata, you can set either:
    # 1. random cells
    # 2. zeroed cells
    # 3. a provided array of your choice, so long as the widths match
    # (default): zeroed cells, with a single centered '1'
    def __init__( self, width: int, init_random=False, init_zeros=False,
            init_custom=None ):
        self.width = width

        # Set the initial conditions for the first row of cells
        if init_random:
            self.cells = np.random.randint( 2, size=self.width )
        elif init_zeros:
            self.cells = np.zeros(self.width)
        elif init_custom is not None and init_custom.size == width:
            self.cells = init_custom
        else:
            self.cells = np.zeros(self.width)
            self.cells[self.width//2] = 1

        # Ensure that the type of numbers in the cell array are floats
        self.cells = self.cells.astype(float)

    # Applies a single iteration of the rule function to the cells
    # If replace_current is left true, the resulting cells replaces the current
    def apply_rule_func( self, rule_func, replace_current=True ):

        # Create new row of cells
        new_cells = np.zeros(self.width)

        # Go through each cell of the 1-d array of cells
        for idx, _ in enumerate(new_cells):

            # Apply the rule function for each cell, depending upon its neighbors
            new_cells[idx] = rule_func( idx, self.cells )

        if replace_current:
            self.cells = new_cells

        # Return the new computed cell block
        return new_cells

    # Applies a single iteration of a rule given 8-bit code X
    # If replace_current is left true, the resulting cells replaces the current
    def apply_rule_X( self, rule_num: int, replace_current=True ):

        # Create new row of cells
        new_cells = np.zeros(self.width)

        # Go through each cell of the 1-d array of cells
        for idx, _ in enumerate(new_cells):

            # Apply the rule function for each cell, depending upon its neighbors
            new_cells[idx] = self._a1drX( idx, rule_num )

        if replace_current:
            self.cells = new_cells

        # Return the new computed cell block
        return new_cells

    # [1-D Automata]: rule X, in which X is an 8-bit number
    # ASSUMPTION: on the edges of the space, we can always fill with 0s
    def _a1drX( self, idx: int, rule_num: int ):
        # Turn into array with padded zeroes on ends; grab the 3 cells above the current
        cells_list = list(self.cells.astype(int))
        cells_list.insert(0, 0)
        cells_list.append(0)
        focus_str = str(cells_list[idx]) + str(cells_list[idx+1]) + str(cells_list[idx+2])

        # Now apply the 8 rules (I know it's an elif-tree... sue me!)
        rule_str = '{0:08b}'.format(rule_num)
        if focus_str == "000":
            return rule_str[7]
        elif focus_str == "001":
            return rule_str[6]
        elif focus_str == "010":
            return rule_str[5]
        elif focus_str == "011":
            return rule_str[4]
        elif focus_str == "100":
            return rule_str[3]
        elif focus_str == "101":
            return rule_str[2]
        elif focus_str == "110":
            return rule_str[1]
        else:
            return rule_str[0]

    # String representation for class
    def __str__(self):
        return np.array_str(self.cells)

# Cellular automata: 2-dimensional
class Automata2D:

    # Constructor for class, calls base class's constructor first
    def __init__( self, init_grid: np.array, num_steps: int ):

        # Set up the array
        self.cells = init_grid
        self.cells = np.pad( self.cells, 1, 'constant', constant_values=0 )
        self.width = init_grid.shape[1]
        self.height = init_grid.shape[0]
        self.num_steps = num_steps
        self.current_step = 0

        # Ensure that the type of numbers in the cell array are floats
        self.cells = self.cells.astype(float)

    # Applies a single iteration of a rule, specified by a code number
    # and the number of neighbors to check , either 4 or 8
    def apply_rule_X( self, rule_num: int, num_neighbors: int ):

        # If we've hit max steps, stop
        if self.current_step >= self.num_steps:
            return self.cells

        # Sanity check!
        if not (num_neighbors == 4 or num_neighbors == 8):
            print( "Please provide a valid number of neighbors (4,8)" )
            return self.cells

        # Get the current state of the grid
        current_cells = self.cells.copy()

        # Go through each cell and update it based on the rule code
        for x in range( 1, self.height+1 ):
            for y in range( 1, self.width+1 ):

                # Update the active cells
                current_cells[x,y] = self._a2drX( self.cells,
                        rule_num, num_neighbors, x, y )

        # Return the result
        self.cells[:] = current_cells[:]
        self.current_step = self.current_step + 1
        return self.cells

    # Helper function for applying a rule once
    # We assume that num_neighbors is either 4 or 8 (since we're on a 2d grid)
    def _a2drX( self, cells: np.array, rule_num: int, 
            num_neighbors: int, x: int, y: int ): 

        # Get the (even-numbered) binary string of the code
        # We use num_neighbors + 1 because we're also checking the center square
        # We also want to reverse the string to make things easier down below
        rule_str = "{0:b}".format(rule_num).zfill( 2*(num_neighbors + 1) )[::-1]

        # Calculate the sum of neighbors, and update those neighbors to 'on'
        sum_n = cells[x,y+1] + cells[x,y-1] + \
                cells[x+1,y] + cells[x-1,y]
        if num_neighbors == 8:
            sum_n = sum_n + cells[x-1,y+1] + cells[x+1,y+1] + \
                    cells[x-1,y-1] + cells[x+1,y-1]

        # Create a 2-tuple: (sum_neighbors, cell)
        rule_t = ( int(sum_n), int(cells[x,y]) )

        # Return the result encoded in the rule string, using the 2-tuple
        return int( rule_str[2*rule_t[0] + rule_t[1]] )

    # String representation for class
    def __str__(self):
        return np.array_str(self.cells)

#----------------------------------[ FUNCTIONS ]-----------------------------------

# [1-D Automata]: cell below is opposite of cell above
def a1dr1( idx: int, cells: np.array ):
    return 1-cells[idx]

# Computes n steps for a 1-d cellular automata
def compute_n_steps_1d( automata: Automata1D, rule_func, num_steps: int ):
    for i in range( 0, num_steps ):
        yield automata.apply_rule_func(rule_func)

# Computes n steps for a 1-d cellular automata, given 8-bit rule X
def compute_n_steps_1d_ruleX( automata: Automata1D, rule_num: int, num_steps: int ):
    for i in range( 0, num_steps ):
        yield automata.apply_rule_X(rule_num)

# [2-D Automata]: cell is black if any of its eight neighbors are black
def a2dr1( cells: np.array, idx_X: int, idx_Y: int ):
    total = cells[idx_X-1, idx_Y-1] + cells[idx_X, idx_Y-1] + cells[idx_X+1, idx_Y-1] + \
            cells[idx_X-1, idx_Y] + cells[idx_X+1, idx_Y] + \
            cells[idx_X-1, idx_Y+1] + cells[idx_X, idx_Y+1] + cells[idx_X+1, idx_Y+1]
    return total >= 1

# [2-D Automata]: cell is black if any of its four neighbors are black
def a2dr2( cells: np.array, idx_X: int, idx_Y: int ):
    total = cells[idx_X, idx_Y-1] + \
            cells[idx_X-1, idx_Y] + cells[idx_X+1, idx_Y] + \
            cells[idx_X, idx_Y+1]
    return total >= 1

# [2-D Automata]: cell is black if either 1 or 4 of its neighbors are black
def a2dr3( cells: np.array, idx_X: int, idx_Y: int ):
    total = cells[idx_X, idx_Y-1] + \
            cells[idx_X-1, idx_Y] + cells[idx_X+1, idx_Y] + \
            cells[idx_X, idx_Y+1]
    return total == 1 or total == 4

#----------------------------------[ END ]-----------------------------------------
