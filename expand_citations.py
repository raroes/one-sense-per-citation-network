#!/usr/bin/python3

# this script creates a second degree network using the citation data
input_file = "pmid_citations_sorted.txt"
output_file = "pmid_citations_second_degree.txt"

#input_file = "temp_output.txt"
#output_file = "temp_output2.txt"

# first, all citations are read
# a dictionary is created in which each PMID is associated to all its first-degree neighbors
print("Reading input file...")
f_in = open(input_file, "r")
pmid_neighbors = {}
counter = 0
for line in f_in:
    counter += 1
    if counter / 1000000 == int(counter / 1000000):
        print("Read " + str(counter) + " lines.")
    data = line[:-1].split("\t")
    pmid1 = int(data[0])
    pmid2 = int(data[1])
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
f_out = open(output_file, "w")
counter = 0
lines_written = 0
old_pmid = 0
output = {}
for line in f_in:
    counter += 1
    if counter / 100000 == int(counter / 100000):
        print("Read " + str(counter) + " lines.")
    data = line[:-1].split("\t")
    pmid1 = int(data[0])
    pmid2 = int(data[1])
    if pmid1 != old_pmid:
        already_out = {}
        old_pmid = pmid1
    #if int(pmid1) < int(pmid2):
        #if pmid2 not in already_out.keys():
            #already_out[pmid2] = 1
            # write out the connection itself
            ###f_out.write(str(pmid1) + "\t" + str(pmid2) + "\n")
            ###lines_written += 1
    # check all possible neighbors of the second PMID
    if pmid2 in pmid_neighbors.keys():
        for pmid in pmid_neighbors[pmid2]:
            if pmid not in already_out.keys():
                if pmid1 < pmid: 
                    already_out[pmid] = 1
                    f_out.write(str(pmid1) + "\t" + str(pmid) + "\n")
                    lines_written += 1

print("Lines read: " + str(counter))
print("Lines written: " + str(lines_written))
