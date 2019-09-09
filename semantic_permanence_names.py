#!/usr/bin/python3

# this script performs the ambiguous annotation analysis

import re

input_file = "connected_pmid_annotations_title_abstract.txt"
ambiguous_annotations_file = "ambiguous_names_and_annotations.txt"
output_file = "connected_pmid_annotations_title_abstract_ambiguous.txt"

# first it reads the annotation pairs that are considered to be ambiguous
f_in = open(ambiguous_annotations_file, "r")

ambiguous_annotation_pairs = {}
name_annotation = {}
for line in f_in:
    data = line[:-1].split("\t")
    name = data[0]
    annotations = data[1]
    for annotation1 in annotations.split("|"):
        if annotation1 in name_annotation.keys():
            name_annotation[annotation1].append(name)
        else:
            name_annotation[annotation1] = [name]
        for annotation2 in annotations.split("|"):
            if annotation1 != annotation2:
                if annotation1 not in ambiguous_annotation_pairs.keys():
                    ambiguous_annotation_pairs[annotation1] = [annotation2]
                else:
                    if annotation2 not in ambiguous_annotation_pairs[annotation1]:
                        ambiguous_annotation_pairs[annotation1].append(annotation2)

# then it reads all the pairs of records with at least an ambiguous annotation
print("Reading annotated citations...")
f_in = open(input_file, "r")
f_out = open(output_file, "w")
matching_counter = 0
mismatching_counter = 0
discard_citation_counter = 0
matched_counter = 0
discard_counter = 0
found1 = 0
mismatching_citation_pmids = set()
matching_citation_pmids = set()
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = data[0]
    annotations1 = data[1].split("|")
    pmid2 = data[2]
    annotations2 = data[3].split("|")
    title1 = data[4]
    abstract1 = data[5]
    title2 = data[6]
    abstract2 = data[7]
    matching_citation = 0
    mismatching_citation = 0
    discard_citation = 0
    matched = 0
    # for every pair of records it starts reading the annotations from one of them
    for annotation1 in annotations1:
        # checks if the annotation is ambiguous
        if annotation1 in ambiguous_annotation_pairs.keys():
            ambiguous_pairs_annotation1 = ambiguous_annotation_pairs[annotation1]
            # checks if the annotation also appears in the other record
            if annotation1 in annotations2:
                # if so then this is counted as a matching annotation
                self_ambiguous = 0
                for ambiguous_annotation in ambiguous_pairs_annotation1:
                    if ambiguous_annotation != annotation1:
                        if ambiguous_annotation in annotations2:
                            self_ambiguous = 1
                if self_ambiguous == 1:
                    discard_counter += 1
                else:
                    names = name_annotation[annotation1]
                    found1 = 0
                    for name in names:
                        if found1 == 0:
                            pattern = "\\b" + name.lower() + "\\b"
                            if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                                if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                    found1 = 1
                                    f_out.write("matching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation1 + "\n")
                                    matching_counter += 1
                                    matching_citation_pmids.add(pmid1)
                                    matching_citation_pmids.add(pmid2)
                self_ambiguous = 0
                for ambiguous_annotation in ambiguous_pairs_annotation1:
                    if ambiguous_annotation != annotation1:
                        if ambiguous_annotation in annotations1:
                            self_ambiguous = 1
                if self_ambiguous == 1:
                    discard_citation_counter += 1
                else:
                    names = name_annotation[annotation1]
                    found1 = 0
                    for name in names:
                        if found1 == 0:
                            pattern = "\\b" + name.lower() + "\\b"
                            if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                                if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                    found1 = 1
                                    f_out.write("matching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation1 + "\n")
                                    matching_counter += 1
                                    matching_citation_pmids.add(pmid1)
                                    matching_citation_pmids.add(pmid2)
    # nhen it looks for mismatches
    # for that first it looks at the annotation types for which the annotation is mutually ambiguous
    # then it checks if any of them exists in the other record (and not in the current record)
    for annotation1 in annotations1:
        found = 0
        if annotation1 in ambiguous_annotation_pairs.keys():
            if annotation1 not in annotations2:
                ambiguous_pairs_annotation1 = ambiguous_annotation_pairs[annotation1]
                for ambiguous_annotation in ambiguous_pairs_annotation1:
                    if ambiguous_annotation != annotation1:
                        if ambiguous_annotation in annotations2:
                            if ambiguous_annotation not in annotations1:
                                if found == 0:
                                   names1 = name_annotation[annotation1]
                                   names2 = name_annotation[ambiguous_annotation]
                                   for name in names1:
                                       if found == 0 and name in names2:
                                           pattern = "\\b" + name.lower() + "\\b"
                                           if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                                               if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                                   found = 1
                                                   f_out.write("mismatching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation1 + "\t" + ambiguous_annotation + "\n")
                                                   mismatching_counter += 1
                                                   mismatching_citation_pmids.add(pmid1)
                                                   mismatching_citation_pmids.add(pmid2)
    for annotation2 in annotations2:
        found = 0
        if annotation2 in ambiguous_annotation_pairs.keys():
            if annotation2 not in annotations1:
                ambiguous_pairs_annotation2 = ambiguous_annotation_pairs[annotation2]
                for ambiguous_annotation in ambiguous_pairs_annotation2:
                    if ambiguous_annotation != annotation2:
                        if ambiguous_annotation in annotations1:
                            if ambiguous_annotation not in annotations2:
                                if found == 0:
                                   names1 = name_annotation[annotation2]
                                   names2 = name_annotation[ambiguous_annotation]
                                   for name in names1:
                                       if found == 0 and name in names2:
                                           pattern = "\\b" + name.lower() + "\\b"
                                           if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                                               if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                                   found = 1
                                                   f_out.write("mismatching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation2 + "\t" + ambiguous_annotation + "\n")
                                                   mismatching_counter += 1
                                                   mismatching_citation_pmids.add(pmid1)
                                                   mismatching_citation_pmids.add(pmid2)

citation_counter = len(matching_citation_pmids.union(mismatching_citation_pmids))
print("Total records with matching and mismatching annotations: " + str(citation_counter))
matching_citation_counter = len(matching_citation_pmids)

print("==>Number of matching annotation pairs: " + str(matching_counter) + " (" + str(100 * matching_counter/(matching_counter + mismatching_counter)) + "%) based on " + str(matching_citation_counter) + " records")
mismatching_citation_counter = len(mismatching_citation_pmids)
print("==>Number of mismatching annotations pairs: " + str(mismatching_counter) + " (" + str(100 * mismatching_counter/(matching_counter + mismatching_counter)) + "%) based on " + str(mismatching_citation_counter) + " records")
print("Number of matching plus mismatching: " + str(matching_counter + mismatching_counter))

