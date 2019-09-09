#!/usr/bin/python3

# this script creates a list of pairs of PubMed records connected by citations

import sys

# the citation file is a parameter that can be changed
if len(sys.argv) > 1:
    input_citation_file = sys.argv[1]
else:
    input_citation_file = "pmid_citations.txt"

input_file = "pmid_ambiguous_annotations.txt"
output_file = "connected_pmid_annotations.txt"

# read a list of annotations
# in our case this is a list of ambiguous annotations
f_in = open(input_file, "r")

print("Reading annotations...")
annotations_pmid = {}
pmids = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        # create a dictionary of annotations for each PMID
        annotations_pmid[pmid] = data[1]
        pmids[pmid] = 1
        for annotation in annotations_pmid[pmid].split("|"):
            counter_annotations += 1

print("Annotations read: " + str(counter_annotations))

connection_counter=0
counter=0
pmid_connections = {}

print("Reading citation data...")

# read the file with citation data, which is a list of PMID pairs
f_in = open(input_citation_file)

for line in f_in:
    data = line[:-1].split("\t")
    counter+=1
    if counter / 10000000 == int(counter / 10000000):
        print("Read " + str(counter) + " connections, " + str(connection_counter) + " matched to annotated references")
    if len(data) > 1:
        # for each pair of PMIDs
        pmid1 = data[0]
        pmid2 = data[1]
        # check if both PMIDs have (ambiguous) annotations
        if pmid1 in pmids.keys():
            if pmid2 in pmids.keys():
                # if so then add them to the dictionary
                connection_counter+=1
                if pmid1 not in pmid_connections.keys():
                    pmid_connections[pmid1] = [pmid2]
                else:
                    pmid_connections[pmid1].append(pmid2)

print("Number of pairs read: " + str(counter))
print("Number of ambiguous annotated pairs found: " + str(connection_counter))

# Write as output the pairs of connected PMIDs and their corresponding annotations
print("Writing output...")
f_out = open(output_file, "w")
for pmid1 in pmid_connections.keys():
    annotations1 = annotations_pmid[pmid1]
    for pmid2 in pmid_connections[pmid1]:
        annotations2 = annotations_pmid[pmid2]
        f_out.write(pmid1 + "\t" + annotations1 + "\t" + pmid2 + "\t" + annotations2 + "\n")
