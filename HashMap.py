from drawLinkedLists import drawLinkedLists
from drawOneLinkedList import drawOneLinkedList
import random

class LLNode():
    def __init__(self, key, data):
        self.value = key
        self.data = data
        self.next = None
class TreeNode():
    def __init__(self, key, data):
        self.value = key
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.color = 'Black'

        self.data = data
class HashMap():
    TABLE_INITIAL_CAPACITY = 16
    TREEIFY_THRESHOLD = 8
    UNTREEIFY_THRESHOLD = 6
    loadFactor = 5
    MIN_TREEIFY_CAPACITY = 64

    def __init__(self):
        self.hashTable = [None] * HashMap.TABLE_INITIAL_CAPACITY
        self.totalElement = 0
    def getTableSize(self):
        return len(self.hashTable)
    def incrementTotal(self):
        self.totalElement = self.totalElement + 1
    def printMap(self):
        isExceedThre = 0
        print("----------------------Start printing hashTable---------------------")
        for i, bucket in enumerate(self.hashTable):
            cnt = 0
            print(i, end=" \t")
            while(bucket!=None):
                print("(%-1s)\t"%bucket.data, end="->")
                bucket = bucket.next
                cnt += 1
            if(cnt >= HashMap.TREEIFY_THRESHOLD):
                isExceedThre += 1
            print("NONE",end="\n")
        print("Probability of treeify: ",isExceedThre)
        print("----------------------End printing hashTable---------------------")
    def hashCodeString(self, key):
        hashValue = 0
        for char in key:
            hashValue = hashValue * 31 + ord((char))
        return hashValue % self.getTableSize()
    def hashCodeInteger(self, key):
        return key % self.getTableSize()
    def treeifyBin(self):
        print("Treeify!")

    def tableRehash(self):
        # Because we didn't store hash value, we calculate hash value for each node again.
        print("------------------------Start rehashing------------------------------")
        newTable = [None]*self.getTableSize()
        rehashNodes = []
        for bucket in self.hashTable:
            # traverse every nodes in the bin.
            traveler = bucket
            while(traveler!=None):
                rehashNodes.append(traveler)
                traveler = traveler.next   
        print("before rehash, total element:", self.totalElement )
        self.hashTable = newTable
        self.totalElement = 0
        print("rehashnodes size: ",len(rehashNodes))
        for node in rehashNodes:
            node.next = None
            self.putValue(node)
        mylist = [node.next for node in rehashNodes]
        print("------------------------End rehashing--------------------------------")


    def putValue(self, newNode):
        print('Hashing a node with key: \t\t',newNode.value)
        hashValue = self.hashCodeInteger(newNode.value)
        root = self.hashTable[hashValue]
        if(root == None): # empty space
            self.hashTable[hashValue] = newNode
            self.incrementTotal()
            print("root ",hashValue," is empty. Add node.\tNo.", self.totalElement)
        else: # Already somebody there.
            if(root.value == newNode.value): # if exact same key, override.
                self.hashTable[hashValue] = newNode
                print("Existed root ",hashValue,". Override.\tNo.",self.totalElement)
            elif(isinstance(root, TreeNode)): # if it's a tree, addtreeVal
                print("Root ",hashValue," is tree. PutTreeValue.")
                pass
            else: # it's LL.
                print("Root ",hashValue," exists, LL found.")
                binCount = 0
                while(root!=None):
                    print("Traveling at position", binCount)
                    if(root.next == None):
                        root.next = newNode
                        self.incrementTotal()
                        binCount += 1
                        print("Add node at position",binCount, " \tNo.", self.totalElement)
                        if(binCount >= HashMap.TREEIFY_THRESHOLD):
                            self.treeifyBin()
                            print("Excess treeify_threshold, treeify.")
                        break
                    if(root.next.value == newNode.value): # if exact same key, override.
                        print("Existed same node at", binCount, ". Override.\tNo. ",self.totalElement)
                        root.next = newNode
                        break
                    binCount += 1
                    root = root.next

        threshold = self.getTableSize() * HashMap.loadFactor
        if(self.totalElement > threshold):
            self.tableResize()

    def tableResize(self):
        threshold = self.getTableSize() * HashMap.loadFactor
        print("=================================Start Resizing. from ",self.getTableSize()," to ", 2*self.getTableSize()," because exceed threshold: ",threshold,"=============================")
        originalSize = self.getTableSize()
        addTable = [None] * originalSize
        self.hashTable += addTable
        self.tableRehash()

    def treeifyBin(self):
        # if(self.getTableSize() < HashMap.MIN_TREEIFY_CAPACITY):
        #     self.tableResize()
        # else if ()
        pass





if __name__ == '__main__':
    hashMap = HashMap()
    
    insertNodeNum = 70

    for i in range(insertNodeNum):
        linkedNode = LLNode(random.randint(1,100000000), i)
        hashMap.putValue(linkedNode)
        # drawer = drawOneLinkedList(rootNode)
        # drawer.draw()
    print('=====%========%==========%=========%=========%=======%========%=======')
    print("End, totalElement: ",hashMap.totalElement)
    print("End. HashTableSize: ",hashMap.getTableSize())
    hashMap.printMap()
