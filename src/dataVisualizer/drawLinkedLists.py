import matplotlib.pyplot as plt
import networkx as nx
class drawLinkedLists():
    def __init__(self, rootList):
        self.rootList = rootList
        self.G = nx.Graph()
        self.nodeList = []
    def draw(self):
        for root in self.rootList:
            if(root==None or root.next==None):
                continue
            while(root.next!=None):
                self.G.add_edge(str(root.value), str(root.next.value),)
                if(str(root.value) in self.nodeList):
                    return
                else:
                    self.nodeList.append(str(root.value))
                root = root.next
            self.nodeList.append(str(root.value))
        self.edge = [(u,v) for (u,v, d) in self.G.edges(data=True)]
        self.pos = nx.spring_layout(self.G)
        print(self.nodeList)
        nx.draw_networkx_nodes(self.G, self.pos, node_size=1400, nodelist=[self.nodeList[0]], node_color='red')
        nx.draw_networkx_nodes(self.G, self.pos, node_size=700, nodelist=self.nodeList[1:], node_color='red')

        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.edge, width=6)
        nx.draw_networkx_labels(self.G, self.pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        plt.show()

class LLNode():
    def __init__(self, key, data):
        self.value = key
        self.data = data
        self.next = None

if __name__ == '__main__':
    rootNode = LLNode(1, "皮卡丘")
    rootNode.next = LLNode(5, "皮卡丘")
    # rootNode.next.next = LLNode(3, "皮卡丘")

    drawer = drawLinkedList([rootNode])
    drawer.draw()
