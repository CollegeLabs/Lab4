from src.mazeData import *
from src.maze2025GraphClass import mazeGraph
from pyvis.network import Network
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from src.mazeProblemClass import MazeProblem
from src.agents import ProblemSolvingMazeAgentBFS
from src.naigationEnvironmentClass import MazeNavigationEnvironment

def makeMaze(n):
  size = (n,n)
  proba_0 =0.25 # resulting array will have 25%? of zeros
  proba_Enemy =0.1 # resulting array will have 10%? of enemy
  arrMaze=np.random.choice([0, 1, 2], size=size, p=[proba_0, 1-proba_0-proba_Enemy, proba_Enemy] )
  return arrMaze

def MazeCheck(mainMaze, initState, goalState):
  if (initState != 1):
    mainMaze[initState] = 1
  if (goalState != 1):
    mainMaze[goalState] = 1


mazeSize=7
mainMaze = makeMaze(mazeSize)
mazeAvalActs=defineMazeAvailableActions(mainMaze)
maze1TM=makeMazeTransformationModel(mazeAvalActs)
mazeWorldGraph=mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

initState = (0,0)
goalState = (6,6)

mp1=MazeProblem(initState, goalState, mazeWorldGraph)