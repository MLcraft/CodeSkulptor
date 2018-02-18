"""
2048
Use arrow keys (Up, Down, Left, Right) to play.
Have fun!
Made by MLcraft
"""

import poc_2048_gui        
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code
    result = []
    is_merged = []
    copy_line = []
    pop_list = []
    for idx in line:
        # Makes a copy of the line so the original line is not modified
        copy_line.append(idx)
        # Adds the correct amount of zeros to the merged list
        result.append(0)
        is_merged.append(False)
    #print result, "\n", copy_line, "\n", is_merged
    while copy_line.count(0) > 0:
        copy_line.remove(0)
    for idx in range(len(copy_line)):
        result[idx] = copy_line[idx]
    for idx in range(len(result) - 1):
        if not is_merged[idx]:
            if result[idx] == result[idx + 1]:
                result[idx] *= 2
                is_merged[idx] = True
                is_merged[idx + 1] = True
                pop_list.append(idx + 1)
                
    for idx in pop_list:
        result[idx] = 0
    while result.count(0) > 0:
        result.remove(0)
    while len(result) < len(line):
        result.append(0)
    #print "RESULT", result
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height = grid_height
        self.width = grid_width
        self.dir_indices = {UP: [(0, j) for j in range(self.width)], \
                            DOWN: [(self.height - 1, j) for j in range(self.width)], \
                            LEFT: [(j, 0) for j in range(self.height)],\
                            RIGHT: [(j, self.width - 1) for j in range(self.height)]}
        #print self.dir_indices
        self.reset()
        #str(self)
        
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        #self.board = [[8, 16, 8, 16, 8], [16, 8, 16, 8, 16], [8, 16, 8, 16, 8], [16, 8, 16, 8, 16]]
        self.board = []
        for dummy_i in range(self.height):
            append_list = [0 for dummy_col in range(self.width)]
            self.board.append(append_list)
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        str_2048 = "Grid height: " + str(self.height) + "\nGrid width: " + str(self.width) + "\n    Row zero      Row one       Row two       Row three\n       |             |               |            |\n       v             v               v            v\n" + str(self.board)
        #print str_2048
        return str_2048
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        
        merged_l = []
        self.movehelp(direction, merged_l)
        #print "MERGED_L", str(merged_l)
        for tlen in range(len(merged_l)):
            for swid in range(len(merged_l[0])):
         #       print self.board[self.height - 1 - swid][tlen], merged_l[tlen][swid]
                square = merged_l[tlen][swid]
                if direction == RIGHT:
                    self.board[tlen][self.width - 1 - swid] = square
                elif direction == DOWN:
                    self.board[self.height - 1 - swid][tlen] = square
                elif direction == LEFT:
                    self.board[tlen][swid] = square
                else:
                    self.board[swid][tlen] = square
        
        for row in self.board:
            if 0 in row:
                self.new_tile()
                break
    
    def movehelp(self, direction, merged_l):
        """
        Poop.
        """
        directions = {1: UP, 2: DOWN, 3: LEFT, 4: RIGHT}
        tup = OFFSETS[directions[direction]]
        dimension = self.width
        if directions[direction] in (UP, DOWN):
            dimension = self.height
        for idx in self.dir_indices[direction]:
                lst = []
                for jdx in range(dimension):
                    #print "HELLO", i[0], "BYE", OFFSETS[directions[direction]]

                    lst.append(self.board[idx[0] + jdx * tup[0]][idx[1] + jdx * tup[1]])
                merged_l.append(merge(lst))
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        possible_places = []
        for idx in range(self.width):
            for jdx in range(self.height):
                if self.board[jdx][idx] == 0:
                    possible_places.append([jdx, idx])
        random_pos = random.choice(possible_places)
        if random.randint(1, 10) == 1:
            self.board[random_pos[0]][random_pos[1]] = 4
        else:
            self.board[random_pos[0]][random_pos[1]] = 2
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        self.board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.board[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
