from typing import Any
from pyecharts import charts
from pyecharts import options as opts
from graph import DiGraph
from tree import Tree
class VTree:
    def __init__(self,tree:Tree) -> None:
        self.tree=tree
    def get_view_data(self,viewf=lambda i,data:"{}:{}".format(i,data)):
        """
        获得可视化数据
        - viewf: 节点数据格式化函数 (i,data)->str
        """
        def node_data(i):
            adjs=self.tree.get_adj(i)
            name = viewf(i,self.tree.get_vex(i))
            children = [node_data(e.i2) for e in adjs]
            return {"name":name,"children":children}
        return node_data(self.tree.root)
    def view(self,viewf=lambda i,data:"{}:{}".format(i,data),path = "tree.html"):
        """render a tree whose node named viewf(data)
        - viewf: 节点数据格式化函数 (i,data)->str
        - path: 保存路径
        """
        pt = charts.Tree()
        pt.add(
            "", 
            [self.get_view_data(viewf)],
            is_expand_and_collapse=False,is_roam=True,label_opts = opts.LabelOpts(font_size=8)
        )
        pt.render(path)
class VDiGraph:
    def __init__(self,graph:DiGraph) -> None:
        self.graph=graph
    def get_view_data(self,viewf=(lambda i,data:data)):
        """
        获得可视化数据
        """
        nodes = [{"name":viewf(i,data),"symbolSize": 20 }for i,data in self.graph.eachvex()]
        links = [{"source":viewf(e.i1,self.graph.vexs[e.i1]),"target":viewf(e.i2,self.graph.vexs[e.i2]),"value":e.data} for e in self.graph.eachedge()]
        return {"nodes":nodes,"links":links}
    def view(self,viewf=lambda i,data:"{}:{}".format(i,data),symbol="circle",path="graph.html"):
        """
        可视化
        - viewf:节点显示格式
        - symbol:节点形状
        """
        view_data = self.get_view_data(viewf)
        pg = charts.Graph()
        pg.add(
                "", 
                view_data["nodes"],
                view_data["links"],
                symbol=symbol,
                repulsion=8000,
                linestyle_opts=opts.LineStyleOpts(width=2, curve=0.5, opacity=0.8, type_='solid'),
                edge_symbol = [ 'none', 'arrow' ],
                edge_label=opts.LabelOpts(
                    is_show=True, position="middle",formatter="{c}"
                ),
            )
        pg.render(path)
if __name__=="__main__":
    json={

    "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}}}
    }
    t=Tree()
    t.from_dict(json,root="root")
    vt=VTree(t)
    vt.view(viewf=lambda i,x:"{} {} ??".format(i,str(x)))
    t.show()
    g = DiGraph()
    vexs = {"aaaaaa": "aaaaaaaaaaa\naaaaaaaaaaaaaaaa", "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16}
    edges = [("a", "b", 1), ("a", "c", 2), ("b", "d", 3), ("b", "e", 4), ("c", "f", 5), ("c", "g", 6), ("d", "h", 7), ("d", "i", 8), ("e", "j", 9), ("e", "k", 10), ("f", "l", 11), ("f", "m", 12), ("g", "n", 13)]
    g.add_vexs(vexs.items())
    g.add_edges(edges)
    g.print()
    vg = VDiGraph(g)
    vg.view(symbol="rect")