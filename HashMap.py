from drawLinkedLists import drawLinkedLists
from drawOneLinkedList import drawOneLinkedList
import random
from RBTree.RedBlackTree import RBTree
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

        self.prev = None
        self.next = None
        self.data = data


class HashMap():
    TABLE_INITIAL_CAPACITY = 4
    TREEIFY_THRESHOLD = 3
    UNTREEIFY_THRESHOLD = 6
    loadFactor = 3
    MIN_TREEIFY_CAPACITY = 64

    def __init__(self):
        self.hashTable = [None] * HashMap.TABLE_INITIAL_CAPACITY
        self.totalElement = 0
    def getTableSize(self):
        return len(self.hashTable)
    def incrementTotal(self):
        self.totalElement = self.totalElement + 1
    def printMap(self):
        print("----------------------Start printing hashTable---------------------")
        for i, bucket in enumerate(self.hashTable):
            print(i,type(bucket).__name__, end=" \t")
            if(isinstance(bucket, RBTree)):
                bucket.printInorder(bucket.root)
                print("RBTree inorder traverse completed.",end="\n")
                continue
            while(bucket!=None):
                print("(%-1s)\t"%bucket.data, end="->")
                bucket = bucket.next
            print("NONE",end="\n")
        print("----------------------End printing hashTable---------------------")
    def hashCodeString(self, key):
        hashValue = 0
        for char in key:
            hashValue = hashValue * 31 + ord((char))
        return hashValue % self.getTableSize()
    def hashCodeInteger(self, key):
        return key % self.getTableSize()

    def tableRehash(self):
        # Because we didn't store hash value, we calculate hash value for each node again.
        print("------------------------Start rehashing------------------------------")
        newTable = [None]*self.getTableSize()
        rehashNodes = []
        for bucket in self.hashTable:
            # traverse every nodes in the bin.
            traveler = bucket
            while(traveler!=None):
                if(isinstance(traveler, RBTree)):
                    # The bucket is a RBtree. Take out all nodes in it and break while.
                    traveler.getAllTreeNodes(traveler.root)
                    print("rehashing, the tree all nodes: ", traveler.allNodes)
                    for node in traveler.allNodes:
                        rehashNodes.append(node)
                    break
                rehashNodes.append(traveler)
                traveler = traveler.next
           
        print("before rehash, total element:", self.totalElement )
        self.hashTable = newTable
        self.totalElement = 0
        print("rehashnodes size: ",len(rehashNodes))
        for node in rehashNodes:
            node.next = None
            self.putValue(node)
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
            if(isinstance(root, RBTree)): # if it's a tree, addtreeVal
                print("Root ",hashValue," is tree. PutTreeValue.")
                root.insert(self.LL2TreeNode(newNode))
                self.incrementTotal()
            elif(root.value == newNode.value): # if exact same key, override.
                self.hashTable[hashValue] = newNode
                print("Existed root ",hashValue,". Override.\tNo.",self.totalElement)
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
                            print("Excess treeify_threshold, treeify.")
                            self.treeifyBin(hashValue)
                        break
                    if(root.next.value == newNode.value): # if exact same key, override.
                        print("Existed same node at", binCount, ". Override.\tNo. ",self.totalElement)
                        root.next = newNode
                        break
                    binCount += 1
                    root = root.next

        threshold = self.getTableSize() * HashMap.loadFactor
        if(self.totalElement > threshold):
            print("=================================Start Resizing. from ",self.getTableSize()," to ", 2*self.getTableSize()," because exceed threshold: ",threshold,"=============================")
            self.tableResize()

    def tableResize(self):
        originalSize = self.getTableSize()
        addTable = [None] * originalSize
        self.hashTable += addTable
        self.tableRehash()

    def treeifyBin(self, hashValue):
        if(self.getTableSize() < HashMap.MIN_TREEIFY_CAPACITY):
            print("=================================Start Resizing. from ",self.getTableSize()," to ", 2*self.getTableSize()," because meet treeifyBin before MIN TEEIFY CAPACITY ",HashMap.MIN_TREEIFY_CAPACITY,"=============================")
            self.tableResize()
        else:
            rbTree = RBTree()
            traveler = self.hashTable[hashValue]
            while(traveler!=None):
                rbTree.insert(self.LL2TreeNode(traveler))
                traveler = traveler.next
            self.hashTable[hashValue] = rbTree
        
    def LL2TreeNode(self, LLNode):
        treeNode = TreeNode(key=LLNode.value, data=LLNode.data)
        return treeNode

    def findElementInMap(self, key):
        print("Start finding data with key: ", key)
        hashValue = self.hashCodeInteger(key)
        findRoot = self.hashTable[hashValue]
        if(isinstance(findRoot, RBTree)):
            print("In treee!")
            return findRoot.searchMap(key)
        else:
            traveler = findRoot
            while(traveler!=None):
                if(traveler.value == key):
                    print("In linked list!")
                    return traveler.data
                traveler = traveler.next







if __name__ == '__main__':
    hashMap = HashMap()
    
    insertNodeNum = 200

    for i in range(insertNodeNum):
        linkedNode = LLNode(random.randint(1,100000000), i)
        # linkedNode = LLNode(i*100, i)
        hashMap.putValue(linkedNode)
        # drawer = drawOneLinkedList(rootNode)
        # drawer.draw()
    print('=====%========%==========%=========%=========%=======%========%=======')
    print("End, totalElement: ",hashMap.totalElement)
    print("End. HashTableSize: ",hashMap.getTableSize())
    hashMap.printMap()
    findKey = 101
    data = hashMap.findElementInMap(findKey)
    if(data != None):
        print("Found key: ",findKey, ", value: ", data)
    else:
        print("Not Found key: ",findKey)