#!/usr/bin/python3

# this script reads the BioCreative 2 Gene Normalization task annotations

# this input file is a combination of the train and testing files
input_file = "./data/bc2_gene_annotations.txt"
output_file = "pmid_annotations.txt"
results_file = "annotation_counts_per_gene.txt"

print("Processing BC2GN annotations")

import gzip

# open BC2GN annotations file
f = open(input_file, 'r')

pmids_per_gene_id = {}
gene_ids_per_pmid = {}
gene_id_list = {}
total_annotations = 0
pmids = {}
print("Reading annotations...")
# read all entries in the file
for line in f:
    line = line[:-1]
    data = line.split("\t")
    gene_id = data[1]
    pmid = data[0]
    # create a list of PMIDs
    pmids[pmid] = 1
    # create a list of gene IDs
    if gene_id not in gene_id_list.keys():
        gene_id_list[gene_id] = 1
    # create a dictionary of PMIDs annotated by each gene ID
    if gene_id not in pmids_per_gene_id:
        pmids_per_gene_id[gene_id] = [pmid]
        total_annotations += 1
    else:
        if pmid not in pmids_per_gene_id[gene_id]:
            pmids_per_gene_id[gene_id].append(pmid)
            total_annotations += 1
    # create a dictionary of gene IDs annotating each PMID
    if pmid not in gene_ids_per_pmid:
        gene_ids_per_pmid[pmid] = [gene_id]
    else:
        if gene_id not in gene_ids_per_pmid[pmid]:
            gene_ids_per_pmid[pmid].append(gene_id)

print("Total (human) annotations: " + str(total_annotations))
print("Total number of genes with annotations: " + str(len(gene_id_list.keys())))
print("Total articles annotated: " + str(len(pmids.keys())))

print("Writing annotation statistics...")
# count the number of PMIDs for each gene ID
pmids_per_gene_id_count = {}
for gene_id in pmids_per_gene_id.keys():
   number_of_pmids = len(pmids_per_gene_id[gene_id])
   if number_of_pmids not in pmids_per_gene_id_count.keys():
       pmids_per_gene_id_count[number_of_pmids]=0
   pmids_per_gene_id_count[number_of_pmids]+=1

# write as output the counts computed
f_out = open(results_file, "w")
for i in range(1,max(pmids_per_gene_id_count.keys())+1):
    if i in pmids_per_gene_id_count.keys():
        count = pmids_per_gene_id_count[i]
    else:
        count = 0
    f_out.write(str(i) + "\t" + str(count) + "\n")

print("Writing output file...")
# write as output file each PMID with its annotations
f_out = open(output_file, "w")
for pmid in gene_ids_per_pmid.keys():
    f_out.write(pmid + "\t" + "|".join(gene_ids_per_pmid[pmid]) + "\n")

print("Finished writing output file.\n")
