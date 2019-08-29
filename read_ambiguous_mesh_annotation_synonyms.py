#!/usr/bin/python3

# this script reads MeSH names and synonyms
# and identifies those names that are ambiguous because they share at least a synonym

#MeSH UMLS file
input_file = "./data/MeSH-RxNORM-MeDRA-NCI-HPO.txt"
# list of ambiguous synonyms and names
output_file = "ambiguous_names_and_annotations.txt"
# statistics on number of synonyms per name
results_file = "synonyms_per_mesh.txt"


import re 
import gzip

f = open(input_file, 'r')

# read MeSH IDs, names and synonyms
annotation_dict = {}
synonym_to_annotation_id = {}
total_annotations = 0
total_synonyms = 0
annotation_count = {}
mesh_id_annotation_id = {}
synonyms_from_mesh = 0
for line in f:
    line = line[:-1]
    data = line.split("|")
    annotation_id = data[0]
    annotation_synonym = data[14]
    ontology = data[11]
    if ontology == "MSH":
        mesh_id = data[13]
        mesh_id_annotation_id[annotation_id] = mesh_id
        synonyms_from_mesh += 1
    # an annotation synonym needs to include at least a letter
    if re.search("[a-zA-Z]", annotation_synonym):
        annotation_dict[annotation_id] = 1
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

print("Total annotations: " + str(len(annotation_dict.keys())))
print("Total synonyms: " + str(total_synonyms))
print("Total synonyms coming from MeSH: " + str(synonyms_from_mesh))

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
        id_list = []
        for annotation_id in synonym_to_annotation_id[annotation_synonym]:
            if annotation_id in mesh_id_annotation_id.keys():
                mesh_id = mesh_id_annotation_id[annotation_id]
                if mesh_id not in id_list:
                    id_list.append(mesh_id)
        if len(id_list) > 1:
            f_out.write(annotation_synonym + "\t" + "|".join(id_list) + "\n")
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
