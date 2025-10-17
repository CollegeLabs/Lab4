# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object
from src.mazeData import *
from src.maze2025GraphClass import mazeGraph
from src.PS_agentPrograms import *
from src.mazeProblemClass import MazeProblem
from src.agents import *
from src.naigationEnvironmentClass import MazeNavigationEnvironment
from src.Lab4Environment import *

nodeColors={
    "wall":"red",
    "path": "White",
    "Goal": "Green",
    "Start": "Yellow",
    "Enemy": "Orange"
}

def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.header("Resolving Maze Navigation Problem ...")
    e,a,c= opt[0],opt[1],opt[2]
    if not st.session_state["clicked"]:
        st.session_state["env"]=e
        st.session_state["agent"]=a
        st.session_state["nodeColors"]=c    
    
    if e.is_agent_alive(a):
        e.step()
        st.success(" Agent now at : {}.".format(a.state))
        st.info("Current Agent performance {}:".format(a.performance))
        c[a.state]="orange"
        st.info("State of the Environment:")
        buildGraph(e.status, c) 
    else:
        if a.state==a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))
        
    st.session_state["clicked"] = True
        
    
        
def buildGraph(graphData, nodeColorsDict):
    net_maze = Network(heading="Lab 4 Maze",
        bgcolor ="#242020",
        font_color = "white",
        height = "750px",
        width = "100%" 
    )
    net_maze.toggle_physics(False)
    nodes=graphData.nodes()
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    #for node in nodes:
        #g.add_node(node, color=nodeColorsDict[node])
    g.add_nodes_from(nodes)
    for node in g:
        node["color"]=nodeColorsDict[node]

    edges=[]
    for node_source in graphData.nodes():
        for node_target, dist in graphData.get(node_source).items():
            if set((node_source,node_target)) not in edges:
                edges.append(set((node_source,node_target)))                
    g.add_edges_from(edges)
    
    # generate the graph
    net_maze.from_nx(g)
    
    net_maze.save_graph('Maze.html')
    HtmlFile = open(f'Maze.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "white")
    return nodeColors
        
def makeMaze(n):
  size = (n,n)
  proba_0 =0.25 # resulting array will have 25%? of zeros
  proba_Enemy =0.1 # resulting array will have 10%? of enemy
  arrMaze=np.random.choice([0, 1, 2], size=size, p=[proba_0, 1-proba_0-proba_Enemy, proba_Enemy] )
  return arrMaze

def main():
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if "env" not in st.session_state:
        st.session_state["env"]=None
        
    if "agent" not in st.session_state:
        st.session_state["agent"]=None
        
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"]=None
        
    if not st.session_state["clicked"]:
        # Set header title
        st.header("Problem Solving Agents: Space Navigation Problem")
        st.header("_Initial Env._", divider=True)
        
        nodeColorsList=[]

        

        initState = (random.randint(0,6),random.randint(0,6))
        goalState = (random.randint(0,6),random.randint(0,6))

        mazeSize=7
        mainMaze = makeMaze(mazeSize)
        MazeCheck(mainMaze,initState,goalState)
        mazeAvalActs=defineMazeAvailableActions(mainMaze)
        maze1TM=makeMazeTransformationModel(mazeAvalActs)
        mazeWorldGraph=mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))
        #nodeColors=makeDefaultColors(romaniaGraph.graph_dict)
        for node in mazeWorldGraph.origin.keys():
            if mainMaze[node[0],node[1]]==1:
                nodeColorsList.append(nodeColors["path"])
            elif mainMaze[node[0],node[1]]==0:
                nodeColorsList.append(nodeColors["wall"])
            else:
                nodeColorsList.append(nodeColors["Enemy"])
        
        maze_Env1=MazeNavigationEnvironment(mazeWorldGraph, mainMaze)
        BFSmazeAgent1=ProblemSolvingMazeAgentBFS(initState, mazeWorldGraph, goalState)
        DLSAgent1=ProblemSolvingMazeAgentIDS(initState, mazeWorldGraph, goalState)       
                      
        maze_Env1.add_thing(BFSmazeAgent1)
        maze_Env1.add_thing(DLSAgent1)
        st.header("State of the Environment", divider="red")
        nodeColors[BFSmazeAgent1.state]="red"
        nodeColors[BFSmazeAgent1.goal]="green"
        buildGraph(mazeWorldGraph, nodeColors) 
        st.info(f"The Uniform Cost Search Agent in: {BFSmazeAgent1.state} with performance {BFSmazeAgent1.performance}.")
        st.info(f"The Iterative Deepened Search Agent in: {DLSAgent1.state} with performance {DLSAgent1.performance}.")
        st.info(f"Both Agents goal is: {BFSmazeAgent1.goal} .")
                
        drawBtn(maze_Env1,BFSmazeAgent1,nodeColors)
    
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            #st.warning("Agent Step Done!")
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"])
       
if __name__ == '__main__':
    main()