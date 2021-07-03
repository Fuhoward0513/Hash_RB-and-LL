# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 00:09:33 2021

@author: asus
"""
from ..hashMap.HashMap import *
from ..dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt

def drawTimeToLoadFactor(NodeNum, LoadFactor):
    
    plt.figure()
    plt.title("Search Time To Load Factor")
    plt.xlabel("Load Factor")
    plt.ylabel("Averge Search Time")
    plt.legend()
    #Load_factor = [0.75, 1.5, 3, 6]
    Treeify_thershold = [1, 2, 4 , 8]
    for TH in Treeify_thershold:
        t = []
        LF_cnt = []
        dataList = load_words(NodeNum)
        random.shuffle(dataList)
        for LF in range(1, LoadFactor, 1):
            # insert N Nodes
            hashMap = HashMap(loadFactor=LF,TREEIFY_THRESHOLD=TH)
            for i in range(NodeNum):
                linkedNode = LLNode(dataList[i]["word"], dataList[i]["word"])
                hashMap.putValue(linkedNode)
        
            avg_n = 50
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
            LF_cnt.append(LF)
        plt.plot(LF_cnt, t, 'o', label = f"Treeify Threshold: {TH}")
        plt.legend()
        
    
    
    plt.show()
