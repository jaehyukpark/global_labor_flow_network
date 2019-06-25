import sys
import pythonlouvain as pylouvain
import pythonlouvain.undirected as undirectedlouvain
import os
import glob
import networkx as nx
import pandas as pd
import numpy as np
import subprocess
from collections import defaultdict
    
def get_communities_to_break(comm2nodes, max_comm_size, comm_already_broken):
    communities_to_break = set()
    for commid, nodes in comm2nodes.items():
        if commid in comm_already_broken:
            continue
        if len(nodes) > max_comm_size: # Decide whether breaking down more or not
            communities_to_break.add(commid)
    return communities_to_break

def ItrLouvain(G=None, out_fname='itr_louvain_cls.txt', max_comm_size = 10, verbose=False, directed=True):
    """ 
        iteratively apply louvain method and store communities (all levels). 
        inputs:
        - `input_graph`: a networkx object (weighted, directed graph). 
        - `output_fname`: output filename to store community information. 

        community id takes the form of tuples. (1,2,2,1,5). E.g. (1, 2) can be broken 
        down into (1, 2, 1), (1, 2, 2), (1, 2, 3), ...

        Each line contains a community.  

        community id \t nodeid1 nodeid2 nodeid3 ... 

        e.g. 

        1,2,1\t10002 10239 24 2321\n

        usage: 

        ItrLouvain(G, out_fname, max_comm_size, verbose=False)
    """ 

    # initialization
    if not G:
        G = nx.barbell_graph(10,5)
    comm2nodes = defaultdict(set)
    comm2nodes[(0,)] = set(G.nodes())
    comm_already_broken = set()

    def update_comm2nodes(node2comm, parent_cid):
        # comm2nodes = {comm1: set([node1, node2]), comm2: set([...]), ...}
        # Changed this from G.node_iter()
        for i in node2comm.keys():
            cid = parent_cid + (node2comm[i], )
            comm2nodes[cid].add(i)

    while(True):
        communities_to_break = get_communities_to_break(comm2nodes, 
                                                        max_comm_size, 
                                                        comm_already_broken)
        if not communities_to_break:
            break
        commid = communities_to_break.pop()  # a tuple like (1,2)
        
        comm_already_broken.add(commid)
        nodes = comm2nodes[commid]
        subg = G.subgraph(nodes)
        
        print("Comm: %s" % str(commid))
        print("Nodes in Subgraph: %s" % (len(subg)))
        #print "Communities To Break\n%s" % str(communities_to_break)

        if directed:
            node2comm = pylouvain.best_partition(subg)
        else:
            node2comm = undirectedlouvain.best_partition(subg)
        
        if(len(set(node2comm.values())) > 1):
            update_comm2nodes(node2comm, parent_cid=commid)
        else:
            print("Maximally Decomposed Above Threshold: %s" % str(commid))
            comm_already_broken.add(commid)

    with open(out_fname, 'w') as fout:
        for cid, members in comm2nodes.items():

            cidstr = ','.join(map(str, cid))
            memberstr = ' '.join(map(str, members))
            fout.write('{}\t{}\n'.format(cidstr, memberstr))

    return comm2nodes
