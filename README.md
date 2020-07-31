### Spanning Tree Covering with path (STC)

The code is a snippet of the work done in the paper 
https://link.springer.com/chapter/10.1007/978-981-13-9419-5_3

The following code requires networkx and matplotlib libraries.

1) install matplotlib 
	```sh pip install matplotlib```
2) install networkx
	```sh pip install networkx```

This Spanning tree covering(STC) algorithm is used to cover a given workspace with the least possible distance.

The code creates a minimal spanning tree(represented in red in the visual plot) around the free nodes and a path(green) along the tree  which the robot has  to follow to cover the complete workspace.

The code assumes that the workspace is a square.Hence,the number of nodes in the workspace that needs to be a perfect square.

The nodes are numbered from 0.
