from src.mazeData import *
from src.maze2025GraphClass import mazeGraph
from pyvis.network import Network
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from src.mazeProblemClass import MazeProblem
from src.agents import ProblemSolvingMazeAgentBFS
from src.naigationEnvironmentClass import MazeNavigationEnvironment
from src.Lab4Agents import EnemyShip

def makeMaze(n):
  size = (n,n)
  proba_0 =0.25 # resulting array will have 25%? of zeros
  proba_Enemy =0.1 # resulting array will have 10%? of enemy
  arrMaze=np.random.choice([0, 1, 2], size=size, p=[proba_0, 1-proba_0-proba_Enemy, proba_Enemy] ) #0=asteroid, 1=open, 2=enemy
  return arrMaze

def MazeCheck(mainMaze, initState, goalState):
  if (initState != 1):
    mainMaze[initState] = 1
  if (goalState != 1):
    mainMaze[goalState] = 1

class Lab4NavEnvironment(MazeNavigationEnvironment):
  def __init__(self, navGraph, maze):
    super().__init__(navGraph)
    self.maze = maze

  def execute_action(self, agent, action): #action and state are backwards here
      '''Check if agent alive, if so, execute action'''
      if self.is_agent_alive(agent):
          """Change agent's location -> agent's state;
          Track performance.
          -1 for each move."""
          
          agent.state=agent.update_state(agent.state, action)
          print(f"Agent in {agent.state} with performance = {agent.performance}")
          print(f"Action = {action} and State = {agent.state}")
          (x, y) = action
          if (self.maze[x][y] == 1): #if the agent is NOT under attack
            agent.performance -= 1
          else: #the spaceship is under attack (0's are walls, so they're ignored before this)
            print(f"Agent in {agent.state} is under attack!")
            enemy = EnemyShip() #dont know how else to put size in without requiring it for ~3 other functions
            if (agent.performance < enemy.power):
              agent.performance = 0 #dies instantly
            else:
              agent.performance = agent.performance*0.9 #removes 10% of performance
          self.update_agent_alive(agent)

'''
mazeSize=7
mainMaze = makeMaze(mazeSize)
mazeAvalActs=defineMazeAvailableActions(mainMaze)
maze1TM=makeMazeTransformationModel(mazeAvalActs)
mazeWorldGraph=mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

initState = (0,0)
goalState = (6,6)

mp1=MazeProblem(initState, goalState, mazeWorldGraph)
'''