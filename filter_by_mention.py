#!/usr/bin/python3

# this script selects records that have mentions of ambiguous annotations

import re

input_file = "pmid_ambiguous_annotations_title_abstract.txt"
output_file = "pmid_ambiguous_annotations_title_abstract_mention.txt"
input_file_ambiguous = "ambiguous_names_and_annotations.txt"


# firstreads annotation types that are ambiguous (i.e. have more than one synonym)
print("Reading ambiguous annotations list...")
f_in = open(input_file_ambiguous, "r")

ambiguous_synonym_annotation = {}
annotation_ambiguous_synonym = {}

for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    annotations = data[1].split("|")
    ambiguous_synonym = data[0]
    for annotation in annotations:
        if annotation not in ambiguous_synonym_annotation.keys():
            ambiguous_synonym_annotation[annotation] = [ambiguous_synonym]
        else:
            ambiguous_synonym_annotation[annotation].append(ambiguous_synonym)
        if ambiguous_synonym not in annotation_ambiguous_synonym.keys():
            annotation_ambiguous_synonym[ambiguous_synonym] = [annotation]
        else:
            annotation_ambiguous_synonym[ambiguous_synonym].append(annotation)

f_in = open(input_file, "r")
f_out = open(output_file, "w")

print("Reading annotations...")

# read records with ambiguous annotations
for line in f_in:
    data = line[:-1].split("\t")
    pmid = data[0]
    annotations = data[1].split("|")
    title = data[2]
    abstract = data[3]
    for annotation in annotations:
        found = 0
        found_annotations = []
        found_names = []
        # select only those that have at least one mention of an ambiguous name
        if annotation in ambiguous_synonym_annotation.keys():
            names = ambiguous_synonym_annotation[annotation]
            for name in names:
                pattern = "\\b" + re.escape(name.lower()) + "\\b"
                if re.search(pattern, " " + title.lower() + " ") or re.search(pattern, " " + abstract.lower() + " "):
                    found = 1
                    found_names = found_names + [name]
                    found_annotations = found_annotations + annotation_ambiguous_synonym[name]
        if found == 1:
            f_out.write(pmid + "\t" + annotation + "\t" + "|".join(found_annotations) + "\n")

