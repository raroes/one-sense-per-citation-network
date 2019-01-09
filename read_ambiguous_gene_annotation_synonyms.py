#!/usr/bin/python3

input_file = "./data/Homo_sapiens.gene_info.gz"
output_file = "ambiguous_names_and_annotations.txt"
results_file = "synonyms_per_gene.txt"

import re 
import gzip

f = gzip.open(input_file, 'rt')

gene_strings = []
synonym_to_gene_id = {}
total_genes = 0
total_synonyms = 0
for line in f:
    line = line[:-1]
    data = line.split("\t")
    species = data[0]
    gene_id = data[1]
    gene_name = data[2]
    gene_synonyms = data[4].split("|")
    gene_synonyms.append(gene_name)
    if species == "9606":
        total_genes += 1
        for gene_synonym in gene_synonyms:
            if re.search("[a-zA-Z]", gene_synonym):
                gene_synonym = gene_synonym.lower()
                if gene_synonym in synonym_to_gene_id.keys():
                    if gene_id not in synonym_to_gene_id[gene_synonym]:
                        synonym_to_gene_id[gene_synonym].append(gene_id)
                else:
                    synonym_to_gene_id[gene_synonym] = [gene_id]
                    total_synonyms += 1

print("Total (human) genes: " + str(total_genes))
print("Total synonyms: " + str(total_synonyms))

f_out = open(output_file, "w")

count_ambiguous = 0
count_non_ambiguous = 0

ambiguous_gene_list = {}
gene_ids_per_ambiguous_synonym = {}
for gene_synonym in synonym_to_gene_id.keys():
    number_of_ids = len(synonym_to_gene_id[gene_synonym])
    if number_of_ids not in gene_ids_per_ambiguous_synonym:
        gene_ids_per_ambiguous_synonym[number_of_ids] = 0
    gene_ids_per_ambiguous_synonym[number_of_ids] += 1
    if number_of_ids > 1:
        f_out.write(gene_synonym + "\t" + "|".join(synonym_to_gene_id[gene_synonym]) + "\n")
        count_ambiguous+=1
        for gene_id in synonym_to_gene_id[gene_synonym]:
            if gene_id not in ambiguous_gene_list.keys():
                ambiguous_gene_list[gene_id] = 1
    else:
        count_non_ambiguous+=1

print("Writing synonym counts to " + results_file + "...")
f_out = open(results_file, "w")
f_out.write("Synonym count\tNumber of genes\n")
for i in range(1,max(gene_ids_per_ambiguous_synonym.keys())+1):
    if i in gene_ids_per_ambiguous_synonym.keys():
        count = gene_ids_per_ambiguous_synonym[i]
    else:
        count = 0
    # print("Number of synonyms that belong to " + str(i) + " gene(s): " + str(count))
    f_out.write(str(i) + "\t" + str(count) + "\n")

print("Genes with ambiguous synonyms: " + str(len(ambiguous_gene_list.keys())))
