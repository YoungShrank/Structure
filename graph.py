from typing import Any,Iterable,Hashable
import random
class Edge:
    def __init__(self,i1:Hashable,i2:Hashable,data=None) -> None:
        self.i1=i1
        self.i2=i2
        self.data=data
    def __hash__(self) -> int:
        """
        parallel edges is not allowed,so if you add a edge between i1,i2 
        while there already exists one,it will be covered.

        Edge's i1-i2 can't be modified
        """
        return (self.i1,self.i2).__hash__()
class DiGraph:
    ID = 0
    @staticmethod
    def idmaker(exists:set[Hashable],maxid=int(1e6),continual = True):
        """
        生成唯一id
        - continual:是否连续生成
        - maxid:最大id
        - exists:已经存在的id
        """
        while True:
            if continual:
                i=(DiGraph.ID+1)%maxid
            else :
                i = random.randint(0,maxid)
            if i not in exists:
                DiGraph.ID=i
                return i
        
    def __init__(self,order=False,vexs:list[tuple]=[], edges:list[tuple]=[]):
        self.order=order
        self.init_order()
        self.vexs={}    #vertex
        self.adjs:dict[Hashable,(set|list)[Edge]]={} #adjacent edges
        self.add_vexs(vexs)
        self.add_edges(edges)
    def init_order(self):
        if self.order==False:
            self.onorder={
                "adjtype":set,
                "add":set.add
            }
        else:
            self.onorder={
                "adjtype":list,
                "add":list.append
            }
    def set_vex(self,i,data):
        self.vexs[i]=data 
    def add_vex(self,i,data=None):
        """
        if vertex already exists this function will do nothing
        """
        if i in self.vexs:return
        self.vexs[i]=data
        self.adjs[i]=self.onorder["adjtype"]()
    def add_nameless_vex(self,data=None):
        """
        add a nameless vertex and return its id
        """
        i = DiGraph.idmaker(self.vexs.keys())
        self.add_vex(i, data)
        return i
    def add_nameless_vexs(self,datas:Iterable=[]):
        """
        add nameless vertexs and return their ids
        """
        return [self.add_nameless_vex(data) for data in datas]
    def add_vexs(self,pairs:list):
        """
        add vertexs
        - pairs:list[tuple[id,data]]
        """
        for pair in pairs:
            self.add_vex(*pair)
    def get_vex(self,i):
        """
        get data of vertex
        """
        return self.vexs[i]
    def get_adj(self,i):
        """
        get adjacent edges of vertex
        """
        return self.adjs[i]
    def add_edge(self,i1,i2,data=None):
        """
        add an edge to gragh,add nodes first if they don't exist
        """
        self.add_vex(i1)
        self.add_vex(i2)
        self.onorder["add"](self.adjs[i1],Edge(i1,i2,data))
    def add_edges(self,edges:list[tuple]=[]):
        """
        add edges to vertex
        - edges:list[tuple[i1,i2,data]]
        """ 
        for edge in edges:
            self.add_edge(*edge)
    def add_adjs(self,i,pairs:list[tuple]=[]):
        """
        add edges to vertex
        - i:id of vertex
        - pairs:list[tuple[i2,data]]
        """
        for pair in pairs:
            self.add_edge(i,*pair)

    def eachedge(self):
        """
        iterate all edges 
        #returns
        - edge:Edge
        """
        for i in self.vexs:
            for edge in self.adjs[i]:
                yield edge
    def eachpair(self):
        """
        iterate all ajacent nodes
        #returns
        - data1:data of vertex1
        - data2:data of vertex2
        - data:data of edge
        """
        for edge in self.eachedge():
            yield (self.get_vex(edge.i1),self.get_vex(edge.i2),edge.data)
    def eachvex(self):
        """
        iterate all vertexs
        #returns
        - id:id of vertex
        - data:data of vertex
        """
        for i in self.vexs:
            yield (i,self.get_vex(i))
    def print(self):
        for i,data in self.eachvex():
            print(i,':',data)
        for e in self.eachedge():
            print(e.i1,'--',e.data,'-->',e.i2)
    

if __name__=="__main__":

    graph=DiGraph(order=True)
    ##graph.add_vexs([[1,{2}],[2,{3}],[3,{6}]])
    graph.add_nameless_vexs(({1},{2},{3},{4}))
    graph.add_adjs(1,[(1,2),(2,4),(3,4)])
    graph.add_edge(2,3,9)
    graph.add_edge(0,4,9)
    graph.add_nameless_vexs(({5},{6},{7},{8}))
    graph.print()
    print()