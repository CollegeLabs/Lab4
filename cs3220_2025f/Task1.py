from src.mazeData import *
from src.maze2025GraphClass import mazeGraph
from pyvis.network import Network
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from src.mazeProblemClass import MazeProblem
from src.agents import ProblemSolvingMazeAgentBFS
from src.naigationEnvironmentClass import MazeNavigationEnvironment

mazeSize=7
mainMaze = makeMaze(mazeSize)
mazeAvalActs=defineMazeAvailableActions(mainMaze)
maze1TM=makeMazeTransformationModel(mazeAvalActs)
mazeWorldGraph=mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

net_maze = Network(heading="Lab 4 Maze",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%" 
)
nodeColors={
    "wall":"red",
    "path": "white"
}
nodeColorsList=[]

for node in mazeWorldGraph.origin.keys():
    if mainMaze[node[0],node[1]]==1:
        nodeColorsList.append(nodeColors["path"])
    else:
        nodeColorsList.append(nodeColors["wall"])

nodes=["-".join(str(item) for item in el) for el in mazeWorldGraph.origin.keys()]

x_coords = []
y_coords = []

for node in mazeWorldGraph.origin.keys():
    x,y=mazeWorldGraph.getLocation(node)
    x_coords.append(x)
    y_coords.append(y)

sizes=[10]*len(nodes)
net_maze.add_nodes(nodes, color=nodeColorsList, x=x_coords, y=y_coords, size=sizes, title=nodes)

for node in net_maze.nodes:
    node['label']=''

edge_weights = {(intTupleTostr(k), intTupleTostr(v2)) : k2 for k, v in mazeWorldGraph.origin.items() for k2, v2 in v.items()}

edges=[]

for node_source in mazeWorldGraph.nodes():
    for node_target, action in mazeWorldGraph.get(node_source).items():
        #node_target or node_source is a tuple -> convert to str
        if (intTupleTostr(node_source),intTupleTostr(node_target)) not in edges and (intTupleTostr(node_target), intTupleTostr(node_source)):
            net_maze.add_edge(intTupleTostr(node_source),intTupleTostr(node_target), label=edge_weights[(intTupleTostr(node_source),intTupleTostr(node_target))])
            edges.append((intTupleTostr(node_source),intTupleTostr(node_target)))

net_maze.toggle_physics(False)
#net_maze.show("graph1.html", notebook=False)

initState = (0,0)
goalState = (4,4)
mp1=MazeProblem(initState, goalState, mazeWorldGraph)

BFSAgent=BestFirstSearchAgentProgram()
#print("BFSAgent: \n")
#seq=BFSAgent(mp1)

BFSmazeAgent1=ProblemSolvingMazeAgentBFS(initState, mazeWorldGraph, goalState)

maze_Env1=MazeNavigationEnvironment(mazeWorldGraph)
