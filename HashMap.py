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
    loadFactor = 0.75

    def __init__(self):
        self.hashTable = [None] * HashMap.TABLE_INITIAL_CAPACITY
        self.totalElement = 0
    def getTableSize(self):
        return len(self.hashTable)
    def incrementTotal(self):
        self.totalElement = self.totalElement + 1
    def printMap(self):
        print(self.hashTable)
    def hashCodeString(self, key):
        hashValue = 0
        for char in key:
            hashValue = hashValue * 31 + ord((char))
        return hashValue % self.getTableSize()
    def hashCodeInteger(self, key):
        return key % self.getTableSize()
    def treeifyBin(self):
        print("Treeify!")
    def putValue(self, newNode):
        hashValue = self.hashCodeInteger(newNode.value)
        print(hashValue)
        root = self.hashTable[hashValue]
        if(root == None): # empty space
            self.hashTable[hashValue] = newNode
            self.incrementTotal()
            print("root is empty. Add node.")
        else: # Already somebody there.
            if(root.value == newNode.value): # if exact same key, override.
                self.hashTable[hashValue] = newNode
                self.incrementTotal()
                print("Existed node at root. Override.")
            elif(isinstance(root, TreeNode)): # if it's a tree, addtreeVal
                print("Root is tree. PutTreeValue.")
                pass
            else: # it's LL.
                print("Root exists and it's root of LL.")
                while(root!=None):
                    binCount = 0
                    print("Traveling...at position", binCount)
                    if(root.next == None):
                        root.next = newNode
                        self.incrementTotal()
                        binCount += 1
                        print("Add node at position",binCount)
                        if(binCount >= HashMap.TREEIFY_THRESHOLD - 1):
                            self.treeifyBin()
                            print("Excess treeify_threshold, treeify.")
                        break
                    if(root.next.value == newNode.value): # if exact same key, override.
                        print("Existed node at", binCount, ". Override.")
                        root.next = newNode
                        self.incrementTotal()
                    root = root.next

            threshold = self.getTableSize() * HashMap.loadFactor
            if(self.totalElement > threshold):
                print(self.totalElement, threshold)
                originalSize = self.getTableSize()
                addTable = [None] * originalSize
                self.hashTable += addTable
                print("Resize", self.hashTable)







if __name__ == '__main__':
    hashMap = HashMap()
    hashMap.printMap()
    
    for i in range(100):
        linkedNode = LLNode(random.randint(1,10000), i)
        hashMap.putValue(linkedNode)
    for i in range(100):
        rootNode = hashMap.hashTable[i]
        # drawer = drawOneLinkedList(rootNode)
        # drawer.draw()
    print(hashMap.totalElement)
    print(hashMap.getTableSize())

