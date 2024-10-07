from tree import Tree
from typing import Generic, Hashable, TypeVar
VT = TypeVar("VT")
ET = TypeVar("ET")
class BTNode(Generic[VT]):
    lrp=(0,1,-1)
    def __init__(self,data=None,lc=None,rc=None,pr=None):
        """
        - data: the data of the node
        - lc: the left child of the node
        - rc: the right child of the node
        - pr: the parent of the node
        """
        self.data:VT = data
        self.lc=lc
        self.rc=rc
        self.pr=pr
    def __eq__(self, __o: object) -> bool:
        """
        return true if the data of the node is equal to the data of the other node
        """
        if(not isinstance(__o,BTNode)):return False
        return __o.data==self.data

    def onestep(self,direct:int):
        """return the node after one step in direct
        - direct : 0 for left, 1 for right, -1 for parent
        # returns 
        - node
        """
        assert direct in self.lrp
        return (self.lc,self.rc,self.pr)[self.lrp.index(direct)]
    def goto(self,path:list[tuple]):
        """return the node after taveling in path or the last node if meet none
        - path : [[direction,times]],negative times means keep going
        # returns 
        - node
        """
        pos=self
        for direct,times in path:
            i=0
            while(i!=times):
                next=self.onestep(direct)
                if(next is None):break
                pos=next
                i+=1
        return pos
class BTree(Generic[VT]):
    def __init__(self,json:dict=None,root=None):
        """
        根据json生成树，或者直接传入root
        - json : the json of the tree
        {
        "data":data,
        "lc":json of the left child,
        "rc":json of the right child
        }
        - node : the root of the tree
        """
        if root is not None:
            self.root=root
            return
        def mktree(json:dict,parent=None):
            if(json is None):return None
            root=BTNode[VT](data=json.get("data"))
            root.lc=mktree(json=json.get("lc"),parent=root)
            root.rc=mktree(json=json.get("rc"),parent=root)
            root.pr=parent
            return root
        self.root=mktree(json=json)
    def print(self):
        """
        use retraction to show the tree
        """
        print("-"*15,"Tree","-"*15)
        def puttree(node:BTNode[VT],deep):
            if node is None: return
            print(" "*4*deep,"@",node.data)
            puttree(node.lc,deep+1)
            puttree(node.rc,deep+1)
        puttree(self.root,0)
        print("-"*15,"Tree","-"*15)
        return
    def goto(self,path:list[tuple]):
        """
        return the node after taveling in path or the last node if meet none
        - path : [[direction,times]],negative times means keep going
        # returns 
        - node
        """
        return self.root.goto(path)
    def deep(self):
        """
        return the tree depth
        """
        def treedeep(node:BTNode[VT]):
            if node is None:return 0
            return max(treedeep(node.lc),treedeep(node.rc))+1
        return treedeep(self.root)
    
    def tlist(self,order="mid"):
        """
        return a list containing the tree's datas 

        order:the order to traverse the tree
        - "mid" : middle order
        - "pre" : pre order
        - "post" : post order
        # returns
        - list of datas
        """
        lst=[]
        order={"mid":(1,0,2),"pre":(0,1,2),"post":(1,2,0)}[order]
        def addlist(node:BTNode[VT]):
            if node is None: return
            actions=[lambda :lst.append(node.data),lambda :addlist(node.lc),lambda:addlist(node.rc)]
            for i in order:
                actions[i]()
        addlist(self.root)
        return lst
    def toTree(self)->Tree:
        """
        convert the btree to a tree object
        """
        tree=Tree()
        def mktree(node:BTNode[VT]):
            if node is None :return None
            root=tree.add_nameless_vex(node.data)
            lc,rc=mktree(node.lc),mktree(node.rc)
            if lc is not None:tree.add_edge(root,lc)
            if rc is not None:tree.add_edge(root,rc)
            return root
        tree.set_root(mktree(self.root))
        return tree
    @staticmethod
    def compare(tree1,tree2):
        """
        return true if the two trees are equal
        """
        def comptree(node1:BTNode,node2:BTNode):
            if node1 is None or node2 is None :
                return node1 is None and node2 is None
            else: 
                return node1.data==node2.data and comptree(node1.lc,node2.lc) and comptree(node1.rc,node2.rc)
        return comptree(tree1.root,tree2.root)
    @staticmethod
    def combine(tree1,tree2,data=None):
        """
        return a new tree which is the combination of two trees
        - tree1 : the left tree
        - tree2 : the right tree
        - data : the data of the root of the new tree
        """
        node=BTNode[VT](data,tree1.root,tree2.root)
        return BTree[VT](root=node)
