# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    startState = problem.getStartState()
    history = dict()
    history[startState] = [None, None]
    unexplored = util.Stack()
    unexplored.push(startState)
    explored = set()

    while(not unexplored.isEmpty()):
        candidate = unexplored.pop()
        if(candidate in explored):
            continue
        explored.add(candidate)

        if(problem.isGoalState(candidate)):
            break

        for newState in problem.getSuccessors(candidate):
            if newState[0] in explored:
                continue
            else:
                history[newState[0]] = [candidate, newState[1]]
                unexplored.push(newState[0])

    if(not problem.isGoalState(candidate)):
        return None

    ans = []
    backtrace = candidate
    while(backtrace!=startState):
        ans = [history[backtrace][1]]+ans
        backtrace = history[backtrace][0]

    return ans

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    history = dict()
    history[startState] = [None, None]
    unexplored = util.Queue()
    unexplored.push(startState)

    while(not unexplored.isEmpty()):
        candidate = unexplored.pop()
        if(problem.isGoalState(candidate)):
            break
        for newState in problem.getSuccessors(candidate):
            if newState[0] in history:
                continue
            else:
                history[newState[0]] = [candidate, newState[1]]
                unexplored.push(newState[0])

    if(not problem.isGoalState(candidate)):
        return None

    ans = []
    backtrace = candidate
    while(backtrace!=startState):
        ans = [history[backtrace][1]]+ans
        backtrace = history[backtrace][0]

    return ans


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    startState = problem.getStartState()
    history = dict()
    history[startState] = [None, None, 0]
    unexplored = util.PriorityQueue()
    unexplored.push(startState, 0)
    explored = set()

    while(not unexplored.isEmpty()):
        candidate = unexplored.pop()
        if(candidate in explored):
            continue
        explored.add(candidate)

        if(problem.isGoalState(candidate)):
            break
        for newState in problem.getSuccessors(candidate):
            if newState[0] in explored:
                continue
            else:
                newCost = history[candidate][2]+newState[2]
                if(newState[0] not in history or newCost<history[newState[0]][2]):
                    history[newState[0]] = [candidate, newState[1], newCost]
                    unexplored.push(newState[0], newCost)

    if(not problem.isGoalState(candidate)):
        return None

    ans = []
    backtrace = candidate
    while(backtrace!=startState):
        ans = [history[backtrace][1]]+ans
        backtrace = history[backtrace][0]

    return ans


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    startState = problem.getStartState()

    history = dict()        # history: state->[prev state, action from prev state, cost]
    history[startState] = [None, None, 0]

    unexplored = util.PriorityQueue()
    unexplored.push(startState, history[startState][2]+heuristic(startState, problem))
    explored = set()

    while(not unexplored.isEmpty()):
        current = unexplored.pop()
        if(problem.isGoalState(current)):
            break
        if(current in explored):
            continue
        for newState in problem.getSuccessors(current):
            newCost = history[current][2] + newState[2]
            if(newState[0] not in history or newCost < history[newState[0]][2]):
                history[newState[0]] = [current, newState[1], newCost]
                unexplored.push(newState[0], newCost+heuristic(newState[0], problem))

    if(not problem.isGoalState(current)):
        return None

    ans = []
    backtrace = current
    while (backtrace != startState):
        ans = [history[backtrace][1]] + ans
        backtrace = history[backtrace][0]

    return ans


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
