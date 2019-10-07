# One sense per citation network

Scripts to analyze the meaning of ambiguous names across citations

For the main analysis the order of execution of the scripts is the following, first:

* *read_ambiguous_gene_annotation_synonyms.py*

Then one of these scripts:

* *read_gene_annotations_uniprot.py*
* *read_gene_annotations_gene2pubmed.py*
* *read_gene_annotations_goa.py*
* *read_mesh_annotations.py*

Then:

* *filter_records_with_ambiguous_annotation.py*

Then one of these scripts:

* *connect_citing_articles.py*: for the first degree network
* *connect_citing_articles.py pmid_citations_shuffled.txt*: for the shuffled network
* *connect_citing_articles.py ./pmid_citations_second_degree.txt*: for the second degree network

Finally:

* *semantic_permanence.py*: annotation ambiguity analysis

* *add_title_and_abstract.py*

* *semantic_permanence_names.py*: mention ambiguity analysis

To predict ambiguous annotations:

* *add_title_and_abstract2.py*
* *filter_by_mention.py*: select pairs of connected PMIDs that share ambiguous mentions
* *disambiguator.py*: count annotations in the neighborhood of a record with an ambiguous mention

To expand large networks to second degree neighbors:

* *sort_citations.py*
* *expand_citations.py*

Additional files:

* *create_second_degree_network.py*: creates the second-degree citation network
* *create_shuffled_network.py*: creates a shuffled version of the original network
* *download_citations.sh*: download citations from the Open Citation Index
* *download_gene2pubmed.sh*: download the gene2pubmed database
* *download_goa.sh*: download the Gene Ontology Annotation database
* *download_ncbi_gene.sh*: download the NCBI Gene database
* *download_pmid_doi_mapping.sh*: download the PMID-PMC-DOI mappings from EBI
* *download_uniprot.sh*: download the UniProtKB annotations
* *map_doi_citations_to_pmid*: map citation pairs in DOI format to PMID using the EBI mapping data
* *top_mismatching_gene_annotations*: lists the gene annotations associated to most mismatching pairs
* *top_mismatching_mesh_annotations*: lists the MeSH annotations associated to most mismatching pairs
