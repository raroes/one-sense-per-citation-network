#!/usr/bin/python3

# this script maps DOIs from Open Citation Index citations
# to PMIDs using the mapping data from the EBI PMID-PMCID-DOI dataset

import re

mapping_file = "./data/PMID_PMCID_DOI.csv"
input_citation_file = "./data/data.csv"
output_citation_file = "pmid_citations.txt"

f_in = open(mapping_file, "r")

# first it reads all the PMID-DOI mappings provided 
# by the EBI mapping file
pmid_doi = {}
pmids = {}
counter=0
matched_counter=0
print("Read mappings of PMID to DOI...")
for line in f_in:
    line = line[:-1]
    data = line.split(",")
    pmid = data[0]
    doi = data[2]
    counter+=1
    if counter / 100000 == int(counter / 100000):
        print("Read " + str(counter) + " lines")
    if pmid != "" and doi != "":
        if re.search("[0-9a-z]", doi):
            if pmid not in pmids.keys():
                # DOI links are converted to DOI values
                doi = doi.replace("\"", "")
                doi = doi.replace("https://doi.org/", "")
                pmid_doi[doi] = pmid
                pmids[pmid] = 1
                matched_counter+=1

print("Total entries read: " + str(counter))
print("Number of PMIDs matched to DOIs: " + str(matched_counter))

# then it reads the citation data from the Open Citation Index
# and tries to map each pair of DOIs to PMIDs when possible

f_out = open(output_citation_file, "w")
f_in = open(input_citation_file, "r")

counter=0
link_counter = 0
for line in f_in:
    data = line.split(",")
    counter+=1
    if counter / 1000000 == int(counter / 1000000):
        print("Read " + str(counter) + " links, " + str(link_counter) + " matched")
    if len(data) > 2:
        doi1 = data[1]
        doi2 = data[2]
        # DOIs are simplified
        doi1 = doi1.replace("\"","")
        doi2 = doi2.replace("\"","")
        # check if there is mapping available for both DOIs
        if doi1 in pmid_doi.keys():
            if doi2 in pmid_doi.keys():
                link_counter+=1
                # if so then map DOIs to PMIDs and print output
                pmid1 = pmid_doi[doi1]
                pmid2 = pmid_doi[doi2]
                f_out.write(pmid1 + "\t" + pmid2 + "\n")

print("Number of PMIDs matched to DOIs: " + str(matched_counter))

print("Number of citations read: " + str(counter))
print("Number of citations matching PMIDs found: " + str(link_counter))
