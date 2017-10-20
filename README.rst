Python implementation of Newman's spectral methods to maximize modularity.
==========================================================================

See:
    - Leicht, E. A., & Newman, M. E. J. (2008). Community Structure in Directed Networks. Physical Review Letters, 100(11), 118703. https://doi.org/10.1103/PhysRevLett.100.118703

    - Newman, M. E. J. (2006). Modularity and community structure in networks. Proceedings of the National Academy of Sciences of the United States of America, 103(23), 8577–82. https://doi.org/10.1073/pnas.0601602103

A quick start can be found .. _here: https://zhiyzuo.github.io/python-modularity-maximization/

All the datasets in `./data` comes from http://www-personal.umich.edu/~mejn/netdata/

Specifically, `big_10_football_directed.gml` is compiled by myself to test community detection for directed network. I combined data from http://www.sports-reference.com/cfb/conferences/big-ten/2005-schedule.html and the original `football.gml` to define the edge directions.

Change log:

- 10-20-2017
  Updated python codes to use NetworkX 2 APIs. See https://networkx.github.io/documentation/stable/release/release_2.0.html.
  Later in the day, I added a wrapper function to retrieve the largest eigenvalue and vector for 2x2 matrices since scipy.sparse.linalg.eigs do not work in that case. 
