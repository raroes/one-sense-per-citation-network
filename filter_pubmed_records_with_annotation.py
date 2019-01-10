#!/usr/bin/python3

# this script selects PMIDs with at least one ambiguous annotation

import sys

pubmed_file = "pmid_annotations.txt"

input_file = "ambiguous_names_and_annotations.txt"
output_file = "pmid_ambiguous_annotations.txt"

# first it reads annotations types that are ambiguous (i.e. have more than one synonym)
print("Reading ambiguous annotations list...")
f_in = open(input_file, "r")

ambiguous_annotations = {}
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    annotations = data[1].split("|")
    for annotation in annotations:
        if annotation not in ambiguous_annotations:
            ambiguous_annotations[annotation] = 1

print("Ambiguous annotation types read: " + str(len(ambiguous_annotations)))

# then it reads available annotations and selects only those that are considered ambiguous 
# based on the data read before
print("Reading annotations...")
f_in = open(pubmed_file, "r")

counter = 0
pmid_with_ambiguous_annotation = {}
ambiguous_annotation_count = 0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    annotations = data[1].split("|")
    pmid = data[0]
    counter += 1
    for annotation in annotations:
        # check if annotation is ambiguous
        if annotation in ambiguous_annotations.keys():
            ambiguous_annotation_count += 1
            # mark at PMID as having an ambiguous annotation
            if pmid not in pmid_with_ambiguous_annotation.keys():
                pmid_with_ambiguous_annotation[pmid] = [annotation]
            else:
                pmid_with_ambiguous_annotation[pmid].append(annotation)

print("Number of PMIDs annotated with ambiguous annotations: " + str(len(pmid_with_ambiguous_annotation)))
print("Number of annotations associated to ambiguous annotation types: " + str(ambiguous_annotation_count))

# The output consists in a filtered version of the input
# only entries with at least one ambiguous annotation are kept
print("Writing output...")
f_out = open(output_file, "w")
for pmid in pmid_with_ambiguous_annotation.keys():
    f_out.write(pmid + "\t" + str("|".join(pmid_with_ambiguous_annotation[pmid])) + "\n")
