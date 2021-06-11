# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 13:24:09 2021

@author: asus
"""
import argparse

class Node():
    def __init__(self, key):
        self.value = key
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.color = 'Black'
    
    def __repr__(self):
        return str(self.value)

class RBTree():
    def __init__(self):
        self.root = None
    
    """ Search """
    def search(self, key, output):
        if(self.root==None):
            return
        else:
            self._search(self.root, key, output)
            output.write('\n')
            
    def _search(self, node, key, output):
        if(key < node.value):
            if(node.left_child==None):
                return
            else:
                self._search(node.left_child, key, output)
        elif(key > node.value):
            if(node.right_child==None):
                return
            else:
                self._search(node.right_child, key, output)
        else:
            # return node.value
            val = node.value
            col = node.color
            output.write(f'{val}: {col} ')
    
    """ Insert """
    def insert(self, key):
        if(self.root==None):
            print('insert:', key)
            self.root = Node(key)
            self.root.color = "Black"
        else:
            print('insert:', key)
            self._insert(self.root, key)
            
    def _insert(self, node, key):
        if(key < node.value):
            if(node.left_child==None):
                node.left_child = Node(key)
                node.left_child.color = 'Red'
                node.left_child.parent = node
                self._insert_fixnode(node.left_child)
            else:
                self._insert(node.left_child, key)
        elif(key > node.value):
            if(node.right_child==None):
                node.right_child = Node(key)
                node.right_child.color = 'Red'
                node.right_child.parent = node
                self._insert_fixnode(node.right_child)
            else:
                self._insert(node.right_child, key)
        else:
            print("item already existed")
    
    def find_uncle(self, node): # 找 parent 旁邊的 node
        grandparent = node.parent.parent
        parent = node.parent
        if(grandparent.value < parent.value):
            return grandparent.left_child
        elif(grandparent.value > parent.value):
            return grandparent.right_child
    
    def _insert_fixnode(self, node): # balance the Tree
        # case 1: parent is "Black"
        if(node.parent==None):
            node.color = 'Black'
        else:
            if(node.parent.color=="Black"):
                return
            # case 2: parent is "Red" 
            elif(node.parent.color=='Red'):
                uncle = self.find_uncle(node)
                grandparent = node.parent.parent
                
                if(self._color(uncle)=='Red'): # recolor, no rotation
                    node.parent.color = 'Black'
                    uncle.color = 'Black'
                    grandparent.color = 'Red'
                    self._insert_fixnode(grandparent)
                
                elif(self._color(uncle)=='Black'): # recolor, rotation
                    if(node.value < node.parent.value and node.parent.value < grandparent.value): #LL Rotation
                        self._insert_LL_Rotation(node)
                    elif(node.value > node.parent.value and node.parent.value < grandparent.value): #LR Rotation
                        self._insert_LR_Rotation(node)
                    elif(node.value > node.parent.value and node.parent.value > grandparent.value): #RR Rotation
                        self._insert_RR_Rotation(node)
                    elif(node.value < node.parent.value and node.parent.value > grandparent.value): #RL Rotation
                        self._insert_RL_Rotation(node)
            
            
    def _insert_LL_Rotation(self, node):
        # Rotate
        grandparent = node.parent.parent
        parent = node.parent
        
        if(grandparent.parent!=None):
            if(grandparent.parent.value < grandparent.value):
                grandparent.parent.right_child = parent # grandparent's parent connect to  node's parent
                parent.parent = grandparent.parent
            elif(grandparent.parent.value > grandparent.value):
                grandparent.parent.left_child = parent
                parent.parent = grandparent.parent
        else:
            self.root = parent
            parent.parent = None
        
        grandparent.left_child = parent.right_child # parent's right child connet to grandparent's left
        if(parent.right_child!=None):
            parent.right_child.parent = grandparent
        
        parent.right_child = grandparent # parent's right child turn to node's grandparent
        grandparent.parent = node.parent
        
        # Recolor
        parent.color = 'Black'
        parent.right_child.color = 'Red'
        
    def _insert_LR_Rotation(self, node):
        # Rotate
        grandparent = node.parent.parent
        parent = node.parent
        
        grandparent.left_child = node # grandparent's left connent to node
        node.parent = grandparent
        
        parent.right_child = node.left_child # connet node's left child to node's parent
        if(node.left_child!=None):
            node.left_child.parent = parent
        
        node.left_child = parent # connect node's parent to node's left
        parent.parent = node
        
        # LL Rotation
        self._insert_LL_Rotation(node.left_child)
        
    def _insert_RR_Rotation(self, node):
        # Rotate
        grandparent = node.parent.parent
        parent = node.parent
        
        if(grandparent.parent!=None):
            if(grandparent.parent.value < grandparent.value):
                grandparent.parent.right_child = parent # grandparent's parent connect to  node's parent
                parent.parent = grandparent.parent
            elif(grandparent.parent.value > grandparent.value):
                grandparent.parent.left_child = parent
                parent.parent = grandparent.parent
        else:
            self.root = parent
            parent.parent = None
            
        grandparent.right_child = parent.left_child # parent's left child connet to grandparent's left
        if(parent.left_child!=None):
            parent.left_child.parent = grandparent
        
        parent.left_child = grandparent # parent's left child turn to node's grandparent
        grandparent.parent = parent
        
        # Recolor
        parent.color = 'Black'
        parent.left_child.color = 'Red'
    
    def _insert_RL_Rotation(self, node):
        # Rotate
        grandparent = node.parent.parent
        parent = node.parent
        
        grandparent.right_child = node # grandparent's right connent to node
        node.parent = grandparent
        
        parent.left_child = node.right_child # connet node's right child to node's parent
        if(node.right_child!=None):
            node.right_child.parent = parent
        
        node.right_child = parent # connect node's parent to node's left
        parent.parent = node
        
        # RR Rotation
        self._insert_RR_Rotation(node.right_child)
        
    
    """ Delete """
    def delete(self, key):          # delete one node
        print('delete:', key)
        self._delete(self.root, key)
    
    def _delete(self, node, key):
        if(node==None):
            return
        else:
            if(node.value>key):
                self._delete(node.left_child, key)
            elif(node.value<key):
                self._delete(node.right_child, key)
            else:
                # Case 1: node has no child
                if(node.left_child==None and node.right_child==None): 
                    if(node.parent!=None):  # 不是 Node
                        if(node.parent.value<node.value):
                            node.parent.right_child = None
                            self._del_fixnode(self.sibling(node))
                            
                        elif(node.parent.value>node.value):
                            node.parent.left_child = None
                            self._del_fixnode(self.sibling(node))     
                    else:   # 為 Root
                        self.root = None
                        
                # Case2: node with one right child
                elif(node.left_child==None): 
                    if(node.parent!=None):
                        if(node.right_child.value > node.parent.value):
                            node.parent.right_child = node.right_child
                            node.right_child.parent = node.parent
                            if(self._del_simple_case(node, node.right_child)): # 判斷是否為simple case
                                self._del_fixnode(self.sibling(node)) # 不是則 fixnode
                        elif(node.right_child.value < node.parent.value):
                            node.parent.left_child = node.right_child
                            node.right_child.parent = node.parent
                            if(self._del_simple_case(node, node.right_child)):
                                self._del_fixnode(self.sibling(node))
                    else:
                        self.root = node.right_child
                        self.root.color = 'Black'
                
                # Case 3: node with one left child      
                elif(node.right_child==None):
                    if(node.parent!=None):
                        if(node.left_child.value > node.parent.value):
                            node.parent.right_child = node.left_child
                            node.left_child = node.parent
                            if(self._del_simple_case(node, node.left_child)):
                                self._del_fixnode(self.sibling(node))
                        elif(node.left_child.value < node.parent.value):
                            node.parent.left_child = node.left_child
                            node.left_child = node.parent
                            if(self._del_simple_case(node, node.left_child)):
                                self._del_fixnode(self.sibling(node))
                    else:
                        self.root = node.left_child
                        self.root.color= 'Black'
                
                # Case4: node with two child    
                else: 
                    temp = self.findmin_for_del(node.left_child) # 左邊邊子孫 inorder 最大的值
                    self._delete(node.left_child, temp.value) # delete 左邊邊子孫 inorder 最大的值
                    
                    temp.right_child = node.right_child
                    if(node.right_child!=None):
                        node.right_child.parent = temp
                    
                    temp.left_child = node.left_child
                    if(node.left_child!=None):
                        node.left_child.parent = temp
                    
                    if(node.parent!=None):
                        if(temp.value < node.parent.value):
                            node.parent.left_child = temp
                            temp.parent = node.parent
                            
                        elif(temp.value > node.parent.value):
                            node.parent.right_child = temp
                            temp.parent = node.parent
                        else:
                            pass
                    else:
                        self.root = temp
                        self.root.color = 'Black'
    
    def findmin_for_del(self, node): # 若有兩個 children 則找 left subtree 中最大的值
        while(node.right_child != None):
            node = node.right_child
        return node
    
    def sibling(self, node):    # 找旁邊的 Node
        if(node.value < node.parent.value):
            return node.parent.right_child
        elif(node.value > node.parent.value):
            return node.parent.left_child
                        
    def _del_simple_case(self, node, child):
        if(node.color=='Red' or child.color=='Red'):
            child.color = 'Black'
            return False
        else:
            return True
    def _color(self, node): # Node 的color 也為 Black
        if(node==None):
            return 'Black'
        else:
            return node.color
        
    def _del_fixnode(self, node):
        if(node==None): # 若 sibling is None, return
            return
        else:
            # Case 1: Sibling is Black
            if(node.color=='Black'):
                if(self._color(node.left_child)=='Red' or self._color(node.right_child)=='Red'): # at least one child is red
                    if(node.value < node.parent.value and self._color(node.left_child)=='Red'):    # LL Case
                        self._del_LL_Rotation(node)                    
                    elif(node.value < node.parent.value and self._color(node.right_child)=='Red'): # LR Case
                        self._del_LR_Rotation(node) 
                    elif(node.value > node.parent.value and self._color(node.right_child)=='Red'): # RR Case
                        self._del_RR_Rotation(node) 
                    elif(node.value > node.parent.value and self._color(node.left_child)=='Red'):  # RL Case
                        self._del_RL_Rotation(node) 
                    else:
                        pass
                else:   # both children are black
                    node.color = 'Red'    
                    if(node.parent.color=='Red'):
                        node.parent.color = 'Black'
                    elif(node.parent.color=='Black'):
                        sibling = self.sibling(node.parent)
                        self._del_fixnode(sibling)
            
            # Case 2: Sibling is Red
            elif(node.color=='Red'):
                if(node.value < node.parent.value): # Left Case
                    self._del_RightCase(node)
                    self._del_fixnode(node.parent.left_child)
                elif(node.value > node.parent.value): # Right Case
                    self._del_RightCase(node)
                    self._del_fixnode(node.parent.right_child)
    
    def _del_RightCase(self, node):
        grandparent = node.parent.parent
        parent = node.parent
        if(grandparent!=None):
            if(grandparent.value < node.value):
                grandparent.right_child = node
                node.parent = grandparent
                parent.right_child = node.left_child
                node.left_child.parent = parent
                node.left_child = parent
                parent.parent = node
                node.color = 'Black'
                parent.color = 'Red'
            elif(grandparent.value > node.value):
                grandparent.left_child = node
                node.parent = grandparent
                parent.right_child = node.left_child
                node.left_child.parent = parent
                node.left_child = parent
                parent.parent = node
                node.color = 'Black'
                parent.color = 'Red'
            else:
                return
                
    def _del_LeftCase(self, node):
        grandparent = node.parent.parent
        parent = node.parent
        if(grandparent!=None):
            if(grandparent.value < node.value):
                grandparent.right_child = node
                node.parent = grandparent
                parent.left_child = node.right_child
                node.right_child.parent = parent
                node.right_child = parent
                parent.parent = node
                node.color = 'Black'
                parent.color = 'Red'
            elif(grandparent.value > node.value):
                grandparent.left_child = node
                node.parent = grandparent
                parent.left_child = node.right_child
                node.right_child.parent = parent
                node.right_child = parent
                parent.parent = node
                node.color = 'Black'
                parent.color = 'Red'
            else:
                return
                
    def _del_LL_Rotation(self, node):
        parent = node.parent
        grandparent = parent.parent
        if(grandparent!=None):
            if(parent.value < grandparent.value):
                grandparent.left_child = node
                node.parent = grandparent
            elif(parent.value > grandparent.value):
                grandparent.right_child = node
                node.parent = grandparent
        else:
            self.root = node
            node.parent = None
    
        parent.left_child = node.right_child # connect node's left child to parent's right
        if(node.right_child!=None):
            node.right_child.parent = parent
            
        node.right_child = parent # connect parent to node's left
        parent.parent = node
        node.left_child.color = 'Black'
        node.color = parent.color
        
    def _del_LR_Rotation(self, node):
        # Rotate
        parent = node.parent
        parent.left_child = node.right_child # connet node's left child to node's parent
        node.right_child.parent = parent
        
        node.right_child = parent.left_child.left_child
        parent.left_child.left_child.parent = node
        
        parent.left_child.left_child = node
        node.parent = parent.left_child
        
        node.color = 'Red'
        node.parent = 'Black'
        # LR Rotate
        self._del_LL_Rotation(node.parent)
        
    def _del_RR_Rotation(self, node):
        parent = node.parent
        grandparent = parent.parent
        if(grandparent!=None):
            if(parent.value < grandparent.value):
                grandparent.left_child = node
                node.parent = grandparent
            elif(parent.value > grandparent.value):
                grandparent.right_child = node
                node.parent = grandparent
        else:
            self.root = node
            node.parent = None
    
        parent.right_child = node.left_child # connect node's left child to parent's right
        if(node.left_child!=None):
            node.left_child.parent = parent
            
        node.left_child = parent # connect parent to node's left
        parent.parent = node
        
        node.right_child.color = 'Black'
        node.color = parent.color
          
    def _del_RL_Rotation(self, node):
        # Rotate
        parent = node.parent
        parent.right_child = node.left_child # connet node's left child to node's parent
        node.left_child.parent = parent
        
        node.left_child = parent.right_child.right_child
        parent.right_child.right_child.parent = node
        
        parent.right_child.right_child = node
        node.parent = parent.right_child
        
        node.color = 'Red'
        node.parent = 'Black'
        # RR Rotate
        self._del_RR_Rotation(node.parent)
        
    
    def inorder(self, output):      # print the in-order traversal of binary search tree
        # TODO
        self._inorder(self.root, output)
        output.write('\n')
        
    def _inorder(self, node, output):
        if node:
            if(node.left_child!=None):
                self._inorder(node.left_child, output)
            val = node.value
            col = node.color
            output.write(f'{val}:{col} ')
            if(node.right_child!=None):
                self._inorder(node.right_child, output)
    
    def main(self, input_path, output_path):
        output = open(output_path, 'w')
        with open(input_path, 'r', newline='') as file_in:
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("insert"):
                    value_list = lines.split(' ')
                    for value in value_list[1:]:
                        self.insert(int(value))
                if lines.startswith('inorder'):
                    self.inorder(output)
                
                if lines.startswith("search"):
                    value_list = lines.split(' ')
                    for value in value_list[1:]:
                        self.search(int(value), output)
                if lines.startswith('delete'):
                    value_list = lines.split(' ')
                    self.delete(int(value_list[1]))
                    
        output.close()
        
if __name__ == '__main__' :
    #########################
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # It's important and repeat three times
    #########################
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './input_1.txt',help="Input file root.")
    parser.add_argument("--output", type=str, default = './output_1.txt',help="Output file root.")
    args = parser.parse_args()
    
    BRTree = RBTree()
    BRTree.main(args.input, args.output)
            
            
                
        






        