class SortTree(BTree):
    def __init__(self, json=None, root:BTNode=None,cmp=(lambda x,y:x<y),equ=(lambda x,y:x==y)):
        """
        二叉排序树
        - json : the json of the tree
        - root : the root of the tree
        - cmp : the compare function
        - equ : the equal function
        """
        super().__init__(json,root)
        self.cmp=cmp
        self.equ=equ
    def fmin(self)->BTNode:
        """
        return the min node in the tree
        """
        l,r,p=BTNode.lrp
        return self.root.goto([(l,-1)])
    def fmax(self):
        """
        return the max node in the tree
        """
        l,r,p=BTNode.lrp
        return self.root.goto([(r,-1)])
    def del_node(self,node:BTNode):
        """
        delete the node from the tree
        - node : the node to delete
        """
        pr=node.pr
        p=None#合成子树的树根    
        if(node.lc is None): p=node.rc
        elif(node.rc is None):p=node.lc
        else:
            m=SortTree(node=node.rc).fmin()#右边最小的节点
            m.lc=node.lc
            node.lc.pr=m
            p=node.rc
        #与父节点
        if(pr is None):self.root=p
        elif(pr.lc is node):
            pr.lc=p
            if p:p.pr=pr
        else:
            pr.rc=p
            if p:p.pr=pr
    def add_node(self,node):
        """
        add a node to the tree
        - node : the node to add
        """
        if(self.root is None):self.root=node;return
        pos=self.root
        while(True):
            if (self.cmp(node.data,pos.data)):
                if(pos.lc is not None):pos=pos.lc
                else :pos.lc=node;node.pr=pos;return
            else: 
                if(pos.rc is not None):pos=pos.rc
                else :pos.rc=node;node.pr=pos;return
    def add_data(self,data):
        """
        add a node to the tree
        - data : the data to add
        """
        self.add_node(BTNode(data=data))
    def del_data(self,data):
        """
        delete a node with data
        - data : the data to delete
        """
        pos=self.root
        while(pos):
            if self.equ(pos.data,data) :self.del_node(pos);return 
            elif (self.cmp(pos.data,data)):
                pos=pos.rc
            else: 
                pos=pos.lc
    def find(self,data,rel="="):
        """
        find a node with relation to data which indicated by rel
        rel:
            >:inferium of prior
            <:superium of inferior
            =:equal
        """
        pos=self.root
        lpos=None
        gpos=None
        while(pos):
            if self.equ(pos.data,data) and '='in rel:return pos
            elif (self.cmp(pos.data,data)):
                lpos=pos
                if pos.rc is None :break
                else :pos=pos.rc
            else: 
                gpos=pos
                if pos.lc is None: break
                else :pos=pos.lc
        if( '>' in rel ):return gpos
        elif( '<' in rel ):return lpos
        return None
    def find_data(self,data,rel):
        """
        find a node's data with relation to data which indicated by rel
        rel:
            >:inferium of prior
            <:superium of inferior
            =:equal
        """
        node=self.find(data=data,rel=rel)
        if(node):return node.data
        else :return None
if __name__=="__main__":
    json={
        "data":1,
        "lc":{
            "lc":{},
            "rc":{

            }
            },
        "rc":{

            }
    }
    from random import Random
    t=SortTree()
    for i in Random.choices(Random(),k=100,population=range(1000)):
        t.add_data(i)
    res=t.find_data(54,rel=">")
    tree=BTree.combine(t,t).toTree()
    tree.show()
    from datavisual import VTree
    print(BTree.compare(t,BTree.combine(t,t)))
    VTree(tree).view(showid=False)
    print(res,BTree.combine(t,t,1000).tlist())