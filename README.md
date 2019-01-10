# One sense per citation network

## Scripts to analyze the meaning of ambiguous names across citations

### For the main analysis the order of execution of the scripts is the following, first:

### read_ambiguous_gene_annotations_synonyms.py

#### Then one of these scripts:

### * *read_gene_annotations_uniprot.py*
### * *read_gene_annotations_gene2pubmed.py*
### * *read_gene_annotations_goa.py*
### * *read_gene_annotations_bc2.py*

#### Then:

### * *filter_pubmed_records_with_annotation.py*

#### Then one of these scripts:

### * *link_citing_articles.py*: for the first degree network
### * *link_citing_articles.py pmid_citations_shuffled.txt*: for the shuffled network
### * *link_citing_articles.py ./pmid_citations_second_degree.txt*: for the second degree network

#### Finally:

### * *semantic_permanence.py*: annotation ambiguity analysis

### * *add_title_and_abstract.py*

### * *semantic_permanence_names.py*: mention ambiguity analysis
