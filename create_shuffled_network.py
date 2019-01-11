#!/usr/bin/python3

# this script creates a shuffled version of the original network
# the shuffling is done by shuffling the first PMID of all PMID pairs
# that define the network

import random

input_file = "pmid_citations.txt"
output_file = "pmid_citations_shuffled.txt"

# first it reads the first PMIDs 
# from all the pairs of PMIDs in the original network
print("Reading citations...")
f_in = open(input_file, "r")

pmid_list = []
for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    pmid_list.append(pmid)

# then it shuffles these PMIDs
print("Shuffling...")
random.shuffle(pmid_list)

# and finally puts then back in the network
print("Write output...")
f_in = open(input_file, "r")
f_out = open(output_file, "w")

counter = 0
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = data[0]
    pmid2 = data[1]    
    pmid_shuffled = pmid_list[counter]
    f_out.write(pmid_shuffled + "\t" + pmid2 + "\n")
    counter += 1
