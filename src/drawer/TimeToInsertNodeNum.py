# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 00:10:31 2021

@author: asus
"""

from ..hashMap.HashMap import *
from ..dataLoader.wordLoader import csvLoader, load_words
import random
from time import time 
import matplotlib.pyplot as plt

def drawTimeToInsertNodeNum(NodeNum):
    
    plt.figure()
    plt.title("Time to InsertNodeNum")
    plt.xlabel("InsertNodeNum")
    plt.ylabel("Time")
    plt.legend()
    Load_factor = [0.75, 1.5, 3, 6]
    Treeify_thershold = [1, 2, 4 , 8]
    for TH in Treeify_thershold:
        t = []
        Node_cnt = []
        for i in range(100, NodeNum, 100):
            time_sum = 0
            avg_n = 10
            dataList = load_words(i)
            random.shuffle(dataList)
            for j in range(avg_n):
                hashMap = HashMap(loadFactor=0.75,TREEIFY_THRESHOLD=TH)
                t1 = time()
                for k in range(i):
                    linkedNode = LLNode(dataList[k]["word"], dataList[k]["word"])
                    hashMap.putValue(linkedNode)
                t2 = time()
                time_sum = time_sum + (t2-t1)
            
            print(f"insert {i} Nodes !")
            print(f"Average Time Cost of Inserting {i} Nodes:", time_sum/avg_n)
            t.append(time_sum/avg_n)
            Node_cnt.append(i)
        plt.plot(Node_cnt, t, 's', label = f"Treeify Thershold: {TH}")
        # plt.plot(Node_cnt, t, label = f"Load_factor: {LF}")
        plt.legend()
        
    
    
    plt.show()
        
        
