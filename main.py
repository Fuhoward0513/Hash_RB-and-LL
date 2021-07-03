from src.drawer.loadFactorWithAvg import drawLFandLambda
from src.drawer.poissonDraw import drawDistribution
from src.drawer.ratioLLandRBTree import drawRatioLLandRBTree
from src.drawer.TimeToConstructMap import drawTimeToConstructMap
from src.drawer.SearchTimeToNodeNum import drawTimeToSearch_N_Node
from src.drawer.TimeToLoadFactor import drawTimeToLoadFactor
from src.drawer.TimeToTreeifyTheshold import drawTreeifyThershold

#### see description in the following modules ####

# drawDistribution(nodeNum=50000,loadFactor=5, drawing=True)
# drawLFandLambda()
drawRatioLLandRBTree(TT=4, drawing=True)
# drawTimeToConstructMap(10000)
# drawTimeToSearch_N_Node(10000)
# drawTimeToLoadFactor(10000, 300)
# drawTreeifyThershold(10000)

