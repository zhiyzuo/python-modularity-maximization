---
layout: page
title: "Quick Start"
category: doc
date: 2017-04-14
---

The following two examples use data in the both cited papers mentioned in the index page.

#### Undirected Network: Karate


```python
import networkx as nx
karate = nx.Graph(nx.read_pajek("data/karate.net"))
print(nx.info(karate))
```

<pre><code>Name: 
Type: Graph
Number of nodes: 34
Number of edges: 78
Average degree:   4.5882
</code></pre>


```python
from modularity_maximization import partition
comm_dict = partition(karate)
for comm in set(comm_dict.values()):
    print("Community %d"%comm)
    print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))
```

<pre><code>Community 3
5, 7, 6, 11, 17
Community 4
20, 22, 1, 3, 2, 4, 8, 10, 13, 12, 14, 18
Community 5
27, 21, 23, 9, 15, 16, 19, 31, 30, 34, 33
Community 6
24, 25, 26, 28, 29, 32
</code></pre>


```python
from modularity_maximization.utils import get_modularity
print('Modularity of such partition for karate is %.3f' % get_modularity(karate, comm_dict))
```

<pre><code>Modularity of such partition for karate is 0.419</code></pre>


#### Directed Network: Big 10 Football Season 2005


```python
big_10_football = nx.read_gml("data/big_10_football_directed.gml")
print(nx.info(big_10_football))
```

<pre><code>Name: 
Type: DiGraph
Number of nodes: 11
Number of edges: 44
Average in degree:   4.0000
Average out degree:   4.0000
</code></pre>


```python
comm_dict = partition(big_10_football)
for comm in set(comm_dict.values()):
    print("Community %d"%comm)
    print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))
```

<pre><code>Community 1
OhioState, Northwestern, Wisconsin, Iowa, PennState, Michigan, Minnesota
Community 2
Purdue, Illinois, MichiganState, Indiana
</code></pre>


```python
print('Modularity of such partition for karate is %.3f' %\
      get_modularity(big_10_football, comm_dict))
```

<pre><code>Modularity of such partition for karate is 0.112</code></pre>


