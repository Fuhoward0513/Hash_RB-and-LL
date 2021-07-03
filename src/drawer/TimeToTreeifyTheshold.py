# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 00:09:50 2021

@author: asus
"""

from ..hashMap.HashMap import *
from ..dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt

def drawTreeifyThershold(NodeNum):
    
    plt.figure()
    plt.title("Search Time To Treeify Thershold")
    plt.xlabel("Treeify Thershold")
    plt.ylabel("Averge Search Time")
    plt.legend()
    Load_factor = [0, 50, 100, 150]
    # Treeify_thershold = [1, 2, 4 , 8]
    for LF in Load_factor:
        t = []
        TH_cnt = []
        dataList = load_words(NodeNum)
        random.shuffle(dataList)
        for TH in range(1, 121, 1):
            # insert N Nodes
            hashMap = HashMap(loadFactor=LF,TREEIFY_THRESHOLD=TH)
            for i in range(NodeNum):
                linkedNode = LLNode(dataList[i]["word"], dataList[i]["word"])
                hashMap.putValue(linkedNode)
        
            avg_n = 10
            time_sum = 0
            # calculation averge time to search N node with diff loadfactor
            for j in range(avg_n):
                t1 = time()
                for element in dataList:
                    findKey = element["word"]
                    data = hashMap.findElementInMap(findKey)
                t2 = time()
                time_sum = time_sum + (t2-t1)
            
            print(f"insert {i} Nodes !")
            print(f"Average Time Cost of Searching {i} Nodes:", time_sum/avg_n)
            t.append(time_sum/avg_n)
            TH_cnt.append(TH)
        plt.plot(TH_cnt, t, 'o', label = f"Load Factor: {LF}")
        plt.legend()
    
    plt.show()