#!/usr/bin/python3

# this script reads MeSH names and its UMLS synonyms
# and identifies those names that are ambiguous because they share at least a synonym

# UMLS-MeSH file
input_file = "./data/Homo_sapiens.gene_info.gz"
# list of ambiguous names and synonyms
output_file = "ambiguous_names_and_annotations.txt"
# statistics on number of synonyms per MeSH term
results_file = "synonyms_per_mesh_term.txt"

import re 
import gzip

f = gzip.open(input_file, 'rt')

# read MeSH IDs, names and synonyms
annotation_strings = []
synonym_to_annotation_id = {}
total_annotations = 0
total_synonyms = 0
for line in f:
    line = line[:-1]
    data = line.split("\t")
    # NCBI Gene data of interest
    species = data[0]
    annotation_id = data[1]
    annotation_name = data[2]
    annotation_synonyms = data[4].split("|")
    annotation_synonyms.append(annotation_name)
    # only information related to humans is of interest (species number 9606)
    if species == "9606":
        total_annotations += 1
        for annotation_synonym in annotation_synonyms:
            # an annotation synonym needs to include at least a letter
            if re.search("[a-zA-Z]", annotation_synonym):
                # annotation synonyms are considered case-insensitively so they are changed to lower case
                annotation_synonym = annotation_synonym.lower()
                # check if annotation synonym has already been seen
                if annotation_synonym in synonym_to_annotation_id.keys():
                    # if so, then add the annotation ID to the list of annotation IDs associated to that synonym
                    if annotation_id not in synonym_to_annotation_id[annotation_synonym]:
                        synonym_to_annotation_id[annotation_synonym].append(annotation_id)
                else:
                    # if not, create a new entry for the synonym
                    synonym_to_annotation_id[annotation_synonym] = [annotation_id]
                    total_synonyms += 1

print("Total annotation: " + str(total_annotations))
print("Total synonyms: " + str(total_synonyms))

# Write an output file with the data read in the previous section
f_out = open(output_file, "w")

count_ambiguous = 0
count_non_ambiguous = 0

ambiguous_annotation_list = {}
annotation_ids_per_ambiguous_synonym = {}
for annotation_synonym in synonym_to_annotation_id.keys():
    number_of_ids = len(synonym_to_annotation_id[annotation_synonym])
    # keep statistic on the number of annotation IDs that are associated to each synonym
    if number_of_ids not in annotation_ids_per_ambiguous_synonym:
        annotation_ids_per_ambiguous_synonym[number_of_ids] = 0
    annotation_ids_per_ambiguous_synonym[number_of_ids] += 1
    # only annotation synonyms associated to more than one annotation ID are considered in the output
    if number_of_ids > 1:
        f_out.write(annotation_synonym + "\t" + "|".join(synonym_to_annotation_id[annotation_synonym]) + "\n")
        count_ambiguous+=1
        # add the annotation IDs to a list of ambiguous annotation IDs
        for annotation_id in synonym_to_annotation_id[annotation_synonym]:
            if annotation_id not in ambiguous_annotation_list.keys():
                ambiguous_annotation_list[annotation_id] = 1
    else:
        count_non_ambiguous+=1

# Write an output table with the statistics on number of annotation IDs per synonym
print("Writing synonym counts to " + results_file + "...")
f_out = open(results_file, "w")
f_out.write("Synonym count\tNumber of annotations\n")
for i in range(1,max(annotation_ids_per_ambiguous_synonym.keys())+1):
    if i in annotation_ids_per_ambiguous_synonym.keys():
        count = annotation_ids_per_ambiguous_synonym[i]
    else:
        count = 0
    f_out.write(str(i) + "\t" + str(count) + "\n")

print("Annotations with ambiguous synonyms: " + str(len(ambiguous_annotation_list.keys())))
