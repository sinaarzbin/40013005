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

import statistics
from pacman import GameState
from util import manhattanDistance
import util
from game import Agent

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class MinimaxAgent(MultiAgentSearchAgent):

    def __init__(self, depth = '1'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = betterEvaluationFunction
        self.depth = int(depth)
        self.BEST_ACTION = None


    def minimax(self, depth, state, player):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        if player == 0:
            v = float('-inf')
            legal_actions = state.getLegalActions(0)

            for action in legal_actions:
                next_state = state.generateSuccessor(0, action)
                new_v = self.minimax(depth, next_state, player + 1)

                if depth == self.depth and new_v > v:
                    self.BEST_ACTION = action
                v = max(v, new_v)
            return v
        else:
            v = float('inf')
            next_player = (player + 1) % state.getNumAgents()
            if player + 1 == state.getNumAgents():
                depth -= 1
            for action in state.getLegalActions(player):
                v = min(v, self.minimax(depth, state.generateSuccessor(player, action), next_player))
            return v

    def getAction(self, gameState):
        self.minimax(self.depth, gameState, 0)
        return self.BEST_ACTION




class ExpectimaxAgent(MultiAgentSearchAgent):
    def __init__(self, depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = betterEvaluationFunction
        self.depth = int(depth)
        self.BEST_ACTION = None

    def minimax(self, depth, state, player):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        if player == 0:
            v = float('-inf')
            legal_actions = state.getLegalActions(0)

            for action in legal_actions:
                next_state = state.generateSuccessor(0, action)
                new_v = self.minimax(depth, next_state, player + 1)

                if depth == self.depth and new_v > v:
                    self.BEST_ACTION = action
                v = max(v, new_v)
            return v
        else:
            score_list = []
            v = float('inf')
            next_player = (player + 1) % state.getNumAgents()
            if player + 1 == state.getNumAgents():
                depth -= 1
            for action in state.getLegalActions(player):
                list.append(score_list, self.minimax(depth, state.generateSuccessor(player, action), next_player))
            v = statistics.mean(score_list)

            return v

    def getAction(self, gameState):
        self.minimax(self.depth, gameState, 0)
        return self.BEST_ACTION


# bfs nearest food
def nearest_food_distance(state):
    state.getFood()
    walls = state.getWalls()
    row, col = 0, 0
    for i in walls:
        for j in walls[0]:
            col += 1
        row += 1

    def is_in_bounds(i, j):
        if 0 < i < row and 0 < j < col:
            return True
        else:
            return False

    pac_position = state.getPacmanPosition()
    visited = set()
    queue = util.Queue()
    queue.push([pac_position, 0])
    while not queue.isEmpty():
        temp_position = queue.pop()
        x, y = temp_position[0]

        if state.hasFood(x, y):
            return temp_position[1]

        if temp_position[0] in visited:
            continue

        visited.add(temp_position[0])

        x, y = temp_position[0]
        if not walls[x - 1][y] and is_in_bounds(x - 1, y):
            queue.push([(x - 1, y), temp_position[1] + 1])
        if not walls[x + 1][y] and is_in_bounds(x + 1, y):
            queue.push([(x + 1, y), temp_position[1] + 1])
        if not walls[x][y - 1] and is_in_bounds(x, y - 1):
            queue.push([(x, y - 1), temp_position[1] + 1])
        if not walls[x][y + 1] and is_in_bounds(x, y + 1):
            queue.push([(x, y + 1), temp_position[1] + 1])

    return float('inf')


def betterEvaluationFunction(currentGameState: GameState):
    score = 0

    pac_pos = currentGameState.getPacmanPosition()
    food_remain = currentGameState.getNumFood()
    ghost_states = currentGameState.getGhostStates()
    ghost_distance = 0


    if currentGameState.isWin():
        return currentGameState.getScore() + 10000
    if currentGameState.isLose():
        return -10000

    score += currentGameState.getScore() / 2

    score -= 100 * food_remain

    score += 10/nearest_food_distance(currentGameState)

    for ghost in ghost_states:
        d = manhattanDistance(ghost.getPosition(), pac_pos)
        ghost_distance += d
        if d < 3:
            score -= d * 10

    return score