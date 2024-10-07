from typing import Any,Iterable,Hashable,TypeVar,Generic
import random
ET = TypeVar("ET")
VT = TypeVar("VT")
class Edge(Generic[ET]):
    def __init__(self,i1:Hashable,i2:Hashable,data: ET=None) -> None:
        self.i1=i1
        self.i2=i2
        self.data:ET =data
    def __hash__(self) -> int:
        """
        parallel edges is not allowed,so if you add a edge between i1,i2 
        while there already exists one,it will be covered.

        Edge's i1-i2 can't be modified
        """
        return (self.i1,self.i2).__hash__()
class DiGraph(Generic[ET, VT]):
    ID = 0
    @staticmethod
    def idmaker(exists:set[Hashable],maxid=int(1e7),continual = True):
        """
        生成唯一id
        - continual:是否连续生成
        - maxid:最大id
        - exists:已经存在的id
        """
        while True:
            if continual:
                i=(DiGraph.ID+1)%maxid
                DiGraph.ID=i
            else :
                i = random.randint(0,maxid)
            if i not in exists:
                return i
        
    def __init__(self,order=False,vexs:list[tuple]=[], edges:list[tuple]=[]):
        """
        - order:邻接表是否有序
        - vexs:顶点列表
        - edges:边列表
        """
        self.order=order
        self.init_order()
        self.vexs:dict[Hashable, VT]={}    #vertex
        self.adjs:dict[Hashable,(set|list)[Edge[ET]]]={} #adjacent edges
        self.add_vexs(vexs)
        self.add_edges(edges)
    def init_order(self):
        if self.order==False: #无序
            self.onorder={
                "adjtype":set,
                "add":set.add,
                "remove":lambda s,x: s.remove(x) if x in s else None,
                "insert":lambda l,i,x : set.add(l,x)
            }
        else:#有序
            self.onorder={
                "adjtype":list,
                "add":list.append,
                "remove":lambda l,x: l.remove(x) if x in l else None,
                "insert":lambda l,i,x : list.insert(l,i,x)
            }
    def set_vex(self,i,data):
        self.vexs[i]=data 
    def insert_edge(self,i1,i2,n,data=None):
        """
        insert an edge to gragh in specified adj position,the vertex should exist
        - i1:from vertex id
        - i2:to vertex id
        - n : n-th adjacent postion
        - data:data of edge
        """
        assert self.order==True
        self.onorder["insert"](self.adjs[i1],n,Edge(i1,i2,data))
    def add_vex(self,i,data=None):
        """
        if vertex already exists this function will do nothing
        """
        if i in self.vexs:return
        self.vexs[i]=data
        self.adjs[i]=self.onorder["adjtype"]()
    def remove_vex(self,i):
        """
        remove vertex and all edges connected to it,nothing will happen if vertex doesn't exist
        - i:vertex id
        """
        edges = []
        for e in self.eachedge():
            if e.i1==i or e.i2==i:
                edges.append((e.i1,e.i2))
        for i1,i2 in edges:
            self.remove_edge(i1,i2)
        if i in self.vexs:
            self.vexs.pop(i) 
    def remove_edge(self,i1,i2):
        """
        remove an edge from i1 to i2,nothing will happen if edge doesn't exist
        - i1:from vertex id
        - i2:to vertex id
        """
        for e in self.adjs[i1]:
            if i2 == e.i2:
                self.onorder["remove"](self.adjs[i1],e)
                return
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
    def add_graph(self,graph):
        """
        合并两个图，返回节点对应关系,顺序保持
        - graph:DiGraph
        # return
        - mapper : dict[graphid:selfid]
        """
        graph:DiGraph =graph
        mapper = {}
        for i,data in graph.eachvex():
            mapper[i] = self.add_nameless_vex(data=data)
        for e in graph.eachedge():
            self.add_edge(mapper[e.i1],mapper[e.i2],e.data)
        return mapper

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
        iterate all edges in order
        # returns
        - edge:Edge
        """
        for i in self.vexs:
            for edge in self.adjs[i]:
                yield edge
    def eachpair(self):
        """
        iterate all connected nodes in order
        # returns
        - data1:data of vertex1
        - data2:data of vertex2
        - data:data of edge
        """
        for edge in self.eachedge():
            yield (self.get_vex(edge.i1),self.get_vex(edge.i2),edge.data)
    def eachvex(self):
        """
        iterate all vertexs
        # returns
        - id:id of vertex
        - data:data of vertex
        """
        for i in self.vexs:
            yield (i,self.get_vex(i))
    def print(self):
        """
        print info of graph in the console,including vertexs and edges
        """
        for i,data in self.eachvex():
            print(i,':',data)
        for e in self.eachedge():
            print(e.i1,'--',e.data,'-->',e.i2)

def test_basic():
    """
    测试 创建图,添加顶点,添加边，打印图，删除点，删除边
    """
    graph=DiGraph(order=True)
    graph.add_nameless_vexs(({1},{2},{3},{4}))
    graph.add_vex(9,{9})
    graph.add_edge(2,3,5)
    graph.add_edge(3,4)
    graph.add_edges([(2,4,6),(1,4,5),(1,2,7)])
    graph.add_nameless_vexs([{5},{6}])
    print("before delete")
    graph.print()
    print("after delete")
    graph.remove_vex(2)
    graph.remove_edge(3,4)
    graph.print()
def test_iter():
    """
    测试 遍历
    """
    graph = DiGraph(order=True,vexs=[[1,2],[2,3],[3,8],[4,5]],edges=[[1,2,3],[2,3,4],[3,1,9],[4,1,0],[4,2,1]])
    print("eachpair:")
    for d1,d2,de in graph.eachpair():
        print(d1,d2,de)
    print("eachvex:")
    for i,data in graph.eachvex():
        print(i,data)
    print("eachedge:")
    for e in graph.eachedge():
        print(e.i1,e.i2,e.data)
    

def test_add_graph():
    graph = DiGraph[int,int](order=True,vexs=[[1,2],[2,3],[3,8],[4,5]],edges=[[1,2,3],[2,3,4],[3,1,9],[4,1,0],[4,2,1]])
    graph2 = DiGraph(order=True,vexs=[[1,2],[2,3],[3,8],[4,5]],edges=[[1,2,3],[2,3,4]])

    print("graph1: ")
    graph.print()
    print("graph2: ")
    graph2.print()
    mapper = graph.add_graph(graph2)
    print("union: ")
    graph.print()
    print("mapper: ")
    print(mapper)

if __name__=="__main__":

    #test_basic()
    test_iter()