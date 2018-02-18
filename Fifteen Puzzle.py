"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import codeskulptor
codeskulptor.set_timeout(1)

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) != 0:
            return False
        for idx in range(target_row + 1, self.get_height()):
            for jdx in range(self.get_width()):
                if self.current_position(idx, jdx) != (idx, jdx):
                    return False
                for kdx in range(target_col + 1, self.get_width()):
                    if self.current_position(idx, kdx) != (idx, kdx):
                        return False
        return True          
    
    def solve_above(self, target_row, target_col):
        """
        Helper Function.
        """
        target_tile = self.current_position(target_row, target_col)
        distar = target_row - target_tile[0]
        diszero = self.current_position(0, 0)[0] - target_tile[0]
        move_string = ""
        if distar < 2:
            move_string = "u"
        elif distar == 2:
            move_string = "u" * diszero + "lddru"
        else:
            move_string = "u" * diszero + "lddru" * (distar - 2)
        move_string += "ld"
        self.update_puzzle(move_string)
        return move_string
    
    def solve_right(self, target_row, target_col):
        """
        Helper Function.
        """
        target_tile = self.current_position(target_row, target_col)
        distarright = target_tile[1] - target_col
        distarup = target_row - target_tile[0] 
        move_string = ""
        if distarright >= 1:
            move_string += "u" * distarup + "r" * distarright
            if distarup > 0:
                    move_string += "dl"
            self.update_puzzle(move_string)

        if self.current_position(target_row, target_col) != (target_row, target_col):
            move_string += self.solve_above(target_row, target_col)
        return move_string
    
    def solve_left(self, target_row, target_col):
        """
        Helper Function.
        """
        target_tile = self.current_position(target_row, target_col)
        distarleft = target_col - target_tile[1]
        distarup = target_row - target_tile[0] 
        move_string = ""
        if not distarleft < 1:
            if distarleft == 1:

                move_string += "u" * distarup + "l" * distarleft
                if distarup > 0:
                    move_string += "dr"
                self.update_puzzle(move_string)

            else:

                move_string += "u" * distarup + "l" * distarleft + "drrul" * (distarleft - 1)+ "dr"
                self.update_puzzle(move_string)

        if self.current_position(target_row, target_col) != (target_row, target_col):	
            move_string += self.solve_above(target_row, target_col)
        return move_string
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        return self._position((target_row, target_col), self.current_position(target_row, target_col))

    def _position(self, target_pos, tile_pos):
        """
        Helper Function.
        """
        position = None
        if target_pos[1] < tile_pos[1]:
            position = self._position_right(target_pos, tile_pos)
         #   print "HI"
        elif target_pos[1] > tile_pos[1]:
            position = self._position_left(target_pos, tile_pos)
          #  print "HI"
        else:
            position = self._position_top(target_pos, tile_pos)
           # print "HI"	
        return position
        
    def _position_right(self, target_pos, tile_pos):
        """
        Helper Function.
        """
        tile_orig_pos = self.get_pos(tile_pos)
        tile_other_pos = self.get_pos(target_pos)
        distarright = tile_pos[1] - target_pos[1]
        distarup = target_pos[0] - tile_pos[0] 
        move_string = ""

        if not distarright < 1:
            
            move_string += "u" * distarup + "r" * distarright + "dllur" * (distarright - 1)
            if distarup > 0:
                    move_string += "dl"
        self.update_puzzle(move_string)

        new_pos = self.current_position(tile_orig_pos[0], tile_orig_pos[1])
        string = "d" * (target_pos[0] - self.current_position(tile_other_pos[0], tile_other_pos[1])[0])
        move_string += string
        self.update_puzzle(string)
        
        if new_pos != target_pos:	
            move_string += self._position_top(target_pos, new_pos)
        return move_string
        
    def _position_left(self, target_pos, tile_pos):
        """
        Helper Function.
        """
        tile_orig_pos = self.get_pos(tile_pos)
        tile_other_pos = self.get_pos(target_pos)
        distarleft = target_pos[1] - tile_pos[1]
        distarup = target_pos[0] - tile_pos[0] 
        move_string = ""
        if not distarleft < 1:
            if distarleft == 1:
                move_string += "u" * distarup + "l" * distarleft
                if distarup > 0:
                    move_string += "dr"
            else:
                print "DDDDD"
                print target_pos,tile_orig_pos[0]   
                if (distarup >0):
                    move_string += "u" * distarup + "l" * distarleft + "drrul" * (distarleft - 1)+ "dr"
                else:
                    move_string +=  "u" * distarup + "l" * distarleft + "urrdl" * (distarleft - 1)
                

        self.update_puzzle(move_string)
        new_pos = self.current_position(tile_orig_pos[0], tile_orig_pos[1])
        string = "d" * (target_pos[0] - self.current_position(tile_other_pos[0], tile_other_pos[1])[0])
        move_string += string
        self.update_puzzle(string)

        if new_pos != target_pos:	
            move_string += self._position_top(target_pos, new_pos)
        return move_string
        
    def _position_top(self, target_pos, tile_pos):
        """
        Helper Function.
        """
        distar = target_pos[0] - tile_pos[0]
        diszero = target_pos[0] - tile_pos[0]
        move_string = ""
        if distar < 2:
            move_string = "u"
        elif distar == 2:
            move_string = "u" * diszero + "lddru"
        else:
            move_string = "u" * diszero + "lddru" * (distar - 1)
        move_string += "ld"
        self.update_puzzle(move_string)
        return move_string        
    
    def _position_zero(self, target_row, target_col):
        """
        Poop
        """
        find = self.current_position
        ddd = target_row - find(0, 0)[0]
        duu = find(0, 0)[0] - target_row
        drr = target_col - find(0, 0)[1]
        dll = find(0, 0)[1] - target_col
