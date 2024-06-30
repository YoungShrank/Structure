# Structure
data structure modules with exhaustive explanations

# modules

## graph.py
> graph data structure,composed of nodes and edges,each node or edge has a value. no parallel edges in a graph.
1. **Digraph**  
   DirectedGraph in which each edge has a direction,so the adjacent relationship is not symmetric.
## tree.py
1. **Tree**  
   a subclass of graph,each node has at most one parent node who has an edge to this node.only an constructor to the Tree class is provided.
## btree.py
> binary tree data structure,each node has at most two children nodes.not based on graph or tree.
1. **btree**  
provides functions such as travel,transverse,construction,etc.
1. **sorttree**  
based on btree,maintains sorted datas,provides functions such as add,delete,search,etc.the time complexity of each function is O(logn)
## datavisual
visualization of tree

# requirements
|dependency| function|
|:---:|:---:|
|pyecharts| data visualization
