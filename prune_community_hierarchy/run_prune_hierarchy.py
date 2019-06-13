import os
import sys
import random
import pandas as pd
from prune_hierarchy import *
from collections import Counter
from matplotlib.pylab import *

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-c", "--clusterfile", help="Location of cluster membership file.",
                    type="str", dest="clusterfile")
    parser.add_option("-r", "--regionlogoddsfile", help="Location of node region logodds file.",
                    type="str", dest="regionlogoddsfile")
    parser.add_option("-i", "--industrylogoddsfile", help="Location of node industry logodds file.",
                    type="str", dest="industrylogoddsfile")
    parser.add_option("-z", "--zthreshold", help="Threshold z value to split cluster ",
                    type="double", dest="zthr"),
    parser.add_option("-s", "--savethreshold", help="Threshold z value to save cluster.",
                    type="double", dest="sthr"),
                    type="float", dest="zthr"),
    parser.add_option("-s", "--savethreshold", help="Threshold z value to save cluster.",
                    type="float", dest="sthr"),
    parser.add_option("-o", "--prunedpath", help="Output location for full pruned hierarchy",
                    type="str", dest="prunedpath"),
    parser.add_option("-p", "--prunedlowpath", help="Output location for lowest level pruned communities",
                    type="str", dest="prunedlowpath")

    options, args = parser.parse_args(sys.argv[1:])

    zthr=options.zthr
    s_zthr=options.sthr
    categories = []
    industry_logodds_path = options.industrylogoddsfile
    if industry_logodds_path:
        categories.append("ind")
    region_logodds_path = options.regionlogoddsfile
    if region_logodds_path:
        categories.append("reg")

    pruned_path = options.prunedpath
    pruned_low_path = options.prunedlowpath

    mem_path = options.clusterfile
    memberships = pd.read_csv(mem_path, sep='\t', index_col= [0], names=['clusterId', 'companyIds'])

    clusterIds = memberships.copy()
    clusterIds['clusterId'] = memberships.index
    T = get_tree_from_cft(clusterIds)

    lodic = {}
    ind_lo = get_logodds(industry_logodds_path)
    reg_lo = get_logodds(region_logodds_path)
    lodic['ind'] = ind_lo
    lodic['reg'] = reg_lo

    if pruned_low_path:
        minPruned = prune_tomin_threshold(T, lodic, thr=0, zthr=zthr,save_zthr=s_zthr, drop_invalid = True, categories = categories, verbose=False)
        with open(pruned_low_path, 'w') as fout:
            for c in sorted(minPruned, key=lambda x: map(int, x.split(','))):
                fout.write('{}\t{}\t{}\t{}\t{}\n'.format(c, reg_lo[c][0], reg_lo[c][1], ind_lo[c][0], ind_lo[c][1]))
    
    if pruned_path:

        minPruned_parents = set()
        for clusterId in minPruned:#{'0,1,2'}:
            clusterList = clusterId.split(',')
            minPruned_parents.add(clusterId)
            for i in range(1, len(clusterList)):
                minPruned_parents.add(','.join(clusterList[:-i]))
            
        with open(pruned_path, 'w') as fout:
            for c in sorted(minPruned_parents, key=lambda x: map(int, x.split(','))):
                fout.write('{}\t{}\t{}\t{}\t{}\n'.format(c, reg_lo[c][0], reg_lo[c][1],ind_lo[c][0],ind_lo[c][1]))