#        print du, dd, dr, dl
        move_string = ""
        
        if drr > 0:
            string = "r" * drr
            self.update_puzzle(string)
            print str(self)
            move_string += string
        if dll > 0:
            string = "l" * dll
            self.update_puzzle(string)
            print str(self)
            move_string += string
        if duu > 0:
            string = "u" * duu
            self.update_puzzle(string)
            print str(self)
            move_string += string
        if ddd > 0:
            string = "d" * ddd
            self.update_puzzle(string)
            print str(self)
            move_string += string
        return move_string
    
    def get_pos(self, tile_pos):
        """
        Helper Function.
        """
        tile_orig_pos = (0, 0)
        for idx in range(self.get_height()):
            for jdx in range(self.get_width()):
                if self.current_position(idx, jdx) == tile_pos:
                    tile_orig_pos = (idx, jdx)
                    return tile_orig_pos
    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = "ur"
        self.update_puzzle("ur")

        if self.current_position(target_row, 0) == (target_row, 0):
            string = "r" * (self.get_width() - 1 - self.current_position(0, 0)[1])
            move_string += string
            self.update_puzzle(string)
        else:
            string = "ruldrdlurdluurddlur" + "r" * (self.get_width() - self.current_position(0, 0)[1] - 1)
            move_string += self._position(self.current_position(0, 0), self.current_position(target_row, 0)) + string
            self.update_puzzle(string)
           
        return move_string
    #############################################################
    # Phase two methods


    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0, target_col) != 0:
            return False
        if self.current_position(1, target_col) != (1, target_col):
            return False
        for idx in range(2, self.get_height()):
            for jdx in range(self.get_width()):
                if self.current_position(idx, jdx) != (idx, jdx):
                    return False
                for kdx in range(target_col + 1, self.get_width()):
                        if self.current_position(idx, kdx) != (idx, kdx):
                            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(1, target_col) != 0:
            return False
        for idx in range(2, self.get_height()):
            for jdx in range(self.get_width()):
                if self.current_position(idx, jdx) != (idx, jdx):
                    return False
                for kdx in range(target_col + 1, self.get_width()):
                        if self.current_position(idx, kdx) != (idx, kdx):
                            return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = "ld"
        self.update_puzzle("ld")
        #print self.current_position(0, target_col)
        distarup = (self.current_position(0, 0)[0] - self.current_position(0, target_col)[0])
        distarright = (self.current_position(0, target_col)[1] - self.current_position(0, 0)[1])
        distarleft = (self.current_position(0, 0)[1] - self.current_position(0, target_col)[1])
        #print distarup, distarright, distarleft
        if self.current_position(0, target_col) == (0, target_col):
            return move_string
        else:
            string = ""
            if distarleft > 0:
                #left
                string = "l" * distarleft + "u" * distarup + "rdl" * distarup + "urrdl" * (distarleft - 1)
            elif distarleft < 0:
                #right
                string = "r" * distarright + "u" * distarup + "ldr" * distarup + "ulldr" * (distarright - 1)            	
            else:
                #up
                string = "uld"
            self.update_puzzle(string)
            move_string += string
            #print str(self)
            self.update_puzzle("urdlurrdluldrruld")
            move_string += "urdlurrdluldrruld"
            #print str(self)
            return move_string
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        distarup = (1 - self.current_position(1, target_col)[0])
        distarleft = (target_col - self.current_position(1, target_col)[1])
        distarright = (self.current_position(1, target_col)[1] - target_col)
        if distarleft > 0:
            # left
            move_string = "l" * distarleft + "u" * distarup + "rdl" * distarup + "urrdl" * (target_col - self.current_position(1, target_col)[1] - 1) + "ur"
            #print move_string
            self.update_puzzle(move_string)
            return move_string
        elif distarleft < 0:
            # right
            move_string = "r" * distarright + "u" * distarup + "ldr" * distarup + "ulldr" * (self.current_position(1, target_col)[1] - target_col - 1) + "ul"
            #print move_string
            self.update_puzzle(move_string)
            return move_string
        else:
            # up
            move_string = "u"
            self.update_puzzle(move_string)
            return move_string
            
    ###########################################################
    # Phase 3 methods
    def _is_done_2x2(self):
        """
        Helper function.
        """
        for item in range(2):
            for jtem in range(2):
                if not (self.current_position(item, jtem) == (item, jtem)):
                    return False
        return True
    
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        move_string = "lu"
        self.update_puzzle("lu")
        while not (self._is_done_2x2()):
            move_string += "rdlu"
            self.update_puzzle("rdlu")
        return move_string

    def _in_2x2(self, row, col):
        """
        Poop.
        """
        return (row<2 and col<2) 
    def _part1(self):
        """
        P1
        """
        height = self.get_height()
        width = self.get_width()
        target_row = self.current_position(0, 0)[0]
        target_col = self.current_position(0, 0)[1]        
        move_string = ""
        if self.current_position(0, 0) == (0, 0) and self.current_position(0, 1) == (0, 1):
            return move_string
        print "DOOO"
        for item in range(height - 1, -1, -1):
            for jtem in range(width - 1, -1, -1):
                print item, jtem
                if self.current_position(item, jtem) != (item, jtem):
                    target_row = item
                    target_col = jtem
                    break
            break
        #print target_row, target_col
        move_string += self._position_zero(target_row, target_col)

        print str(self) 
        return move_string

    def _part2(self):
        """
        P1
        """        
        move_string = ""
        height = self.get_height()
        width = self.get_width()        
        for row in range(height -1, -1, -1):
            for col in range(width -1, -1, -1): 
                print str(self) 
                if (self._in_2x2(row, col)):
                    break
                elif (row > 1 and self.lower_row_invariant(row, col)):
                        if(col!=0):
                            move_string += self.solve_interior_tile(row, col)
                        else:    
                            move_string += self.solve_col0_tile(row)
                elif (row == 1 and self.row1_invariant(col)):
                    #print "FOO ", row, col, self.row1_invariant(col)
                    if(col!=0):                    
                        move_string +=self.solve_row1_tile(col)
                        if (self.row0_invariant(col)):
                            move_string +=self.solve_row0_tile(col)
                    else:
                        move_string +=self.solve_col0_tile(row)
                        if (self.row0_invariant(col)):
                            move_string +=self.solve_row0_tile(col)                            
        return move_string
        
        
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        
        height = self.get_height()
        width = self.get_width()
        print height, width
        move_string = ""
        target_row = self.current_position(0, 0)[0]
        target_col = self.current_position(0, 0)[1]
        

        if self.current_position(0, 0) == (0, 0) and self.current_position(0, 1) == (0, 1):
            return move_string
        print "DOOO"
        for item in range(height - 1, -1, -1):
            for jtem in range(width - 1, -1, -1):
                print item, jtem
                if self.current_position(item, jtem) != (item, jtem):
                    target_row = item
                    target_col = jtem
                    break
            break
        #print target_row, target_col
        move_string += self._position_zero(target_row, target_col)

        print str(self) 

        move_string += self._part2()         
        move_string += self.solve_2x2()
        
        return move_string     

