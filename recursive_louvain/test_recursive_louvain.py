import networkx as nx
import recursive_louvain as rlv

G = nx.barabasi_albert_graph(n=10000, m=5)
print(G.number_of_edges())

rlv.ItrLouvain(G)

