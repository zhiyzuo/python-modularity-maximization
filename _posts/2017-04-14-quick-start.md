---
layout: page
title: "Quick Start"
category: doc
date: 2017-04-14
---

The following two examples use data in the both cited papers mentioned in the index page.

```python
import networkx as nx
nx.__version__
```
<pre><code>'2.0'</code></pre>


```python
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity
```

#### Undirected Network 
##### Karate


```python
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


##### Jazz Network

```python
jazz = nx.Graph(nx.read_pajek("data/jazz.net"))
print(nx.info(jazz))
```
<pre><code>Name:
Type: Graph
Number of nodes: 198
Number of edges: 2742
Average degree:  27.6970
</code></pre>


```python
comm_dict = partition(jazz)
for comm in set(comm_dict.values()):
    print("Community %d"%comm)
    print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))
```

<pre><code>Community 3
    130, 127, 129, 69, 55, 54, 57, 56, 53, 52, 195, 194, 197, 67, 192, 114, 89, 113, 112, 83, 7, 103, 31, 30, 36, 34, 61, 178, 174, 186, 196, 185, 164, 165, 161, 11, 10, 12, 14, 19, 151, 150, 158, 49, 87, 142, 141, 74, 72, 71, 70, 2
    Community 4
    133, 136, 138, 25, 26, 27, 21, 28, 29, 4, 96, 124, 126, 128, 51, 90, 198, 191, 115, 88, 85, 3, 92, 102, 39, 37, 176, 173, 172, 180, 181, 184, 6, 189, 97, 169, 167, 160, 163, 13, 18, 153, 152, 155, 157, 156, 86, 45, 5, 147, 144, 145, 140, 148, 149, 77, 76, 75, 73, 79, 41, 47
    Community 5
    132, 131, 135, 134, 139, 24, 20, 22, 23, 95, 8, 120, 122, 123, 91, 58, 50, 110, 80, 81, 119, 108, 109, 100, 101, 106, 107, 104, 105, 38, 33, 32, 35, 60, 62, 63, 64, 65, 66, 68, 171, 170, 182, 187, 188, 179, 99, 98, 168, 166, 162, 15, 17, 16, 154, 159, 48, 46, 44, 42, 43, 40, 1, 78
    Community 6
    137, 93, 94, 121, 125, 59, 190, 193, 111, 82, 118, 84, 177, 175, 183, 117, 116, 9, 146, 143
</code></pre>

```python
print('Modularity of such partition for jazz is %.3f' % get_modularity(jazz, comm_dict))
```

<pre><code>
    Calculating modularity for undirected graph
    Modularity of such partition for karate is 0.442
</code></pre>

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

<pre><code>Calculating modularity for directed graph
Modularity of such partition for karate is 0.112
</code></pre>


