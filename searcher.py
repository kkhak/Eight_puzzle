#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Kyle Hakimi
# email: kylehaki@bu.edu
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """ constructs new searcher object"""
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
        
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s

    def should_add(self, state):
        """ takes a State object called state and returns True 
        if the called Searcher should add state to its list of 
        untested states, and False otherwise."""
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        if state.creates_cycle():
            return False
        return True
    
    def add_state(self, new_state):
       """ takes a single State object called new_state and 
       adds it to the Searcher's list of untested states """
       self.states.append(new_state)
    
    def add_states(self, new_states):
        """ takes a list of State objects called new_states, and processes the elements of new_states one at a time """
        for s in new_states:
            if self.should_add(s):
                self.add_state(s)
    
    def next_state(self):
        """ chooses the next state to be tested from the list of 
        untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s 
    
    def find_solution(self, init_state):
        """performs a full random state-space search, 
        stopping when the goal state is found or when the 
        Searcher runs out of untested states."""
        self.add_state(init_state)
        while self.states:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None
        
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###
def h1(state):
    """ a heuristic function that estimates the cost to reach the goal state
        by counting the number of misplaced tiles
    """
    return state.board.num_misplaced()

def h2(state):
    """heuristic function that calculates the sum of the row 
    and column distances of each tile from its goal position."""
    board = state.board
    distance = 0
    for r in range(3):
        for c in range(3):
            tile = board.tiles[r][c]
            if tile != 0:
                goal_r = (tile - 1) // 3
                goal_c = (tile - 1) % 3
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ###

    def __init__(self, depth_limit, heuristic):
        """ constructor for a GreedySearcher object
            inputs:
             * depth_limit - the depth limit of the searcher
             * heuristic - a reference to the function that should be used 
             when computing the priority of a state
        """
        super().__init__(depth_limit)  
        self.heuristic = heuristic

    def priority(self, state):
        """ takes a State object called state, and that computes and returns the 
        priority of that state."""
        return -1 * self.heuristic(state)

    def add_state(self, state):
        """  overrides (i.e., replaces) the add_state method that is inherited from Searcher.
        Rather than simply adding the specified state
        to the list of untested states, the method should
        add a sublist that is a [priority, state] pair,
        where priority is the priority of state, as 
        determined by calling the priority method. """
        priority = self.priority(state)
        self.states.append([priority, state])

    def next_state(self):
        """ choose one of the states with the highest priority """
        if not self.states:
            return None
        
        best_index = 0
        for i in range(1, len(self.states)):
            if self.states[i][0] > self.states[best_index][0]:
                best_index = i
        
        best = self.states[best_index]
        new_states = []
        for i in range(len(self.states)):
            if i != best_index:
                new_states.append(self.states[i])
        self.states = new_states
        
        return best[1]

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s


### Add your AStarSeacher class definition below. ###

class BFSearcher(Searcher):
    """ A class for searcher objects that perform 
    breadth-first search (BFS)."""
    
    def next_state(self):
        """ overrides (i.e., replaces) the next_state method 
        that is inherited from Searcher. Rather than choosing 
        at random from the list of untested states, this 
        version of next_state should follow FIFO (first-in 
        first-out) ordering – choosing the state that has been 
        in the list the longest. 
        """
        if self.states:
            s = self.states[0]  
            self.states.remove(s)
            return s
        else:
            return None 
    
class DFSearcher(Searcher):
    """ A class for searcher objects that perform depth-first
    search (DFS)."""
    
    def next_state(self):
        """ Chooses the next state to be tested from the list of untested
        states, removing it from the list and returning it.
        Overrides the next_state method of the Searcher class.
        """
        if self.states:
            s = self.states[-1]  
            self.states.remove(s)
            return s
        else:
            return None
        
class AStarSearcher(GreedySearcher):
    """ A class for searcher objects that perform A* search. """

    def __init__(self, depth_limit, heuristic):
        """ constructor for an AStarSearcher object
            inputs:
             * depth_limit - the depth limit of the searcher
             * heuristic - a reference to the function that should be used 
             when computing the priority of a state
        """
        super().__init__(depth_limit, heuristic)

    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function"""
        return -1 * (self.heuristic(state) + state.num_moves)

    def __repr__(self):
        """ return a string representation of the AStarSearcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s
