from HashMap import *
from dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.special import factorial
import scipy.stats as stats
import numpy as np
import math


insertNodeNum = 370103

hashMap = HashMap(loadFactor=500,TREEIFY_THRESHOLD=8)
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
x = []
y = []
p = []
for key in rootTypeNum:
    x.append(key)
    y.append(rootTypeNum[key])
for num in y:
    p.append(num/hashMap.getTableSize())
plt.bar(x, p, label='HashMap settings: load factor=%.2f, treeify threshold=%d' %(hashMap.loadFactor, hashMap.TREEIFY_THRESHOLD))
plt.title("Number of bins that contain certain amounts of nodes")
plt.xlabel("nodes in bin")
plt.ylabel("Probability")
#####################################
Lambda = np.average([key for key in rootTypeNum], weights=[rootTypeNum[key] for key in rootTypeNum])
print("Experimental weighted average of 'nodes in bins':",Lambda)
# t = np.arange(min(x), max(x), 0.1)
# d = np.exp(-Lambda)*np.power(Lambda, t)/factorial(t)
# plt.plot(t, d, 'rs',label=r"Poisson Distribution with $\lambda$=%.2f"%Lambda)
#####################################
mu = Lambda
variance = Lambda
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma),'gs', label=r"Normal Distribution with $\mu$=%.2f, $\sigma$=%.2f"%(Lambda, math.sqrt(Lambda)))
plt.legend()
plt.show()
print("Time to construct map: ", t2-t1, "seconds.")
print("average searching time: {:.20f}".format((t4-t3)/insertNodeNum))