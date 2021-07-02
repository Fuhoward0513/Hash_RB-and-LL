from poissonDraw import drawDistribution
import matplotlib.pyplot as plt
import pickle

LFX_ratio = []
LLY = []
RBTreeY = []
ratioY = []
for LF in range(5, 100, 5):
    expX, expP, normX, normY, poissonX, poissonY, Lambda, rootType = drawDistribution(nodeNum=200000,loadFactor=LF, drawing=False)
    LFX_ratio.append(LF)
    LL = rootType["LinkedList"]
    RBTree = rootType["RBTree"]
    LLY.append(LL)
    RBTreeY.append(RBTree)
# ratioY.append(LL)

# with open("LFX_ratio.txt", "wb") as fp:   #Pickling
#     pickle.dump(LFX_ratio, fp)
# with open("LLY.txt", "wb") as fp:   #Pickling
#     pickle.dump(LLY, fp)
# with open("RBTreeY.txt", "wb") as fp:   #Pickling
#     pickle.dump(RBTreeY, fp)

# with open("LFX_ratio.txt", "rb") as fp:   #Unpickling
#     LFX_ratio = pickle.load(fp)
# with open("LLY.txt", "rb") as fp:   #Unpickling
#     LLY = pickle.load(fp)
# with open("RBTreeY.txt", "rb") as fp:   #Unpickling
#     RBTreeY = pickle.load(fp)

print("load factor:",LFX_ratio)
print("Number of Linked List",LLY)
print("Number of RBTree",RBTreeY)
plt.title("Type(Linked List/RBTree) vs. load factor")
plt.xlabel("load factor")
plt.ylabel("Numbers")
plt.plot(LFX_ratio,LLY,'rs', label="Linked List")
plt.plot(LFX_ratio,RBTreeY,'gs', label="RBTree")
plt.legend()
plt.show()