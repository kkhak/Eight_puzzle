#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: 
# email:
#

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
       
        #rest of init method
        for r in range(3):
           for c in range(3):
               tile_value = int(digitstr[3*r + c])
               self.tiles[r][c] = tile_value
               if tile_value == 0:
                   self.blank_r = r
                   self.blank_c = c

    ### Add your other method definitions below. ###
    def __repr__(self):
        """ Returns a string representation for a Board object."""
        s = ''
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == 0:
                    s += '_'
                else:
                    s += str(self.tiles[r][c])
                s += ' ' 
            s += '\n'  
        return s

    #method 3
    def move_blank(self, direction):
        """takes as input a string direction that specifies the 
        direction in which the blank should move, and that 
        attempts to modify the contents of the called Board 
        object accordingly."""
        moves = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        
        if direction not in moves:
            print(f"unknown direction: {direction}")
            return False
        
        dr, dc = moves[direction]
        new_r = self.blank_r + dr
        new_c = self.blank_c + dc
        
        # Checking movement
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            self.tiles[self.blank_r][self.blank_c] = self.tiles[new_r][new_c]
            self.tiles[new_r][new_c] = 0
            self.blank_r = new_r
            self.blank_c = new_c
            return True
        else:
            return False
        
    #method 4
    def digit_string(self):
        """creates and returns a string of digits that 
        corresponds to the current contents of the called 
        Board object’s tiles attribute."""
        s =""
        for r in range(3):
            for c in range(3):
                s += str(self.tiles[r][c])
        return s
   
    #method 5
    def copy(self):
        """returns a newly-constructed Board object that is a 
        deep copy of the called object"""
        return Board(self.digit_string())
    
    #method 6
    def num_misplaced(self):
        """counts and returns the number of tiles in the 
        called Board object that are not where they should 
        be in the goal state."""
        goal = '012345678'  
        count = 0
        for r in range(3):
            for c in range(3):
                current_tile = self.tiles[r][c]
                if current_tile != 0 and current_tile != int(goal[3 * r + c]):
                    count += 1
        return count
    #method 7
    def  __eq__(self, other):
        """overloads the == operator – creating a version of 
        the operator that works for Board objects"""
        return self.tiles == other
    