#!/usr/bin/python3

# this script identifies gene annotations which are associated to
# most mistaching pairs

import re

input_file = "connected_pmid_annotations_ambiguous.txt"

#MeSH UMLS file
mapping_file = "./data/MeSH-RxNORM-MeDRA-NCI-HPO.txt"

f = open(mapping_file, "r")

mesh_id_annotation_id = {}
name_synonyms = {}
name_id = {}
for line in f:
    line = line[:-1]
    data = line.split("|")
    annotation_id = data[0]
    annotation_synonym = data[14]
    ontology = data[11]
    if ontology == "MSH":
        mesh_id = data[13]
        name_id[mesh_id] = annotation_synonym
        mesh_id_annotation_id[annotation_id] = mesh_id

f = open(mapping_file, "r")


for line in f:
    line = line[:-1]
    data = line.split("|")
    annotation_id = data[0]
    annotation_synonym = data[14]
    ontology = data[11]
    if annotation_id in mesh_id_annotation_id.keys():
        annotation_id = mesh_id_annotation_id[annotation_id]
        # an annotation synonym needs to include at least a letter
        if re.search("[a-zA-Z]", annotation_synonym):
            # annotation synonyms are considered case-insensitively so they are changed to lower case
            annotation_synonym = annotation_synonym.lower()
            if annotation_id in name_synonyms.keys():
                if annotation_synonym not in name_synonyms[annotation_id]:
                    name_synonyms[annotation_id].append(annotation_synonym)
            else:
                name_synonyms[annotation_id] = [annotation_synonym]

# then it goes through the matching analysis output
# which lists all matching and mismatching hits

f_in = open(input_file, "r")
mismatch_counts = {}
match_counts = {}
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    # if an entry corresponds to a mismatch
    if data[0] == "mismatching":
        annotation1 = data[3]
        annotation2 = data[4]
        # order the annotations to simplify
        if annotation1 > annotation2:
            temp = annotation1
            annotation1 = annotation2
            annotation2 = temp
        # counts a mismatch in a dictionary
        if annotation1 + "_" + annotation2 in mismatch_counts.keys():
            mismatch_counts[annotation1 + "_" + annotation2] += 1
        else:
            mismatch_counts[annotation1 + "_" + annotation2] = 1
    # similarly, here it counts the matchings
    if data[0] == "matching":
        annotation1 = data[3]
        if annotation1 in match_counts.keys():
            match_counts[annotation1] += 1
        else:
            match_counts[annotation1] = 1

# After that it writes the output
# which is sorted and only the annotations
# with the most mismatches are shown

# sort based on mismatching counts
sorted_mismatch_counts = sorted(mismatch_counts, key=mismatch_counts.get, reverse=True)

# write table with statistics
print("MeSH name\tMeSH ID\tMatching\tMeSH name\tMeSH ID\tMatching\tMismatching\tCommon synonyms")
for annotation_pair in sorted_mismatch_counts[0:10]:
    annotations = annotation_pair.split("_")
    annotation_id1 = annotations[0]
    annotation_name1 = name_id[annotation_id1]
    annotation_id2 = annotations[1]
    annotation_name2 = name_id[annotation_id2]
    overlapping_synonyms = list(set(name_synonyms[annotation_id1]) & set(name_synonyms[annotation_id2]))
    print(annotation_name1 + "\t" + annotation_id1 + "\t" + str(match_counts[annotation_id1]) + "\t" + annotation_name2 + "\t" + annotation_id2 + "\t" + str(match_counts[annotation_id2]) + "\t" + str(mismatch_counts[annotation_pair]) + "\t" + ",".join(overlapping_synonyms))
