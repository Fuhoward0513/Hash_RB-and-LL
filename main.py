from src.drawer.loadFactorWithAvg import drawLFandLambda
from src.drawer.poissonDraw import drawDistribution
from src.drawer.ratioLLandRBTree import drawRatioLLandRBTree
from src.drawer.TimeToConstructMap import drawTimeToConstructMap
from src.drawer.SearchTimeToNodeNum import drawTimeToSearch_N_Node

#### see description in the following modules ####

drawDistribution(nodeNum=50000,loadFactor=5, drawing=True)
drawLFandLambda(nodeNum=10000)
drawRatioLLandRBTree(TT=4, drawing=True)
drawTimeToConstructMap(10000)
drawTimeToSearch_N_Node(10000)

