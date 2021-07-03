# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 10:10:56 2021

@author: asus
"""

from ..hashMap.HashMap import *
from ..dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt

def drawTimeToSearch_N_Node(NodeNum):
    
    plt.figure()
    plt.title("Time To Search N-Node(load Factor=100)")
    plt.xlabel("NodeNum")
    plt.ylabel("Time")
    plt.legend()
    Load_factor = [0.75, 1.5, 3, 6]
    Treeify_thershold = [10, 30, 60, 120]
    for TH in Treeify_thershold:
        t = []
        Node_cnt = []
        for i in range(100, NodeNum, 100):
            time_sum = 0
            avg_n = 10
            dataList = load_words(i)
            random.shuffle(dataList)
            
            # insert N Nodes
            hashMap = HashMap(loadFactor=100,TREEIFY_THRESHOLD=TH)
            for k in range(i):
                linkedNode = LLNode(dataList[k]["word"], dataList[k]["word"])
                hashMap.putValue(linkedNode)
            
            # calculation averge time to search N node
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
            Node_cnt.append(i)
        plt.plot(Node_cnt, t, 'o', label = f"Treeify Thershold: {TH}")
        # plt.plot(Node_cnt, t, label = f"Load_factor: {LF}")
        plt.legend()
        
    
    
    plt.show()