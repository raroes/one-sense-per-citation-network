#!/usr/bin/python3

# this script performs the ambiguous annotation mention analysis

import re

input_file = "connected_pmid_annotations_title_abstract.txt"
ambiguous_annotations_file = "ambiguous_names_and_annotations.txt"
output_file = "connected_pmid_annotations_title_abstract_ambiguous.txt" 
results_file = "total_annotations_per_match_type_mentions.txt"

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
output_counter = 0
matched_counter = 0
counter = 0
discard_counter = 0
matching_citation = 0
mismatching_citation = 0
matching_citation_counter = 0
mismatching_citation_counter = 0
matching_total_annotations = {}
mismatching_total_annotations = {}
discard_counter = 0
discard_citation_counter = 0
for line in f_in:
    counter += 1
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
        matching = 0
        mismatching = 0
        self_ambiguous = 0
        output_lines = ""
        # checks if the annotation is ambiguous
        if annotation1 in ambiguous_annotation_pairs.keys():
            ambiguous_pairs_annotation1 = ambiguous_annotation_pairs[annotation1]
            # checks if the annotation also appears in the other record
            if annotation1 in annotations2:
                # if so then this is counted as a matching annotation
                names = name_annotation[annotation1]
                found = 0
                for name in names:
                    if found == 0:
                        pattern = "[^\&^0-9^a-z^A-Z]" + name.lower() + "[^\&^0-9^a-z^A-Z]"
                        if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                            if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                found = 1
                                matching = 1
            # next it looks for mismatches
            # for that first it looks at the annotation types for which the annotation is mutually ambiguous
            # then it checks if any of them exists in the other record (and not in the current record)
            for ambiguous_annotation in ambiguous_pairs_annotation1:
                if ambiguous_annotation not in annotations1:
                    if ambiguous_annotation in annotations2:
                        names1 = name_annotation[annotation1]
                        names2 = name_annotation[ambiguous_annotation]
                        found = 0
                        for name in names1:
                            if found == 0 and name in names2:
                                pattern = "[^\&^0-9^a-z^A-Z]" + name.lower() + "[^\&^0-9^a-z^A-Z]"
                                if re.search(pattern, " " + title1.lower() + " ") or re.search(pattern, " " + abstract1.lower() + " "):
                                    if re.search(pattern, "  " + title2.lower() + " ") or re.search(pattern, "  " + abstract2.lower() + " "):
                                        found = 1
                                        # if those two conditions are met it is counted as a mismatch
                                        mismatching += 1
                                        # every mismatch is saved for output later
                                        output_lines = output_lines + "mismatching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation1 + "\t" + ambiguous_annotation + "\n"
            # make sure that there is no mutually ambiguous annotation in the same record
            for ambiguous_annotation in ambiguous_pairs_annotation1:
                if ambiguous_annotation in annotations1:
                    self_ambiguous = 1
            # if there is no mutually ambiguous annotation in the same record
            if self_ambiguous == 0:
                # if there is a matching pair but also a mismatching pair then these are all discarded
                if matching == 1:
                    if mismatching > 0:
                        discard_citation = 1
                        discard_counter += 1
                    else:
                        # but if not then a matching is called
                        matching_counter += 1
                        matching_citation = 1
                        matched = 1
                        # the matching goes to output to keep track of all matchings
                        f_out.write("matching" + "\t" + pmid1 + "\t" + pmid2 + "\t" + annotation1 + "\n")
                else:
                    # if there are no matchings and there are mismatchings then all mismatchings are counted and go to output
                    if mismatching > 0:
                        mismatching_counter += 1
                        mismatching_citation = 1
                        matched = 1
                        f_out.write(output_lines)
            else:
                discard_counter += 1
                discard_citation = 1
    # here statistics about record pairs containing matching and mismatching annotations are counted
    total_annotations = len(annotations1) + len(annotations2)
    if discard_citation == 1:
        discard_citation_counter += 1
    if matching_citation == 1:
        matching_citation_counter += 1
        if total_annotations in matching_total_annotations.keys():
            matching_total_annotations[total_annotations] += 1
        else:
            matching_total_annotations[total_annotations] = 1
    if mismatching_citation == 1:
        mismatching_citation_counter += 1
        if total_annotations in mismatching_total_annotations.keys():
            mismatching_total_annotations[total_annotations] += 1
        else:
            mismatching_total_annotations[total_annotations] = 1
    if matched == 1:
        output_counter += 1

# the statistics computed are written out in a results file
print("Writing results file " + results_file + "...")
f_out = open(results_file, "w")
for i in range(1,max(list(mismatching_total_annotations.keys()) + list(matching_total_annotations.keys()))+1):
    if i in mismatching_total_annotations.keys():
        mismatching_total_annotations_count = mismatching_total_annotations[i]
    else:
        mismatching_total_annotations_count = 0
    if i in matching_total_annotations.keys():
        matching_total_annotations_count = matching_total_annotations[i]
    else:
        matching_total_annotations_count = 0
    f_out.write(str(i) + "\t" + str(matching_total_annotations_count) + "\t" + str(mismatching_total_annotations_count) + "\n")

print("Number of unique citations matched / mismatched: " + str(output_counter))
print("==>Number of matching annotation pairs: " + str(matching_counter) + " (" + str(100 * matching_counter/(matching_counter + mismatching_counter)) + "%) based on " + str(matching_citation_counter) + " citations")
print("==>Number of mismatching annotations pairs: " + str(mismatching_counter) + " (" + str(100 * mismatching_counter/(matching_counter + mismatching_counter)) + "%) based on " + str(mismatching_citation_counter) + " citations")
print("Number of matching plus mismatching: " + str(matching_counter + mismatching_counter))
print("Number of discarded citations: " + str(discard_citation_counter))

