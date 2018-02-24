# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from scipy import sparse
from modularity_maximization import utils

def _divide(network, community_dict, comm_index, B, refine=False):
    '''
    Bisection of a community in `network`.

    Parameters
    ----------
    network : nx.Graph or nx.DiGraph
        The network of interest

    Returns
    -------
    tuple
        If the given community is indivisible, return (None, None)
        If the given community is divisible, return a tuple where
        the 1st element is a node list for the 1st sub-group and
        the 2nd element is a node list for the original group
    '''

    comm_nodes = tuple(u for u in community_dict \
                  if community_dict[u] == comm_index)
    B_hat_g = utils.get_mod_matrix(network, comm_nodes, B)

    # compute the top eigenvector u₁ and β₁
    if B_hat_g.shape[0] < 3:
        beta_s, u_s = utils.largest_eig(B_hat_g)
    else:
        beta_s, u_s = sparse.linalg.eigs(B_hat_g, k=1, which='LR')
    u_1 = u_s[:, 0]
    beta_1 = beta_s[0]
    if beta_1 > 0:
        # divisible
        s = sparse.csc_matrix(np.asmatrix([[1 if u_1_i > 0 else -1] for u_1_i in u_1]))
        if refine:
            improve_modularity(network, comm_nodes, s, B)
        delta_modularity = utils._get_delta_Q(B_hat_g, s)
        if delta_modularity > 0:
            g1_nodes = np.array([comm_nodes[i] \
                                 for i in range(u_1.shape[0]) \
                                 if s[i,0] > 0])
            #g1 = nx.subgraph(g, g1_nodes)
            if len(g1_nodes) == len(comm_nodes) or len(g1_nodes) == 0:
                # indivisble, return None
                return None, None
            # divisible, return node list for one of the groups
            return g1_nodes, comm_nodes
    # indivisble, return None
    return None, None

def improve_modularity(network, comm_nodes, s, B):
    '''
    Fine tuning of the initial division from `_divide`
    Modify `s` inplace

    Parameters
    ----------
    network : nx.Graph or nx.DiGraph
        The network of interest
    comm_nodes: iterable
        List of nodes for the original group
    s: np.matrix
        A matrix of node membership. Only +1/-1
    B: np.amtrix
        Modularity matrix for `network`
    '''

    # iterate until no increment of Q
    B_hat_g = utils.get_mod_matrix(network, comm_nodes, B)
    while True:
        unmoved = list(comm_nodes)
        # node indices to be moved
        node_indices = np.array([], dtype=int)
        # cumulative improvement after moving
        node_improvement = np.array([], dtype=float)
        # keep moving until none left
        while len(unmoved) > 0:
            # init Q
            Q0 = utils._get_delta_Q(B_hat_g, s)
            scores = np.zeros(len(unmoved))
            for k_index in range(scores.size):
                k = comm_nodes.index(unmoved[k_index])
                s[k, 0] = -s[k, 0]
                scores[k_index] = utils._get_delta_Q(B_hat_g, s) - Q0
                s[k, 0] = -s[k, 0]
            _j = np.argmax(scores)
            j = comm_nodes.index(unmoved[_j])
            # move j, which has the largest increase or smallest decrease
            s[j, 0] = -s[j, 0]
            node_indices = np.append(node_indices, j)
            if node_improvement.size < 1:
                node_improvement = np.append(node_improvement, scores[_j])
            else:
                node_improvement = np.append(node_improvement, \
                                        node_improvement[-1]+scores[_j])
            #print len(unmoved), 'max: ', max(scores), node_improvement[-1]
            unmoved.pop(_j)
        # the biggest improvement
        max_index = np.argmax(node_improvement)
        # change all the remaining nodes
        # which are not helping
        for i in range(max_index+1, len(comm_nodes)):
            j = node_indices[i]
            s[j,0] = -s[j, 0]
        # if we swap all the nodes, it is actually doing nothing
        if max_index == len(comm_nodes) - 1:
            delta_modularity = 0
        else:
            delta_modularity = node_improvement[max_index]
        # Stop if ΔQ <= 0 
        if delta_modularity <= 0:
            break
