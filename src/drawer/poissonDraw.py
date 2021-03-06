from ..hashMap.HashMap import *
from ..dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt
from scipy.special import factorial
import scipy.stats as stats
import numpy as np
import math

'''
In "drawDistribution", we take nodeNum, loadFactor, TREEIFY_THRESHOLD as arguments. 
Given these parameters, we can conduct a single time of experiment. 
Then, for different length of bins, we sum up the number of bins. For example, {3:2834, ...} means there are 2834 bins that have 3 nodes within it.
In the same figure, we also plot 
1. poisson distribution(with lambda equal to the weighted average of experimental results)
2. normal distribution(with mu and variance both equal to the lambda in poisson distribution.) 
'''

def drawDistribution(nodeNum, loadFactor, drawing, TREEIFY_THRESHOLD=8):
    insertNodeNum = nodeNum
    hashMap = HashMap(loadFactor=loadFactor,TREEIFY_THRESHOLD=TREEIFY_THRESHOLD)
    dataList = load_words(insertNodeNum)
    random.shuffle(dataList)

    t1 = time()
    for i in range(insertNodeNum):
        linkedNode = LLNode(dataList[i]["word"], dataList[i]["word"])
        hashMap.putValue(linkedNode)
    t2 = time()

    # hashMap.printMap()
    rootType, rootTypeNum = hashMap.computeTreeifyRatio()

    t3 = time()
    for element in dataList:
        findKey = element["word"]
        data = hashMap.findElementInMap(findKey)
    t4 = time()

    print('=====%========%==========%=========%=========%=======%========%=======')
    print("Treeify threshold:", hashMap.TREEIFY_THRESHOLD)
    print("Load factor:",hashMap.loadFactor)
    print("End, totalElement: ",hashMap.totalElement)
    print("End. HashTableSize: ",hashMap.getTableSize())
    print(rootType["LinkedList"],"roots are Linked List,",rootType["RBTree"],"are RBTree, and",rootType["Empty"],"are empty bins.")
    print("Length Frequency: ",rootTypeNum)
    print("Time to construct map: ", t2-t1, "seconds.")
    print("average searching time: {:.20f}".format((t4-t3)/insertNodeNum))

    ######################### Drawing ###########################
    expX = []
    n = []
    expP = []
    for key in rootTypeNum:
        expX.append(key)
        n.append(rootTypeNum[key])
    for num in n:
        expP.append(num/hashMap.getTableSize())
    Lambda = np.average([key for key in rootTypeNum], weights=[rootTypeNum[key] for key in rootTypeNum])
    ############## Normal Distribution ##############
    mu = Lambda
    variance = Lambda
    sigma = math.sqrt(variance)
    normX = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    normY = stats.norm.pdf(normX, mu, sigma)
    print("Experimental weighted average of 'nodes in bins':",Lambda)
    ############### Poisson ################
    poissonX = []
    poissonY = []
    if(nodeNum <= 50000):
        poissonX = np.arange(min(expX), max(expX), 0.1)
        poissonY = np.exp(-Lambda)*np.power(Lambda, poissonX)/factorial(poissonX)
    ############### Plot and Show ###############
    if (drawing == True):
        plt.figure()
        plt.title("Number of bins that contain certain amounts of nodes")
        plt.xlabel("nodes in bin")
        plt.ylabel("Probability")
        plt.bar(expX, expP,label='HashMap settings: load factor=%.2f' %(hashMap.loadFactor))
        # plt.plot(normX, normY, "g-",linewidth=4,label=r"Normal Distribution with $\mu$=%.2f, $\sigma$=%.2f"%(Lambda, math.sqrt(Lambda)))
        plt.plot(poissonX, poissonY,"r-",linewidth=4, label=r"Poisson Distribution with $\lambda$=%.2f"%Lambda)
        plt.legend()
        plt.show()

    return expX, expP, normX, normY, poissonX, poissonY, Lambda, rootType


if __name__ == '__main__':
    drawDistribution(nodeNum=200000,loadFactor=300, drawing=True,TREEIFY_THRESHOLD=8)

