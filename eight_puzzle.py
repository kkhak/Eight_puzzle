#
# eight_puzzle.py (Final Project)
#
# driver/test code for state-space search on Eight Puzzles
#
# name: Kyle Hakimi
# email: Kylehaki@bu.edu
#

from searcher import *
from timer import *

def create_searcher(algorithm, depth_limit = -1, heuristic = None):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
            
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(depth_limit)
    elif algorithm == 'BFS':
        searcher = BFSearcher(depth_limit)
    elif algorithm == 'DFS':
        searcher = DFSearcher(depth_limit)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(depth_limit, heuristic)
    elif algorithm == 'A*':
       searcher = AStarSearcher(depth_limit, heuristic)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, depth_limit = -1, heuristic = None):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * depth_limit - an optional parameter that can be used to
            specify a depth limit 
          * heuristic - an optional parameter that can be used to pass
            in a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')

    searcher = create_searcher(algorithm, depth_limit, heuristic)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()

def process_file(filename, algorithm, depth_limit=-1, heuristic=None):
    """Process a file of eight puzzle configurations"""
    
    total_moves = total_states = puzzles_solved = 0
    
    file = open(filename, 'r')
    for digit_string in file:
       init_state = State(Board(digit_string.strip()), None, 'init')
       searcher = create_searcher(algorithm, depth_limit, heuristic)
       if not searcher:
           print(f"Searcher not created for {algorithm}")
           file.close()
           return

       try:
           soln = searcher.find_solution(init_state)
       except KeyboardInterrupt:
           print(f'{digit_string.strip()}: search terminated, ', end='')
           soln = None

       if soln:
           print(f'{digit_string.strip()}: {soln.num_moves} moves, {searcher.num_tested} states tested')
           total_moves += soln.num_moves
           total_states += searcher.num_tested
           puzzles_solved += 1
       else:
           print('no solution')

    file.close()
    
    print(f'\nsolved {puzzles_solved} puzzles')
    if puzzles_solved:
        avg_moves = total_moves / puzzles_solved
        avg_states = total_states / puzzles_solved
        print(f'averages: {avg_moves:.1f} moves, {avg_states:.1f} states tested')
        
        
