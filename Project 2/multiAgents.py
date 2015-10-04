# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.
	
	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""
	
	
	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.
		
		getAction chooses among the best options according to the evaluation function.
		
		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()
		print legalMoves;
		
		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		print "Hello: " + str(bestScore);
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		
		"Add more of your code here if you want to"
		
		return legalMoves[chosenIndex]
	
	def mh_dist(self, pos1, pos2):
		return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]);
		
	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.
		
		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.
		
		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.
		
		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		
	
		min_dist = -1;
		for f in newFood.asList():
			d = self.mh_dist(f,newPos);
			if (min_dist == -1):
				min_dist = d;
			elif(d < min_dist):
				min_dist = d;
		
		
		print "min dist: " + str(min_dist);
		#print newScaredTimes;
		
		sc = 10.0/float(min_dist) + successorGameState.getScore();
		
		if (action == "Stop"):
			sc = 0;
		elif (action == "West"):
			sc += 0.01;
		elif (action == "East"):
			sc += 0.02;
		elif (action == "South"):
			sc += 0.03;
		elif (action == "North"):
			sc += 0.04;
			
			
		for ng in newGhostStates:
			if(self.mh_dist(ng.getPosition(),newPos) <= 1):
				sc = 0;
		print "score: " + str(sc);
		
		return sc;
		#return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
	
	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.
	
	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""
	
	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)
		self.f = open("minimax.txt",'w');
		

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 2)
	"""
	def printstate(self,gameState,depth):
		gpos = "";
		for ng in gameState.getGhostStates():
			gpos = gpos + " " + str(ng.getPosition());
		print "score: " + str(self.evaluationFunction(gameState)) + " depth: " + str(depth) + " pacman pos: " + str(gameState.getPacmanPosition()) + " ghost pos: " + gpos + " actions: " + str(actions);

	def max_value(self, gameState, agentIndex, depth): #called by pacman only
		actions = gameState.getLegalActions(agentIndex);
		max_val = 0;
		best_action = "";
		start = 0;
		
		#self.printstate(gameState,depth);
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
		
					
		for action in actions:	#for each action:
			successor = gameState.generateSuccessor(agentIndex,action);	#generate successor states
			(act,val) = self.min_value(successor, agentIndex+1,depth-1);

			if (start == 0):	#find the maximum value and the corresponding action, store in max_val and best_action
				max_val = val;
				best_action = action;
				start = 1;
			elif (val > max_val):
				best_action = action;
				max_val = val;
			elif (val == max_val):
				if (best_action == "Stop"):
					best_action = action;
				else:
					if (random.randint(0,1) == 1):
						best_action = action;
						
		return (best_action,max_val);
		
	def min_value(self, gameState, agentIndex, depth):	#called by ghosts only
		
		actions = gameState.getLegalActions(agentIndex);
		min_val = 0;
		worst_action = "";
		start = 0;
		
#		self.printstate(gameState,depth);
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
		
		
		for action in actions:
			successor = gameState.generateSuccessor(agentIndex,action);
			if (agentIndex == (gameState.getNumAgents()-1)):		#if last ghost run pacman with max
				(act,val) = self.max_value(successor,0,depth-1);
			else:
				(act,val) = self.min_value(successor,agentIndex+1,depth-1);
			
			if (start == 0):		#compute the minimum value
				min_val = val;
				worst_action = action;
				start = 1;
			elif (val < min_val):
				min_val = val;
				worst_action = action;
			elif (val == min_val):
				if (worst_action == "Stop"):
					worst_action = action;
				else:
					if (random.randint(0,1) == 1):
						worst_action = action;
				
		return (worst_action,min_val);	
	
	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.
		
		Here are some method calls that might be useful when implementing minimax.
		
		gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1
		
		gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action
		
		gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		depthn = self.depth*gameState.getNumAgents();
		(act,val) = self.max_value(gameState,0,depthn);
		#print "final action: " + str(act);
		return act;
		"*** YOUR CODE HERE ***"
	
#		util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""
	def max_value(self, gameState,alpha,beta,agentIndex,depth):
		actions = gameState.getLegalActions(agentIndex);
		max_val = -1000000;
		best_action = "";
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
		
		for action in actions:	#for each action:
			successor = gameState.generateSuccessor(agentIndex,action);	#generate successor states
			(act,val) = self.min_value(successor,alpha,beta,agentIndex+1,depth-1);
						
			if (val > max_val):
				max_val = val;
				best_action = action;
				
			if (max_val > beta):
				return (best_action,max_val);
			
			if (val > alpha):
				alpha = val;
		
		return (best_action,max_val);
			
	def min_value(self, gameState,alpha,beta,agentIndex,depth):
		actions = gameState.getLegalActions(agentIndex);
		min_val = 1000000;
		worst_action = "";
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
	
		for action in actions:	#for each action:
			successor = gameState.generateSuccessor(agentIndex,action);	#generate successor states
			if (agentIndex == (gameState.getNumAgents()-1)):		#if last ghost run pacman with max
				(act,val) = self.max_value(successor,alpha,beta,0,depth-1);
			else:
				(act,val) = self.min_value(successor,alpha,beta,agentIndex+1,depth-1);
			
			if (val < min_val):
				min_val = val;
				worst_action = action;
		
			if (min_val < alpha):
				return (worst_action,min_val);
			
			if (val < beta):
				beta = val;
				
		return (worst_action,min_val);
		
	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		depthn = self.depth*gameState.getNumAgents();
		alpha_init = -1000000;
		beta_init = 1000000;
		(act,val) = self.max_value(gameState,alpha_init,beta_init,0,depthn);
		return act;
		#util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	Your expectimax agent (question 4)
	"""
	def max_value(self, gameState,agentIndex,depth):
		actions = gameState.getLegalActions(agentIndex);
		max_val = -1000000;
		best_action = "";
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
		
		for action in actions:	#for each action:
			successor = gameState.generateSuccessor(agentIndex,action);	#generate successor states
			(act,val) = self.min_value(successor,agentIndex+1,depth-1);
		
			if (val > max_val):
				max_val = val;
				best_action = action;
				
		return (best_action,max_val);
			
	def min_value(self, gameState,agentIndex,depth):
		actions = gameState.getLegalActions(agentIndex);
		worst_action = "";
		
		if ((depth == 0) or (len(actions) == 0)):	#if at bottom of tree or there are no remaining moves to be taken return the value of the state
			return ("act",self.evaluationFunction(gameState));
	
		val_sum = 0;
		
		for action in actions:	#for each action:
			successor = gameState.generateSuccessor(agentIndex,action);	#generate successor states
			if (agentIndex == (gameState.getNumAgents()-1)):		#if last ghost run pacman with max
				(act,val) = self.max_value(successor,0,depth-1);
			else:
				(act,val) = self.min_value(successor,agentIndex+1,depth-1);
			
			val_sum = val_sum + val;
				
		return ("act",float(val_sum)/float(len(actions)));
	
	def getAction(self, gameState):
		"""
		Returns the expectimax action using self.depth and self.evaluationFunction
		
		All ghosts should be modeled as choosing uniformly at random from their
		legal moves.
		"""
		"*** YOUR CODE HERE ***"
		depthn = self.depth*gameState.getNumAgents();
		(act,val) = self.max_value(gameState,0,depthn);
		#util.raiseNotDefined()
		return act;
		
def mhdist(p1,p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]);
	
def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).
	
	DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	initScore = currentGameState.getScore();			#initialized score
	pacmanPos = currentGameState.getPacmanPosition();	#pacman positions
	gpos = currentGameState.getGhostPositions();		#ghost positions
	fpos = [];											#list of food positions
	
	#proportional to ghost distances and inversely proportional to food distances
	
	d1 = len(currentGameState.data.food);
	d2 = len(currentGameState.data.food[0]);
	
	for x in range(d1):
		for y in range(d2):
			if (currentGameState.data.food[x][y]):
				fpos.append((x,y));
	
	fscore = 0;
	for fp in fpos:
		df = 1.0/float(float(mhdist(fp,pacmanpos)) + 0.1);
		fscore += df;
	
	gscore = 0;
	for gp in gpos:
		dg = 1.0/float(float(mhdist(gp,pacmanpos)) + 0.1);
		gscore -= dg;
	
	finalscore = initScore + fscore + gscore;
	return finalscore;
	
	#newPos = successorGameState.getPacmanPosition()
	#newFood = successorGameState.getFood()
	#newGhostStates = successorGameState.getGhostStates()
	#newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	#util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

