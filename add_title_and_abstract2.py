#!/usr/bin/python3


# this script simply adds the title and abstract corresponding to each PMID in the input file

input_file = "pmid_ambiguous_annotations.txt"
output_file = "pmid_ambiguous_annotations_title_abstract.txt"
title_abstract_file = "./data/pmid_title_abstract.txt"

f_in = open(input_file, "r")

# the input file, which is made of pairs of PMIDs and their annotations is read

print("Reading annotations...")

pmid_list = {}

for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    pmid_list[pmid] = 1

# then a file which contains all titles and abstracts from MEDLINE is read
# only those titles and abstracts for PMIDs identified in the input file are recorded
print("Reading titles and abstracts...")

title_pmid = {}
title_abstract = {}
abstract_pmid = {}

f_in = open(title_abstract_file, "r")

for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    title = data[1]
    abstract = data[2]
    # the title and abstract are recorded only if the PMID was in the input file
    if pmid in pmid_list.keys():
        title_pmid[pmid] = title
        abstract_pmid[pmid] = abstract

print("Reading and writing annotations...")

f_out = open(output_file, "w")
f_in = open(input_file, "r")

# the output file is like the input file but with the corresponding titles and abstracts added
for line in f_in:
    data = line[:-1].split("\t")
    title = ""
    abstract = ""
    pmid = data[0]
    if pmid in title_pmid.keys():
        title = title_pmid[pmid]
    if pmid in abstract_pmid.keys():
        abstract = abstract_pmid[pmid]
    f_out.write(line[:-1] + "\t" + title + "\t" + abstract + "\n")