# Start interactive simulation

#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[5, 4, 1, 3], [8, 0, 2, 7], [10, 13, 6, 11], [9, 12, 14, 15]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 2, [[1, 2], [0, 4], [3, 5]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 3, [[3, 4, 1], [0, 2, 5]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2, [[0, 3], [1, 2]]))

#obj = Puzzle(5, 4, [[5, 4, 2, 3], [1, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#obj.solve_puzzle() 

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_puzzle()

#obj = Puzzle(3, 3, [[1, 3, 0], [2, 4, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_row0_tile(2)

#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [6, 7, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_col0_tile(3)
#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#poc_fifteen_gui.FifteenGUI(obj)    

#obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#poc_fifteen_gui.FifteenGUI(obj)    

#obj = Puzzle(3, 3, [[4, 2, 1], [6, 5, 3], [0, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_col0_tile(2)

#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(1, 1)

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(2, 2)

#obj = Puzzle(3, 3, [[7, 3, 2], [1, 4, 6], [5, 0, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(2, 1)

#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(2, 1)

#obj = Puzzle(4, 4, [[11, 1, 13, 12], [10, 14, 9, 8], [7, 6, 5, 4], [3, 2, 0, 15]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_interior_tile(3, 2)

#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_row1_tile(2)
#assert obj.row0_invariant(2), "INCORRECT!!!!"

#obj = Puzzle(4, 5, [[7, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_row1_tile(2)
#print "llurdlur"

#obj = Puzzle(3, 3, [[1, 4, 0], [2, 3, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_row0_tile(2)
#assert obj.row1_invariant(1), "INCORRECT!!"

#obj = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_row0_tile(4)

#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_2x2()

#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_puzzle() 

#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.solve_puzzle()
