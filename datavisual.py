from typing import Any
from pyecharts.charts import Tree as PT,Graph as PG
from pyecharts import options as opts

from graph import DiGraph
from tree import Tree

class VTree:
    def __init__(self,tree:Tree) -> None:
        self.tree=tree
    def tojson(self,viewf,showid=True):
        def idjson(id):
            adjs=self.tree.get_adj(id)
            return {"name":(str(id) if showid else "")+viewf(self.tree.get_vex(id)),"children":[idjson(adj.i2) for adj in adjs]}
        return idjson(self.tree.root)
    def view(self,viewf=lambda x:str(x),showid=True):
        """render a tree whose node named id-viewf(data) to tree.html"""
        pt = PT()
        pt.add("", [self.tojson(viewf,showid)],is_expand_and_collapse=False,is_roam=True,label_opts = opts.LabelOpts(font_size=8))
        pt.render("tree.html")
class VDiGraph:
    def __init__(self) -> None:
        
        pass
if __name__=="__main__":
    json={

    "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}}}
    }
    t=Tree()
    t.from_dict(json,root="root")
    vt=VTree(t)
    vt.view(viewf=lambda x:str(x)+"?")
    t.show()