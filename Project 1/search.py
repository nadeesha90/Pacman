# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    DFSstack = util.Stack();
    DFSstack.push(problem.getStartState());
    visited = [];
    visited.append(problem.getStartState());
    directions = {};		
    prevstate = {};
    dirs = [];
    while (not(DFSstack.isEmpty())):
		state = DFSstack.pop();
		print "State: ", state;
		if (not(problem.isGoalState(state))):
			successors = problem.getSuccessors(state);
			for s in successors:
				if (not(s[0] in visited)):
					print "Successor: ", s[0];
					DFSstack.push(s[0]);
					directions[s[0]] = s[1];
					prevstate[s[0]] = state;
					visited.append(s[0]);
		else:
			print "Goal Found";
			gstate = state;
			while(gstate != problem.getStartState()):
				print gstate;
				dirs.append(directions[gstate]);
				gstate = prevstate[gstate];
			break;
    
    print "Start:", problem.getStartState();
    print "Is the start a goal?", problem.isGoalState(problem.getStartState());
    print "Start's successors:", problem.getSuccessors(problem.getStartState());	
    print "Goal State:", problem.goal;    
    #util.raiseNotDefined()
    return dirs[::-1];

def breadthFirstSearch(problem):
	"""
	Search the shallowest nodes in the search tree first.
	[2nd Edition: p 73, 3rd Edition: p 82]
	"""
	"*** YOUR CODE HERE ***"
	f = open('states.txt','w');
	
	BFSQueue = util.Queue();
	BFSQueue.push(problem.getStartState());
	visited = [];
	visited.append(problem.getStartState());
	
	directions = {};
	prevstate = {};
	dirs = [];
	
	while (not(BFSQueue.isEmpty())):
		state = BFSQueue.pop();
		#print "state: ",state;
		f.write(str(state) + '\n');
		if (not(problem.isGoalState(state))):
			successors = problem.getSuccessors(state);
			for s in successors:
				if (not(s[0] in visited)):
					#print "Successor: ", s[0];
					BFSQueue.push(s[0]);
					if (s[0] in directions):
						print "over-writing directions";
					
					directions[s[0]] = s[1];
					prevstate[s[0]] = state;
					visited.append(s[0]);
		else:
			print "Goal Found";
			gstate = state;
			while(gstate != problem.getStartState()):
				print gstate;
				dirs.append(directions[gstate]);
				gstate = prevstate[gstate];
			print gstate;
			break;
	
	#print problem.corners;
	f.close();
	
	return dirs[::-1]; 

def uniformCostSearch(problem):
	"Search the node of least total cost first. "
	"*** YOUR CODE HERE ***"
	cost_dict = {};
	directions = {};
	prevstate = {};
	visited = [];
	
	dirs = [];
	
	pq = util.PriorityQueue();
	state = problem.getStartState();
	cost_dict[state] = 0;
	visited.append(state);
	pq.push(state,0);
	while (not(pq.isEmpty())):
		state = pq.pop();
		if (not(problem.isGoalState(state))):
			succ = problem.getSuccessors(state);
			for s in succ:
				if (not(s[0] in visited)):
					cost = cost_dict[state] + s[2];
					visited.append(s[0]);
					directions[s[0]] = s[1];
					prevstate[s[0]] = state;
					pq.push(s[0],cost);
					cost_dict[s[0]] = cost;
		else:
			gstate = state;
			while (gstate != problem.getStartState()):
				dirs.append(directions[gstate]);
				gstate = prevstate[gstate];
			break;
			
#    util.raiseNotDefined()
	return dirs[::-1];
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"Search the node that has the lowest combined cost and heuristic first."
	"*** YOUR CODE HERE ***"
	cost_dict = {};	#g(n)	backward cost
	directions = {};
	prevstate = {};
	visited = [];
	
	dirs = [];
	
	pq = util.PriorityQueue();
	state = problem.getStartState();
	cost_dict[state] = 0;
	visited.append(state);
	pq.push(state,0);
	print 'here';
	while (not(pq.isEmpty())):
		state = pq.pop();
		#print state;
		if (not(problem.isGoalState(state))):
			succ = problem.getSuccessors(state);
			for s in succ:
				if (not(s[0] in visited)):
					g_cost = cost_dict[state] + s[2];		#backward cost
					h_cost = heuristic(state,problem);		#heuristic
					visited.append(s[0]);
					directions[s[0]] = s[1];
					prevstate[s[0]] = state;
					
					pq.push(s[0],g_cost + h_cost);
#					print h_cost;
					cost_dict[s[0]] = g_cost;
		else:
			gstate = state;
			while (gstate != problem.getStartState()):
				dirs.append(directions[gstate]);
				gstate = prevstate[gstate];
			break;
	return dirs[::-1];
#    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
