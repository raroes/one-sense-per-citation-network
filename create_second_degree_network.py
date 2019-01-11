#!/usr/bin/python3

# this script creates a second degree network using the citation data
input_file = "pmid_citations.txt"
temp_output_file = "temp_pmid_citations_second_degree.txt"
output_file = "pmid_citations_second_degree.txt"

# first, all citations are read
# a dictionary is created in which each PMID is associated to all its first-degree neighbors
print("Reading input file...")
f_in = open(input_file, "r")
pmid_neighbors = {}
counter = 0
for line in f_in:
    counter += 1
    if counter / 100000 == int(counter / 100000):
        print("Read " + str(counter) + " lines.")
    data = line[:-1].split("\t")
    pmid1 = data[0]
    pmid2 = data[1]
    # to eliminate redundancy, the first PMID is always the smaller value
    if int(pmid1) > int(pmid2):
        temp_pmid = pmid1
        pmid1 = pmid2
        pmid2 = temp_pmid
    # a dictionary of PMIDs and first-degree connections is created
    if pmid2 not in pmid_neighbors.keys():
        pmid_neighbors[pmid2] = [pmid1]
    else:
        pmid_neighbors[pmid2].append(pmid1)

print("Input file read")

# Then, citations are read once again
# each first-degree connection is substituted by a second-degree connection
# then they are written into a temp file that will be used in the next step
print("Reading input file again and writing output file " + output_file + "...")

f_in = open(input_file, "r")
f_out = open(temp_output_file, "w")
counter = 0
lines_written = 0
for line in f_in:
#for i in range(1,210000):
#    line = f_in.readline()
    counter += 1
    if counter / 100000 == int(counter / 100000):
        print("Read " + str(counter) + " lines.")
    data = line[:-1].split("\t")
    pmid1 = data[0]
    pmid2 = data[1]
    # order PMIDs by increasing value
    if int(pmid1) > int(pmid2):
        temp_pmid = pmid1
        pmid1 = pmid2
        pmid2 = temp_pmid
    # check all possible neighbors of the second PMID
    if pmid2 in pmid_neighbors.keys():
        for pmid in pmid_neighbors[pmid2]:
            if pmid != pmid1 and pmid != pmid2:
                f_out.write(pmid1 + "\t" + pmid + "\n")
                lines_written += 1
    # check all possible neighbors of the first PMID
    if pmid1 in pmid_neighbors.keys():
        for pmid in pmid_neighbors[pmid1]:
            if pmid != pmid1 and pmid != pmid2:
                f_out.write(pmid + "\t" + pmid2 + "\n")
                lines_written += 1

print("Lines read: " + str(counter))
print("Lines written: " + str(lines_written))

# this next step eliminates all redundant second-degree connections created in the previous step
pmid_neighbors = {}
print("Removing redundant entries...")

f_in = open(temp_output_file, "r")
f_out = open(output_file, "w")

lines_read = 0
lines_written = 0
pmid_read = {}
# read all connections created in the previous step
for line in f_in:
    data = line[:-1].split("\t")
    pmid1 = int(data[0])
    pmid2 = int(data[1])
    lines_read += 1
    # order PMIDs to simplify
    if pmid1 > pmid2:
        temp_pmid = pmid1
        pmid1 = pmid2
        pmid2 = temp_pmid
    # check if the connection has already been seen before
    # only if the connection is new it will be printed out
    if pmid1 not in pmid_read.keys():
        pmid_read[pmid1] = [pmid2]
        f_out.write(str(pmid1) + "\t" + str(pmid2) + "\n")
        lines_written += 1
    else:
        if pmid2 not in pmid_read[pmid1]:
            pmid_read[pmid1].append(pmid2)
            f_out.write(str(pmid1) + "\t" + str(pmid2) + "\n")
            lines_written += 1

print("Lines read: " + str(lines_read))
print("Lines written: " + str(lines_written))
