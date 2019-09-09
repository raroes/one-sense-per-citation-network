#!/usr/bin/python3

input_file = "pmid_citations.txt"
output_file = "pmid_citations_sorted.txt"


f_in = open(input_file, "r")

pair_pmids = {}

counter = 0
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = int(data[0])
    pmid2 = int(data[1])
    if pmid1 not in pair_pmids.keys():
        pair_pmids[pmid1] = [pmid2]
    else:
        pair_pmids[pmid1].append(pmid2)
    if pmid2 not in pair_pmids.keys():
        pair_pmids[pmid2] = [pmid1]
    else:
        pair_pmids[pmid2].append(pmid1)
    counter += 1
    if counter / 1000000 == int(counter / 1000000):
        print(counter)

print("Citations read...\n")

f_out = open(output_file, "w")

for pmid1 in pair_pmids.keys():
    for pmid2 in pair_pmids[pmid1]:
        f_out.write(str(pmid1) + "\t" + str(pmid2) + "\n")
