#!/usr/bin/python3

# this script predicts the most likely annotation of an ambiguous mention

import sys

# the citation file is a parameter that can be changed
if len(sys.argv) > 1:
    input_citation_file = sys.argv[1]
else:
    input_citation_file = "pmid_citations.txt"

input_file = "pmid_ambiguous_annotations_title_abstract_mention.txt"
input_annotation_file = "pmid_annotations.txt"

f_in = open(input_file, "r")

pmids = set()

# reads all the PMIDs with mentions that are ambiguous
for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    pmids.add(pmid)

counter=0
pmid_connections = {}

# reads all annotations available
f_in = open(input_annotation_file, "r")

print("Reading annotations...")
annotations_pmid = {}

counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid in pmids:
        annotations_pmid[pmid] = data[1]

print("Reading citation data...")

# read the file with citation data, which is a list of PMID pairs
f_in = open(input_citation_file, "r")

annotations_network = {}
all_connection_count = {}
annotated_connection_count = {}
for line in f_in:
    data = line[:-1].split("\t")
    counter+=1
    if counter / 1000000 == int(counter / 1000000):
        print("Read " + str(counter) + " connections.")
    if len(data) > 1:
        # for each pair of PMIDs
        pmid1 = data[0]
        pmid2 = data[1]
        # check if the first PMID is annotated
        if pmid1 in pmids:
            #print(pmid1)
            if pmid2 in annotations_pmid.keys():
                if pmid1 in annotations_network.keys():
                    annotations_network[pmid1] = annotations_network[pmid1] + "|" + annotations_pmid[pmid2]
                else:
                    annotations_network[pmid1] = annotations_pmid[pmid2]
        if pmid2 in pmids:
            if pmid1 in annotations_pmid.keys():
                if pmid2 in annotations_network.keys():
                    annotations_network[pmid2] = annotations_network[pmid2] + "|" + annotations_pmid[pmid1]
                else:
                    annotations_network[pmid2] = annotations_pmid[pmid1]

# reads all the ambiguous mentions
f_in = open(input_file, "r")

semantic_permanence_correct_count = 0
semantic_permanence_incorrect_count = 0

for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    base_annotation = data[1]
    ambiguous_annotations = data[2].split("|")
    # for each ambiguous mention check the record's neighborhood
    # to count the annotations statistics
    if pmid in annotations_network.keys():
        annotations = annotations_network[pmid]
        annotation_counts = {}
        for annotation in annotations.split("|"):
            if annotation in ambiguous_annotations:
                if annotation in annotation_counts.keys():
                    annotation_counts[annotation] += 1
                else:
                    annotation_counts[annotation] = 1
        max_count = 0
        #for annotation in annotation_counts:
        #    print(annotation + "\t" + str(annotation_counts[annotation]))

        # pick the most frequent annotation as prediction
        if len(annotation_counts.keys()) > 0:
            max_value = max(annotation_counts.values())
            # if there are several annotations with the same maximum count then discard
            if list(annotation_counts.values()).count(max_value) == 1:
                # check whether the prediction was correct
                max_key = max(annotation_counts, key=annotation_counts.get)
                if max_key == base_annotation:
                    semantic_permanence_correct_count += 1
                else:
                    semantic_permanence_incorrect_count += 1
            #print(str(semantic_permanence_correct_count) + "//" + str(semantic_permanence_incorrect_count))

print("Total correct predictions:" + str(semantic_permanence_correct_count))
print("Total incorrect predictions:" + str(semantic_permanence_incorrect_count))

accuracy = semantic_permanence_correct_count / (semantic_permanence_correct_count + semantic_permanence_incorrect_count)

print("Accuracy: " + str(accuracy))
