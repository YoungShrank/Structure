from graph import DiGraph
from typing import Hashable
class Tree(DiGraph):
    def __init__(self,order=True):
        """
        - order:ordered tree  
        """
        super().__init__(order)
        self.parents:dict[Hashable,Hashable] = {}# {child:parent,...}
    def init_parents(self):
        """
        初始化parents,除了root的parents为None，其他有1个父节点
        """
        self.parents = {}
        self.parents.setdefault(self.root,None)
        for e in self.eachedge():
            self.parents[e.i2]=e.i1
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
        self.init_parents()
    def from_tree(self,t):
        """
        init tree with tree(or copy construction)
        - t:tree
        """
        t:Tree = t
        self.onorder = t.onorder
        self.order = t.order
        self.adjs = t.adjs
        self.vexs = t.vexs
        self.parents = t.parents
        self.root = t.root
    
    def iter(self,order = "pre"):
        """
        iter tree with order
        - order:order of iter, [pre,post]
        # returns
        [(id,data)]
        """
        return self.iter_sub(self.root, order=order)
    def iter_layer(self):
        """
        iter tree layer by layer
        # returns
        [[(id,data)]]
        """
        if self.root:
            first = [(self.root,self.get_vex(self.root))]
            yield first
            while True:
                next = []
                for i,data in first:
                    next.extend([(e.i2,self.get_vex(e.i2)) for e in self.get_adj(i)])
                if len(next)==0:
                    break
                else :
                    yield next
                    first = next
    def get_leaf(self, n:int):
        """
        get the n-the leaf node
        - n : the n-th leaf node
        # return 
        (id,data)
        """
        leafs = [(i,d) for i,d in self.iter_leafs()]
        assert n<=len(leafs)
        return leafs[n-1]
    def get_child(self,i,n):
        """
        get n-th child of node 
        - i :id of the node
        - n :n-th child
        # return 
        (id,data)
        """
        subs=self.get_adj(i)
        assert n<=len(subs)
        j = subs[n-1].i2
        return j,self.get_vex(j)
    def get_childs(self,i):
        """
        get all children of node 
        - i :id of the node
        # return 
        [(id,data)]
        """
        subs = self.get_adj(i)
        return [(e.i2,self.get_vex(e.i2)) for e in subs]

            
    def iter_leafs(self):
        """
        iter leaf node
        # returns
        (id,data)
        """
        def iter_node(i):
            subs=self.get_adj(i)
            if len(subs)==0:
                yield i,self.get_vex(i)
            else:
                for sub in subs:
                    yield from iter_node(sub.i2)
        return iter_node(self.root)
    def iter_ancestor(self,i):
        """
        iter ancestors
        - i :id of the begin node
        # returns
        (id,data)
        """
        while i is not None:
            yield i,self.get_vex(i)
            i = self.parents[i]
    def iter_sub(self,i,order = "pre"):
        """
        iter subtree in order
        - i: id of root  of the subtree
        - order:order of iter, [pre,post]
        """
        assert order in ["pre","post"]
        def iter_node(n):
            subs=self.get_adj(n)
            if order=="pre":
                yield n,self.get_vex(n)
            for sub in subs:
                yield from iter_node(sub.i2)
            if order=="post":
                yield n,self.get_vex(n)
        return iter_node(i)
    def get_subtree(self,i):
        """
        获得子树
        - i:id of the root of subtree
        """
        t = Tree(order=self.order)#不便于继承
        for j,d in self.iter_sub(i,order="pre"):
            t.add_vex(j,d)
        t.root = i
        for j,d in self.iter_sub(i,order="pre"):
            if j!=i:
                t.add_edge(self.parents[j],j)
        t.init_parents()
        return t
    def copy_subtree(self, i, data_copy = lambda x:x):
        """
        copy subtree
        - i:id of the root of subtree
        - data_copy:function to copy data
        # return
        Tree
        """
        t = Tree(order=self.order)
        for j,d in self.iter_sub(i,order="pre"):
            t.add_vex(j,data_copy(d))
        t.root = i
        for j,d in self.iter_sub(i,order="pre"):
            if j!=i:
                t.add_edge(self.parents[j],j)
        t.init_parents()
        return t
    def common_ancestors(self,ids:list[Hashable]):
        """
        get common ancestors of nodes, arranged from leaf to root
        - ids:ids of nodes
        # return
        - ancestors :list, ids of common ancestor down-to-up
        """
        i0 = ids[0]
        ancestors0 = [i for i,d in self.iter_ancestor(i0)]
        left_ancestors = set(ancestors0).intersection(
            *[{j for j, _ in self.iter_ancestor(ids[k])} for k in range(1, len(ids))]
        )
        while True:
            if ancestors0[0] in left_ancestors:
                return ancestors0
            else :
                ancestors0.pop(0)


    def remove_sub(self, i):
        """
        remove subtree, the result can be a empty tree
        - i:id of the root of subtree
        """
        if self.root==i: # i is root
            self.root = None
            return
        for i,d in list(self.iter_sub(i,order="post")):#正在迭代不能修改generator 所以用list
            #因为知道入节点(即父节点)，可以直接删除，不用Graph的删除顶点方法
            parent = self.parents[i]
            self.parents.pop(i)
            self.vexs.pop(i)
            self.adjs.pop(i)
            self.remove_edge(parent,i)
    def substitute(self,i,t):
        """
        substitute node with tree, the i can be root, and t can be a empty tree
        - i:id of the node
        - t:tree
        # returns 
        - j : the root of the t in this tree
        """
        t:Tree = t
        j = t.root
        p= self.parents[i]
        if p:
            n = [pos for pos,e in  enumerate (self.get_adj(p)) if e.i2==i][0]#位置
        self.remove_sub(i)#删除i节点及其子树
        if t.root is not None:#非空树
            mapper = self.add_graph(t)#添加树
            if p:
                self.insert_edge(p,mapper[j],n)
            else :
                self.root = mapper[j]
        self.init_parents()
        return mapper[j]

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
        assert root in self.vexs
        self.root=root

