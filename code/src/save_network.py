#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The save_network.py module creates a co-occurence matrix and saves 
the matrix to a gefx format for network visualisation using Gephi.
"""


from itertools import chain
from collections import Counter
from collections import OrderedDict

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl


def write_to_gexf():

    data = pd.read_excel(
        '../../data/processed/search_results_processed_concepts_v3.xlsx'
    )

    # prepare data 
    ls = [x for x in data.concepts.tolist() if str(x) != 'nan']
    ls = [x.split(',') for x in ls]
    lst = [[x.replace(' ','') for x in i] for i in ls]

    u = pd.get_dummies(pd.DataFrame(lst), prefix='', prefix_sep='').sum(level=0, axis=1)

    v = u.T.dot(u)
    
    # set 0 to lower triangular matrix
    v.values[np.tril(np.ones(v.shape)).astype(np.bool)] = 0

    # reshape and filter only count > 0
    a = v.stack()
    a = a[a >= 1].rename_axis(('source', 'target')).reset_index(name='weight')

    # write to gexf format
    G = nx.from_pandas_edgelist(a,  edge_attr=True)
    nx.write_gexf(G, "cooccurence_network.gexf")
