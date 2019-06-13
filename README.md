# global_labor_flow_network
This package aims to share the core algorithms used in the paper, "Global labor flow network reveals the hierarchical organization and dynamics of geo-industrial clusters"

There are three main algorithms:
1. Recursive Louvain
2. Community Label Log-odds Calculation with Dirichlet Prior
3. Hierarchical Community Pruning

## Recursive Louvain
Recursive Louvain iteratively applies the louvain algorithm, using an extension of the python-louvain library to the directed case, until communities are smaller than a target size. The python script is located in recursive_louvain/run_recursive_louvain.py and should be run with the following options:

	-g : The path of a networkx DiGraph input file as a pickle.
	-r : The path to write the output tsv file of cluster-node memberships in the format of: {clusterId}\t{comma-separated-list of nodes in cluster}
	-m : (Optional, default=10) Maximum size at which to stop splitting communities
	-v : (Optional, default=False) Whether to run in verbose mode (prints messages during run to the terminal)

## Log-Odds Calculation with Dirichlet Prior
An implementation of the method described in Monroe, B. L., Colaresi, M. P. & Quinn, K. M. Fightin’ words: Lexical feature selection and evaluation for identifying the content of political conflict. Political Analysis 16, 372–403 (2008) to find the log-odds ratio with informative Dirichlet prior between labels within a cluster and the "background corpus" of all labels. The python script is located in calculate_logodds/run_calculate_logodds.py and should be run with the following options:

	-c : The path of the cluster membership file (the output of recursive louvain)
	-l : The path to a label tsv file in the format: {clusterId}\t{attrId}\t{attrVal}\t{clustAttrCount}\t{meanCompAttrProp}\t{clustAttrProp} where clusterId is the cluster Id in the cluster membership file, attrId is an ID for the attribute of interest, attrVal is a string describing the attribute, clustAttrCount is the number of times the attribute occurs for employees within the cluster, meanCompAttrProp is the mean proportion of the attribution per company, clustEmployeeCount is the number of employees within the cluster, and clustAttrProp is the overall proportion of the attribute among all employees in the cluster
	-o : The output path to write the top logodds ratio of the labels to the background corpus in the format: {clusterId}\t{attrVal}\t{logoddsRatio}

## Hierarchical Community Pruning
This algorithm prunes the hierarchy of communities based on the coherence of its labels. It is described in more detail in the paper as Algorithm 1. The python scipt is located in prune_hierarchy/run_prune_hierarchy.py and should be run with the following options:

	-c : The path of the cluster membership file (the output of recursive louvain)
	-r : The path to the region label top-log-odds file (the output of the log odds calculation with Dirichlet prior)
	-i : The path to the industry label top-log-odds file (the output of the log offs calculation with Dirichlet prior)
	-z : The z-threshold at which to continue to child communities
	-s : The save-threshold at which to save keep communities
	-o : (Optional) The output location to store the full pruned hierarchy in the format: {clusterId}\t{comma-separated-list of nodes in cluster}
	-p : (Optional) The output location to store the lowest level pruned communities in the format: {clusterId}\t{comma-separated-list of nodes in cluster}

## Dependencies
These scripts were tested with following packages versions

	python		2.7.14
	pandas		0.22.0
	numpy		1.14.0
	scipy		1.0.0
	networkx	2.2