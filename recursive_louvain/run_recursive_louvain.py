import networkx as nx
import recursive_louvain as rlv
import pickle as p
import sys

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-g", "--graphfile", help="Location of the networkx graph input file as a pickle.",
                    type="str", dest="graphfile")
    parser.add_option("-r", "--outputfile", help="Location to write txt file of cluster-node memberships.",
                    type="str", dest="outputfile")
    parser.add_option("-m", "--maxcommsize", help="Maximum size at which to stop splitting communities",
    				type="int", dest="maxcommsize", default=10)
    parser.add_option("-v", "--verbose", help="Whether to print verbose messages during run",
    				action="store_true", dest="verbose", default=False)


    options, args = parser.parse_args(sys.argv[1:])
    graphPath = options.graphfile
    outPath = options.outputfile
    max_comm_size = options.maxcommsize 
    verbose = options.verbose

    G = p.load(open(graphPath, 'r'))
    rlv.ItrLouvain(G, out_fname=outPath, max_comm_size = max_comm_size, verbose=verbose)