def test_construct_iter():
    """
    测试 构造,迭代,打印
    """
    json = {
        "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}},"c":{"ca":1,"cb":1}}
    }
    t = Tree(order=True)
    t2 = Tree(order=True)
    t.from_dict(json,root="root")
    t.set_vex("cb",data="1")
    t.set_vex("bc",data="6")
    print("【t1 show】")
    t.show()
    t2.from_tree(t)
    print("【t2 show】")
    t2.show()
    print("【iter_layer】")
    for layer in t.iter_layer():
        print(layer)
    print("【iter_leaf】")
    for i,d in t.iter_leafs():
        print(i,d)
    print("【post order】")
    for i,d in t.iter(order="post"):
        print(i,d)
    print("【pre order】")
    for i,d in t.iter(order="pre"):
        print(i,d)
    print("【iter ancestor】")
    for i,d in t.iter_ancestor("cb"):
        print(i,d)

def test_sub():
    """
    测试 获得子树，替换子树，移除子树，获得孩子
    """
    json = {
        "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}},"c":{"ca":1,"cb":1}}
    }
    t = Tree(order=True)
    t2 = Tree(order=True)
    t.from_dict(json,root="root")
    print("【t:from_dict】")
    t.show()
    print("【t:parents】")
    print(t.parents)
    t2.from_dict(json,root="root")
    t2.remove_sub("b")
    print("t2 afer remove b")
    t2.show()
    print("t2 = get g")
    t2 = t2.get_subtree("g")
    t2.show()
    print("t replace b by t2")
    j = t.substitute("b",t2)
    print(" new root", j)
    t.show()
    print(t.get_childs(4))
def test_copy():
    """
    测试 拷贝子树
    """

    t = Tree(order=True)
    t.set_root("root")
    t.add_vexs([("root",[1]),("a",[2]),("b",[3]),("c",[4])])
    t.add_edges([("root","a"),("root","b"),("a","c")])
    t.init_parents()
    t2 = t.get_subtree("root")
    t3 = t.copy_subtree("root",data_copy=lambda x:x.copy())
    t.get_vex("root").append(5)
    print("********  t *********")
    t.print()
    print(list(t.vexs))
    print("********  t2 *********")
    t2.print()
    print(list(t2.vexs))
    print("********  t3 *********")
    t3.print()
    print(list(t3.vexs))
def test_common_ancestors():
    """
    测试 获得公共祖先
    """
    json = {
        "g":{"a":{"ac":6},"b":{"ba":{"bc":6,"abc":6,"bfc":6,"bcf":6}},"c":{"ca":1,"cb":1}}
    }
    t = Tree(order=True)
    t.from_dict(json,root="root")
    t.show()
    print(t.common_ancestors(["bfc","ba"]))



if __name__=="__main__":
    test_copy()

 
