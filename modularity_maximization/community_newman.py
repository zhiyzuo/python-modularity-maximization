# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from collections import deque
from modularity_maximization import utils, _divide

def partition(network, refine=True):
    '''
    Cluster a network into several modules
    using modularity maximization by spectral methods.

    Supports directed and undirected networks.
    Edge weights are ignored

    See:

    Newman, M. E. J. (2006). Modularity and community structure in networks.
    Proceedings of the National Academy of Sciences of the United States of America,
    103(23), 8577–82. https://doi.org/10.1073/pnas.0601602103

    Leicht, E. A., & Newman, M. E. J. (2008). Community Structure in Directed Networks.
    Physical Review Letters, 100(11), 118703. https://doi.org/10.1103/PhysRevLett.100.118703

    Parameters
    ----------
    network : nx.Graph or nx.DiGraph
        The network of interest
    refine: Boolean
        Whether refine the `s` vector from the initial clustering
        by repeatedly moving nodes to maximize modularity

    Returns
    -------
    dict
        A dictionary that saves membership.
        Key: node label; Value: community index
    '''
    ## preprocessing
    network = nx.convert_node_labels_to_integers(network, first_label=1, label_attribute="node_name")
    node_name = nx.get_node_attributes(network, 'node_name')

    ## only support unweighted network 
    nx.set_edge_attributes(G=network, name='weight', values={edge:1 for edge in network.edges})

    B = utils.get_base_modularity_matrix(network)

    ## set flags for divisibility of communities
    ## initial community is divisible
    divisible_community = deque([0])

    ## add attributes: all node as one group
    community_dict = {u: 0 for u in network}

    ## overall modularity matrix

    comm_counter = 0

    while len(divisible_community) > 0:
        ## get the first divisible comm index out
        comm_index = divisible_community.popleft()
        g1_nodes, comm_nodes = _divide._divide(network, community_dict, comm_index, B, refine)
        if g1_nodes is None:
            ## indivisible, go to next
            continue
        ## Else divisible, obtain the other group g2
        #### Get the subgraphs (sub-communities)
        g1 = network.subgraph(g1_nodes)
        g2 = network.subgraph(set(comm_nodes).difference(set(g1_nodes)))
        parent = "%d"%comm_index

        ## add g1, g2 to tree and divisible list
        comm_counter += 1
        #community_tree.create_node(comm_counter, "%d" %comm_counter,\
        #                           parent = parent, data = g1_nodes)
        divisible_community.append(comm_counter)
        ## update community
        for u in g1:
            community_dict[u] = comm_counter

        #community_tree.create_node(comm_counter, "%d" %comm_counter,\
        #                          parent = parent, data = list(g2))
        comm_counter += 1
        divisible_community.append(comm_counter)
        ## update community
        for u in g2:
            community_dict[u] = comm_counter

        '''
        print '------'
        community_tree.show()
        partition = []
        for comm_index in set(community_dict.values()):
            print comm_index
            partition.append(set([node_name[i] for i in community_dict if community_dict[i]==comm_index]))
            print sorted(list(partition[-1]))
        print 'Modularity: ', utils.get_modularity(network, community_dict)
        '''

    return {node_name[u]: community_dict[u] for u in network}
