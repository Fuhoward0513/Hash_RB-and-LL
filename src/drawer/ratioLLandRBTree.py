from .poissonDraw import drawDistribution
import matplotlib.pyplot as plt
import pickle

'''
In drawRatioLLandRBTree, we want to know how LF, TT affect the numbers of LL and RBTree.
Note that both LF and nodeNum can affect lambda(you can see it as "average length of bin".), so here we fix LF.
Besides, the numbers of LL and RBTree are mainly affected by lambda and TT, so here we fix TT.
As a result, we fix LF and TT, and see how number of nodes can affect ratio of LL and RBTRee.
After conducting many times of experiments, we plot the number of LL, RBTree, Empty node for each experiment.
'''

def drawRatioLLandRBTree(LF=3, TT=3, drawing=True):

    numberNodes = []
    LLY = []
    RBTreeY = []
    EmptyY = []
    ratioY = []
    for n in range(5000, 150000, 1000):
        expX, expP, normX, normY, poissonX, poissonY, Lambda, rootType = drawDistribution(
            nodeNum=n,
            loadFactor=LF,
            drawing=False,
            TREEIFY_THRESHOLD=TT
        )
        numberNodes.append(n)
        LL = rootType["LinkedList"]
        RBTree = rootType["RBTree"]
        empty = rootType["Empty"]
        LLY.append(LL)
        RBTreeY.append(RBTree)
        EmptyY.append(empty)
    # ratioY.append(LL)

    with open("numberNodes.txt", "wb") as fp:   #Pickling
        pickle.dump(numberNodes, fp)
    with open("LLY.txt", "wb") as fp:   #Pickling
        pickle.dump(LLY, fp)
    with open("RBTreeY.txt", "wb") as fp:   #Pickling
        pickle.dump(RBTreeY, fp)
    with open("EmptyY.txt", "wb") as fp:   #Pickling
        pickle.dump(EmptyY, fp)    

    with open("numberNodes.txt", "rb") as fp:   #Unpickling
        numberNodes = pickle.load(fp)
    with open("LLY.txt", "rb") as fp:   #Unpickling
        LLY = pickle.load(fp)
    with open("RBTreeY.txt", "rb") as fp:   #Unpickling
        RBTreeY = pickle.load(fp)
    with open("EmptyY.txt", "rb") as fp:   #Unpickling
        EmptyY = pickle.load(fp)

    print("number of nodes:",numberNodes)
    print("Number of Linked List",LLY)
    print("Number of RBTree",RBTreeY)
    print("Number of Empty",EmptyY)
    if (drawing == True):
        plt.figure()
        plt.title("Type(Linked List/RBTree) vs. number of nodes, with load factor = %d, Treeify Threshold = %d"%(LF, TT))
        plt.xlabel("number of nodes")
        plt.ylabel("Numbers")
        plt.plot(numberNodes,LLY,'bs', label="Linked List")
        plt.plot(numberNodes,RBTreeY,'rs', label="RBTree")
        plt.plot(numberNodes,EmptyY,'k.', label="Empty")
        plt.legend()
        plt.show()

if __name__ == '__main__':
    LF = 3 # Load Factor
    TT = 3 # Treeify Threshold
    drawRatioLLandRBTree(LF=LF, TT=TT, drawing=True)