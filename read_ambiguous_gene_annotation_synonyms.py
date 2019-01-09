#!/usr/bin/python3

# this script reads NCBI Gene gene names and synonyms 
# and identifies those gene names that are ambiguous because they share at least a synonym

# NCBI Gene file
input_file = "./data/Homo_sapiens.gene_info.gz"
# list of ambiguous gene synonyms and gene names
output_file = "ambiguous_names_and_annotations.txt"
# statistics on number of synonyms per gene
results_file = "synonyms_per_gene.txt"

import re 
import gzip

f = gzip.open(input_file, 'rt')

# read gene names, IDs and synonyms from NCBI Gene data
gene_strings = []
synonym_to_gene_id = {}
total_genes = 0
total_synonyms = 0
for line in f:
    line = line[:-1]
    data = line.split("\t")
    # NCBI Gene data of interest
    species = data[0]
    gene_id = data[1]
    gene_name = data[2]
    gene_synonyms = data[4].split("|")
    gene_synonyms.append(gene_name)
    # only information related to humans is of interest (species number 9606)
    if species == "9606":
        total_genes += 1
        for gene_synonym in gene_synonyms:
            # a gene synonym needs to include at least a letter
            if re.search("[a-zA-Z]", gene_synonym):
                # gene synonyms are considered case-insensitively so they are changed to lower case
                gene_synonym = gene_synonym.lower()
                # check if gene synonym has already been seen
                if gene_synonym in synonym_to_gene_id.keys():
                    # if so, then add the gene ID to the list of gene IDs associated to that synonym
                    if gene_id not in synonym_to_gene_id[gene_synonym]:
                        synonym_to_gene_id[gene_synonym].append(gene_id)
                else:
                    # if not, create a new entry for the synonym
                    synonym_to_gene_id[gene_synonym] = [gene_id]
                    total_synonyms += 1

print("Total (human) genes: " + str(total_genes))
print("Total synonyms: " + str(total_synonyms))

# Write an output file with the data read in the previous section
f_out = open(output_file, "w")

count_ambiguous = 0
count_non_ambiguous = 0

ambiguous_gene_list = {}
gene_ids_per_ambiguous_synonym = {}
for gene_synonym in synonym_to_gene_id.keys():
    number_of_ids = len(synonym_to_gene_id[gene_synonym])
    # keep statistic on the number of gene IDs that are associated to each synonym
    if number_of_ids not in gene_ids_per_ambiguous_synonym:
        gene_ids_per_ambiguous_synonym[number_of_ids] = 0
    gene_ids_per_ambiguous_synonym[number_of_ids] += 1
    # only gene synonyms associated to more than one gene ID are considered in the output
    if number_of_ids > 1:
        f_out.write(gene_synonym + "\t" + "|".join(synonym_to_gene_id[gene_synonym]) + "\n")
        count_ambiguous+=1
        # add the gene IDs to a list of ambiguous gene IDs
        for gene_id in synonym_to_gene_id[gene_synonym]:
            if gene_id not in ambiguous_gene_list.keys():
                ambiguous_gene_list[gene_id] = 1
    else:
        count_non_ambiguous+=1

# Write an output table with the statistics on number of gene IDs per synonym
print("Writing synonym counts to " + results_file + "...")
f_out = open(results_file, "w")
f_out.write("Synonym count\tNumber of genes\n")
for i in range(1,max(gene_ids_per_ambiguous_synonym.keys())+1):
    if i in gene_ids_per_ambiguous_synonym.keys():
        count = gene_ids_per_ambiguous_synonym[i]
    else:
        count = 0
    f_out.write(str(i) + "\t" + str(count) + "\n")

print("Genes with ambiguous synonyms: " + str(len(ambiguous_gene_list.keys())))
