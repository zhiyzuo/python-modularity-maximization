# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx

def get_base_modularity_matrix(network):
    '''
        Obtain the modularity matrix for the whole network

        Parameters
        ----------
        network : nx.Graph or nx.DiGraph
            The network of interest

        Returns
        -------
        np.matrix
            The modularity matrix for `network`

        Raises
        ------
        TypeError
            When the input `network` does not fit either nx.Graph or nx.DiGraph
    '''

    if type(network) == nx.Graph:
        return nx.modularity_matrix(network)
    elif type(network) == nx.DiGraph:
        return nx.directed_modularity_matrix(network)
    else:
        raise TypeError('Graph type not supported. Use either nx.Graph or nx.Digraph')

def get_modularity(network, community_dict):
    '''
        Calculate the modularity

        Undirected:
            Q = 1/2m * ∑[A_ij - k_i * k_j/2m] * δ_(c_i, c_j)
        Directed:
            Q = 1/m * ∑[A_ij - k_i^in * k_j^out / m] * δ_(c_i, c_j)

        Parameters
        ----------
        network : nx.Graph or nx.DiGraph
            The network of interest
        community_dict : dict
            A dictionary to store the membership of each node
            Key is node and value is community index

        Returns
        -------
        float
            The modularity of `network` given `community_dict`
    '''

    Q = 0
    A = nx.to_scipy_sparse_matrix(network).astype(float)

    if type(network) == nx.Graph:
        # for undirected graphs, in and out treated as the same thing
        in_degree = dict(nx.degree(network))
        out_degree = dict(nx.degree(network))
    elif type(network) == nx.DiGraph:
        in_degree = dict(network.in_degree())
        out_degree = dict(network.out_degree())

    if type(network) == nx.Graph:
        M = 2.*(network.number_of_edges())
    else:
        M = network.number_of_edges()

    node_indices = range(network.number_of_nodes())
    nodes = list(network.nodes())
    for i in node_indices:
        ui = nodes[i]
        for j in node_indices:
            uj = nodes[j]
            if community_dict[ui] == community_dict[uj]:
                Q += A[i,j] - in_degree[ui]*out_degree[uj]/M

    return Q / M


def get_mod_matrix(network, comm_nodes=None, B=None):
    '''
        This function computes the modularity matrix
        for a specific group in the network.
        (a.k.a., generalized modularity matrix)

        Specifically,
            B^g_(i,j) = B_ij - δ_ij * ∑_(k∈g) B_ik
            B_ij = A_ij - k_i*k_j/2m
            m = |E| (total # of edges in the whole network)

        When `comm_nodes` is None or all nodes in `network`, this reduces to `B`

        Parameters
        ----------
        network : nx.Graph or nx.DiGraph
            The network of interest
        comm_nodes : iterable (list, np.array, or tuple)
            List of nodes that defines a community
        B : np.matrix
            Modularity matrix of `network`

        Returns
        -------
        np.matrix
            The modularity of `comm_nodes` within `network`
    '''


    if comm_nodes is None:
        comm_nodes = list(network)
        return get_base_modularity_matrix(network)

    if B is None:
        B = get_base_modularity_matrix(network)

    # subset of mod matrix in g
    indices = [list(network).index(u) for u in comm_nodes]
    B_g = B[indices, :][:, indices]

    # B^g_(i,j) = B_ij - δ_ij * ∑_(k∈g) B_ik
    # i, j ∈ g
    B_hat_g = np.zeros((len(comm_nodes), len(comm_nodes)), dtype=float)

    # ∑_(k∈g) B_ik
    B_g_rowsum = np.asarray(B_g.sum(axis=1))[:, 0]
    if type(network) == nx.Graph:
        B_g_colsum = np.copy(B_g_rowsum)
    elif type(network) == nx.DiGraph:
        B_g_colsum = np.asarray(B_g.sum(axis=0))[0, :]

    for i in range(B_hat_g.shape[0]):
        for j in range(B_hat_g.shape[0]):
            if i == j:
                B_hat_g[i,j] = B_g[i,j] - 0.5 * (B_g_rowsum[i] + B_g_colsum[i])
            else:
                B_hat_g[i,j] = B_g[i,j]

    if type(network) == nx.DiGraph:
        B_hat_g = B_hat_g + B_hat_g.T

    return B_hat_g

