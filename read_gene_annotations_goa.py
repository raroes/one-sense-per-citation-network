#!/usr/bin/python3

# this script reads annotations from the Gene Ontology Annotation (GOA) database

mapping_file = "./data/goa_human.gpi.gz"
input_file = "./data/goa_human.gpa.gz" 
output_file = "pmid_annotations.txt"
results_file = "annotation_counts_per_gene.txt"

import gzip
import re


# GOA annotations need to be mapped from UniProt IDs to NCBI Gene gene IDs
# first read the mappings
print("Processing GOA annotations")
print("Reading mappings...")

# open mappings file
f = gzip.open(mapping_file, 'rt')

gene_id_uniprot_id = {}
# read every line of the file
for line in f:
    line = line[:-1]
    data = line.split("\t")
    # only lines with gene ID information are parsed
    if len(data) > 6:
        uniprot_id = data[1]
        species_text = data[6]
        gene_text = data[8]
        # only entries for human genes are selected (species 9606)
        if re.search("\:9606",species_text):
            # only entries with human genes are selected
            if re.search("HGNC\:", gene_text):
                # read all gene ID values and create a Uniprot ID - NCBI Gene gene ID mapping dictionary
                matches = re.findall("[0-9]+", gene_text, re.DOTALL)
                for match in matches:
                    gene_id = match
                    if uniprot_id in gene_id_uniprot_id.keys():
                        gene_id_uniprot_id[uniprot_id].append(gene_id)
                    else:
                        gene_id_uniprot_id[uniprot_id] = [gene_id]

print("Reading annotations...")

# open the GOA annotations file
f = gzip.open(input_file, 'rt')

pmids_per_gene_id = {}
gene_ids_per_pmid = {}
gene_id_list = {}
total_annotations = 0
pmids = {}
# read every line of the file
for line in f:
    line = line[:-1]
    data = line.split("\t")
    # a line is only parsed if it has annotation information
    if len(data) > 3:
        uniprot_id = data[1]
        # check if the UniProt ID in the line can be mapped to a gene ID
        if uniprot_id in gene_id_uniprot_id.keys():
            gene_ids = gene_id_uniprot_id[uniprot_id]
            # for each gene ID mapped to the UniProt ID
            for gene_id in gene_ids:
                # read all PMIDs listed in the line
                pmid_text = data[4]
                if re.search("PMID\:", pmid_text):
                    pmid_list = re.findall("[0-9]+", pmid_text, re.DOTALL)
                    # create a dictionary relating PMIDs to each gene ID
                    for pmid in pmid_list:
                        pmids[pmid] = 1
                        # create a list of gene IDs
                        if gene_id not in gene_id_list.keys():
                            gene_id_list[gene_id] = 1
                        if gene_id not in pmids_per_gene_id:
                            pmids_per_gene_id[gene_id] = [pmid]
                            total_annotations += 1
                        else:
                            if pmid not in pmids_per_gene_id[gene_id]:
                                pmids_per_gene_id[gene_id].append(pmid)
                                total_annotations += 1
                        # create also the reverse dictionary of gene IDs and PMIDs
                        if pmid not in gene_ids_per_pmid:
                            gene_ids_per_pmid[pmid] = [gene_id]
                        else:
                            if gene_id not in gene_ids_per_pmid[pmid]:
                                gene_ids_per_pmid[pmid].append(gene_id)

print("Total (human) annotations: " + str(total_annotations))
print("Total number of genes with annotations: " + str(len(gene_id_list.keys())))
print("Total articles annotated: " + str(len(pmids.keys())))

print("Write statistics file...")
# count the number of PMIDs per gene ID
pmids_per_gene_id_count = {}
for gene_id in pmids_per_gene_id.keys():
   number_of_pmids = len(pmids_per_gene_id[gene_id])
   if number_of_pmids not in pmids_per_gene_id_count.keys():
       pmids_per_gene_id_count[number_of_pmids]=0
   pmids_per_gene_id_count[number_of_pmids]+=1

# write a file with the numbers computed
f_out = open(results_file, "w")
for i in range(1,max(pmids_per_gene_id_count.keys())+1):
    if i in pmids_per_gene_id_count.keys():
        count = pmids_per_gene_id_count[i]
    else:
        count = 0
    f_out.write(str(i) + "\t" + str(count) + "\n")

print("Writing output file...")

# Write output file with PMIDs and their annotations
f_out = open(output_file, "w")
for pmid in gene_ids_per_pmid.keys():
    f_out.write(pmid + "\t" + "|".join(gene_ids_per_pmid[pmid]) + "\n")

print("Finished writing output file.\n")
