from calculate_logodds import *
import sys

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()


    parser.add_option("-c", "--clusterfile", help="Location of cluster membership file.",
                    type="str", dest="clusterfile")
    parser.add_option("-l", "--label_file", help="Input file of label counts per cluster",
                    type="str", dest="labelfile")
    parser.add_option("-o", "--output", help="Output path for logodds", 
                    type="str", dest="output")

    options, args = parser.parse_args(sys.argv[1:])

    hier_file = options.clusterfile
    clfv_file = options.labelfile
    cluids = get_cluids(hier_file)

    bg_attr_dic, clu_attr_dic = generate_attr_dictionary(clfv_file, cluids)
    lo_dic = logodds(clu_attr_dic, bg_attr_dic)
    fout = open(options.output, 'w')

    for cluid in sorted(lo_dic.keys(), key=lambda x: map(int, x.split(','))):
        try:
            attr, z = sorted(lo_dic[cluid].items(), key=lambda x: x[1], reverse=True)[0]
        except:
            attr, z = '-', '0.0'
        fout.write('{}\t{}\t{}\n'.format(cluid, attr, z))

