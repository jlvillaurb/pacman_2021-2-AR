from __future__ import print_function
# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from builtins import range
from builtins import object
from random import *
import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters

class NullGraphics(object):
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState):
        #tick = self.countActions
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        dimensionesMapa = width , height
        # Pacman position
        posicionPacman = gameState.getPacmanPosition()
        # Legal actions for Pacman in current position
        legalActions = gameState.getLegalPacmanActions()
        legal = ['None', 'None', 'None', 'None']
        if legalActions != None :
            for x in range(len(legalActions)):
                if str(legalActions[x]) == 'North': legal[0]='North'
                if str(legalActions[x]) == 'South': legal[1]='South'
                if str(legalActions[x]) == 'East': legal[2]='East'
                if str(legalActions[x]) == 'West': legal[3]='West'
            legalActions = legal
        if legalActions == None :
            legalActions = ['None', 'None', 'None', 'None']
        # Pacman direction
        direccionPacman = str(gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        numfantasmas = gameState.getNumAgents() - 1
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        fantasmasRestantes = gameState.getLivingGhosts()
        # Ghosts positions
        posicionFantasmas = gameState.getGhostPositions()
        # Ghosts directions
        direccionesFantasmas = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Manhattan distance to ghosts
        distanciasFantasmas = str(gameState.data.ghostDistances)
        distanciasFantasmas = distanciasFantasmas.replace('None', '1000')
        # Pending pac dots
        pacdotsRestantes = str(gameState.getNumFood())
        pacdotsRestantes = pacdotsRestantes.replace('None', '1000')
        # Manhattan distance to the closest pac dot
        distanciasPacdotMasCercano = gameState.getDistanceNearestFood()
        #if distanciasPacdotMasCercano == None: distanciasPacdotMasCercano=1000
        # Score
        score = gameState.getScore()

        ##Abrimos el fichero y escribimos en el
        string = posicionPacman, legalActions, direccionPacman, fantasmasRestantes, distanciasFantasmas, posicionFantasmas, pacdotsRestantes, distanciasPacdotMasCercano, score

        return str(string)


from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        ##gameState.
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

        self.NewDir = 'X'
        self.LastDir = 'Y'
        self.Last2Dir = 'Z'
        self.Last3Dir = 'T'
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances)
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood())
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood())
        # Map walls
        print("Map:")
        print( gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())
        
        
    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman

        pacmanPosition = gameState.getPacmanPosition()
        closestGhost = 0
        closestGhostDistance = 100

        for i in range(0, gameState.getNumAgents()-1):
            """
            ghostPosition = gameState.getGhostPositions()[i]
            if gameState.data.ghostDistances[i] != None: print("---> posicion fantasma: " + str(ghostPosition[0]) + " " + str(ghostPosition[1]))
            """
            if gameState.data.ghostDistances[i] != None and closestGhostDistance > gameState.data.ghostDistances[i]: 
                closestGhost = i
                closestGhostDistance = gameState.data.ghostDistances[i]

        ghostPosition = gameState.getGhostPositions()[closestGhost]
        
        north_south = ghostPosition[1] - pacmanPosition[1]
        west_east = ghostPosition[0] - pacmanPosition[0]

        if north_south == 0 and west_east > 0 and Directions.EAST in legal: 
            move = Directions.EAST
            self.NewDir = 'E'
        elif north_south == 0 and west_east < 0 and Directions.WEST in legal: 
            move = Directions.WEST
            self.NewDir = 'W'
        elif west_east == 0 and north_south > 0 and Directions.NORTH in legal: 
            move = Directions.NORTH
            self.NewDir = 'N'
        elif west_east == 0 and north_south < 0 and Directions.SOUTH in legal: 
            move = Directions.SOUTH
            self.NewDir = 'S'

        elif north_south > 0 and north_south >= abs(west_east) and Directions.NORTH in legal: 
            move = Directions.NORTH
            self.NewDir = 'N'
        elif north_south < 0 and abs(north_south) >= abs(west_east) and Directions.SOUTH in legal: 
            move = Directions.SOUTH
            self.NewDir = 'S'
        elif west_east > 0 and west_east >= abs(north_south) and Directions.EAST in legal: 
            move = Directions.EAST
            self.NewDir = 'E'
        elif west_east < 0 and abs(west_east) >= abs(north_south) and Directions.WEST in legal: 
            move = Directions.WEST
            self.NewDir = 'W'

        elif north_south <= west_east and north_south>0 and self.NewDir!='N' and Directions.NORTH in legal: 
            move = Directions.NORTH
            self.NewDir = 'N' 
        elif north_south <= west_east and north_south<0 and self.NewDir!='S' and Directions.SOUTH in legal: 
            move = Directions.SOUTH
            self.NewDir = 'S' 
        elif north_south >= west_east and west_east>0 and self.NewDir!='E' and Directions.EAST in legal: 
            move = Directions.EAST
            self.NewDir = 'E'  
        elif north_south >= west_east and west_east<0 and self.NewDir!='W' and Directions.WEST in legal: 
            move = Directions.WEST
            self. NewDir = 'W' 

        else:
            for i in range(0,100):
                rnd = randint(1,4)
                if Directions.EAST in legal and rnd==1: 
                    move = Directions.EAST
                    self.NewDir = 'E'
                    break
                if Directions.WEST in legal and rnd==2: 
                    move = Directions.WEST
                    self.NewDir = 'W'
                    break
                if Directions.NORTH in legal and rnd==3: 
                    move = Directions.NORTH
                    self.NewDir = 'N'
                    break
                if Directions.SOUTH in legal and rnd==4: 
                    move = Directions.SOUTH
                    self.NewDir = 'S'
                    break

        #En caso de que se repita un movimiento sucesivamente en la misma posicion se prueba con otro aleatorio
        """if self.LastDir == self.Last3Dir and pacmanPositionLast2==pacmanPosition:            
                for i in range(0, 50):
                    rnd = randint(1,4)
                    if rnd == 1 and NewDir!='N' and Directions.NORTH in legal: 
                        move = Directions.NORTH 
                        break
                    if rnd == 2 and NewDir!='S' and Directions.SOUTH in legal: 
                        move = Directions.SOUTH
                        break
                    if rnd == 3 and NewDir!='E' and Directions.EAST in legal: 
                        move = Directions.EAST
                        break
                    if rnd == 4 and NewDir!='W' and Directions.WEST in legal: 
                        move = Directions.WEST
                        break

        elif self.NewDir == self.Last2Dir:            

                for i in range(0, 50):
                    rnd = randint(1,4)
                    if rnd == 1 and NewDir!='N' and Directions.NORTH in legal: 
                        move = Directions.NORTH 
                        break
                    if rnd == 2 and NewDir!='S' and Directions.SOUTH in legal: 
                        move = Directions.SOUTH
                        break
                    if rnd == 3 and NewDir!='E' and Directions.EAST in legal: 
                        move = Directions.EAST
                        break
                    if rnd == 4 and NewDir!='W' and Directions.WEST in legal: 
                        move = Directions.WEST
                        break
        
        self.Last3Dir=self.Last2Dir
        self.Last2Dir=self.LastDir
        self.LastDir=self.NewDir"""
        return move

    def printLineData(self, gameState):
        #tick = self.countActions
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        dimensionesMapa = width , height
        # Pacman position
        posicionPacman = gameState.getPacmanPosition()
        # Legal actions for Pacman in current position
        legalActions = gameState.getLegalPacmanActions()
        legal = ['None', 'None', 'None', 'None']
        if legalActions != None :
            for x in range(len(legalActions)):
                if str(legalActions[x]) == 'North': legal[0]='North'
                if str(legalActions[x]) == 'South': legal[1]='South'
                if str(legalActions[x]) == 'East': legal[2]='East'
                if str(legalActions[x]) == 'West': legal[3]='West'
            legalActions = legal
        if legalActions == None :
            legalActions = ['None', 'None', 'None', 'None']
        # Pacman direction
        direccionPacman = str(gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        numfantasmas = gameState.getNumAgents() - 1
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        fantasmasRestantes = gameState.getLivingGhosts()
        # Ghosts positions
        posicionFantasmas = gameState.getGhostPositions()
        # Ghosts directions
        direccionesFantasmas = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Manhattan distance to ghosts
        distanciasFantasmas = str(gameState.data.ghostDistances)
        distanciasFantasmas = distanciasFantasmas.replace('None', '1000')
        # Pending pac dots
        pacdotsRestantes = str(gameState.getNumFood())
        pacdotsRestantes = pacdotsRestantes.replace('None', '1000')
        # Manhattan distance to the closest pac dot
        distanciasPacdotMasCercano = gameState.getDistanceNearestFood()
        #if distanciasPacdotMasCercano == None: distanciasPacdotMasCercano=1000
        # Score
        score = gameState.getScore()

        ##Abrimos el fichero y escribimos en el
        string = posicionPacman, legalActions, direccionPacman, fantasmasRestantes, distanciasFantasmas, posicionFantasmas, pacdotsRestantes, distanciasPacdotMasCercano, score

        return str(string)
