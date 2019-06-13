import math
from collections import Counter

def get_cluids(hier_file):
    return set(i.strip('\n').split('\t')[0] for i in open(hier_file))
	
def logodds_for_two_docs(name2doc, bg_counter=None, doc_size_dic=None, bg_size=None):
    from collections import Counter
    """ It calculates the log odds ratio of term i's frequency between 
    a target corpus and another corpus, with the prior information from
    a background corpus. Inputs are:
    
    - a dictionary of Counter objects (corpora of our interest)
    - a Counter objects (background corpus): if None, this function will create one
      by adding up all document counters. 

    You can pass doc_size_dic (document name -> number of words (sum of cnt values)) 
    and/or bg_size (an integer. the number of words in the background corpus). 
    
    Output is a dictionary of dictionaries. Each dictionary contains the log 
    odds ratio of each word. 
    
    """
    if not bg_counter:
        # put all docs together to create a bg_counter. 
        bg_counter = {}
        for i in name2doc:
            bg_counter = bg_counter.copy()
        bg_counter = reduce(lambda x, y: dict(Counter(x)+Counter(y)), name2doc.values())
        bg_size = sum(bg_counter.values())
    if not doc_size_dic:
        doc_size_dic = dict([(c, sum(name2doc[c].values())) for c in name2doc])
    if not bg_size:
        bg_size = sum(bg_counter.values())

    result = dict([(c, {}) for c in name2doc])
    
    name_i, name_j = list(name2doc.keys())
    di = name2doc[name_i]
    dj = name2doc[name_j]
    for word in bg_counter:
        if word not in di or word not in dj:
            continue
        fi = di[word]
        fj = dj[word]
        fbg = bg_counter[word]
        ni = doc_size_dic[name_i]
        nj = doc_size_dic[name_j]
        try:
            oddsratio = math.log(fi+fbg) - math.log(ni+bg_size-(fi+fbg)) -\
                        math.log(fj+fbg) + math.log(nj+bg_size-(fj+fbg))
            std = 1.0 / (fi+fbg) + 1.0 / (fj+fbg)
            z = oddsratio / math.sqrt(std)
        except:
            continue

        result[name_i][word] = z
    return result

def logodds(name2doc, bg_counter=None, doc_size_dic=None, bg_size=None):
    from collections import Counter
    """ It calculates the log odds ratio of term i's frequency between 
    a target corpus and another corpus, with the prior information from
    a background corpus. Inputs are:
    
    - a dictionary of Counter objects (corpora of our interest)
    - a Counter objects (background corpus): if None, this function will create one
      by adding up all document counters. 

    You can pass doc_size_dic (document name -> number of words (sum of cnt values)) 
    and/or bg_size (an integer. the number of words in the background corpus). 
    
    Output is a dictionary of dictionaries. Each dictionary contains the log 
    odds ratio of each word. 
    
    """
    if not bg_counter:
        # put all docs together to create a bg_counter. 
        bg_counter = {}
        for i in name2doc:
            bg_counter = bg_counter.copy()
        bg_counter = reduce(lambda x, y: dict(Counter(x)+Counter(y)), name2doc.values())
        bg_size = sum(bg_counter.values())
    if not doc_size_dic:
        doc_size_dic = dict([(c, sum(name2doc[c].values())) for c in name2doc])
    if not bg_size:
        bg_size = sum(bg_counter.values())

    result = dict([(c, {}) for c in name2doc])
    
    for name, doc in name2doc.items():
        for word in doc:
            #if 10 > sum(1 for corpus in name2doc.values() if corpus[word]):
            #    continue
            
            fi = doc[word]
            fbg = bg_counter[word]
            #fj = sum(d[word] for x, d in name2doc.items() if word in d and x != name)
            fj = fbg - fi
            ni = doc_size_dic[name]
            #nj = sum(size for x, size in doc_size_dic.items() if x != name)
            nj = bg_size - ni
            try:
                oddsratio = math.log(fi+fbg) - math.log(ni+bg_size-(fi+fbg)) -\
                            math.log(fj+fbg) + math.log(nj+bg_size-(fj+fbg))
                std = 1.0 / (fi+fbg) + 1.0 / (fj+fbg)
                z = oddsratio / math.sqrt(std)
            except:
                continue
            result[name][word] = z
    return result
    
def generate_attr_dictionary(clfv_file, clusterId_set, freq=True, cpn_level=False):
    """
    Generate the attribute dictionary for applying to log-odd ratio 
    in order to extract the set of significantly frequent category names
    Input
    1. clfv_file: cluster feature vector file, tsv format
    2. clusterId_set: set of cluster ids 
    3. freq: If True then the result is frequency, otherwise the result is portion
    Output: two dictionaries
    1. dictionary as a background corpus, extracted from the whole cluster, '0'
    2. dictionary of dictionaries containing word freqencies(or portions) of each lowest level cluster.
    """

    cluster_attr_dic = {}
    bg_attr_dic = {}

    # Filtering only lowest level clusters and generate sub-dictionaries for them
    for clusterId in clusterId_set:
        cluster_attr_dic[clusterId] = {}

    # Checking if the cluster is the lowest level one, and save it to 
    with open(clfv_file) as f:
        next(f)
        for line in f:
            line = line.strip('\n').split('\t')
            # For previous data
            #clId, attrVal, emplCount, attrProp = line[1], line[3], int(line[6]), float(line[7])
            # For current data
            if cpn_level:
                clId, attrVal, emplCount, attrProp = line[0], line[2], int(line[3]), float(line[5])
            else:
                clId, attrVal, emplCount, attrProp = line[0], line[2], int(line[5]), float(line[6])

            if clId in cluster_attr_dic:
                if freq:
                    cluster_attr_dic[clId][attrVal] = attrProp * emplCount
                else:
                    cluster_attr_dic[clId][attrVal] = attrProp
                
            elif clId == '0':
                if freq:
                    bg_attr_dic[attrVal] = attrProp * emplCount
                else:
                    bg_attr_dic[attrVal] = attrProp
    
         
    return [bg_attr_dic, cluster_attr_dic]
	