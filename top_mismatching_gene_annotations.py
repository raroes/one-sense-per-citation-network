#!/usr/bin/python3

# this script identifies gene annotations which are associated to
# most mistaching pairs

input_file = "connected_pmid_annotations_ambiguous.txt"

mapping_file = "./data/Homo_sapiens.gene_info.gz"

# first it reads which synonyms are ambiguous for each annotation
import gzip

f = gzip.open(mapping_file, 'rt')

name_id = {}
name_synonyms = {}
for line in f:
    line = line[:-1]
    data = line.split("\t")
    species = data[0]
    gene_id = data[1]
    gene_name = data[2]
    if species == "9606":
        name_id[gene_id] = gene_name
        gene_synonyms = data[4].split("|")
        gene_synonyms.append(gene_name)
        name_synonyms[gene_id] = gene_synonyms

f_in = open(input_file, "r")

# then it goes through the matching analysis output
# which lists all matching and mismatching hits
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
        if int(annotation1) > int(annotation2):
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
print("Gene name\tGene ID\tMatching\tGene name\tGene ID\tMatching\tMismatching\tCommon synonyms")
for annotation_pair in sorted_mismatch_counts[0:10]:
    annotations = annotation_pair.split("_")
    annotation_id1 = annotations[0]
    annotation_name1 = name_id[annotation_id1]
    annotation_id2 = annotations[1]
    annotation_name2 = name_id[annotation_id2]
    overlapping_synonyms = list(set(name_synonyms[annotation_id1]) & set(name_synonyms[annotation_id2]))
    print(annotation_name1 + "\t" + annotation_id1 + "\t" + str(match_counts[annotation_id1]) + "\t" + annotation_name2 + "\t" + annotation_id2 + "\t" + str(mismatch_counts[annotation_pair]) + "\t" + str(match_counts[annotation_id2]) + "\t" + ",".join(overlapping_synonyms))
