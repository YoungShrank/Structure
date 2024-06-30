from graph import DiGraph
class Tree(DiGraph):
    def __init__(self,order=True):
        """
        - order:ordered tree  
        """
        super().__init__(order)
    def from_dict(self,dic:dict,root=None):
        """
        init tree with dict
        - dic:{id:subtree|None,...}
        - root:root id
        """
        self.root=root
        def mktree(key,val):
            self.add_vex(key)
            if isinstance(val,dict):
                for ckey,cval in val.items():
                    mktree(ckey,cval)
                    self.add_edge(key,ckey)
        mktree(self.root,dic)

    def show(self):
        """
        show tree in console with indent
        """
        def show_(id,deep):
            print(" "*deep,"@",id)
            subs=self.get_adj(id)
            for sub in subs:
                show_(sub.i2,deep+4)
        if self.root is not None:
            show_(self.root,0)
    def set_root(self,root):
        self.root=root
if __name__=="__main__":
    json={
    "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}}}
    }
    t=Tree()
    t.from_dict(json,root="root")
    t.show()
