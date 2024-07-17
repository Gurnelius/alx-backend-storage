#!/usr/bin/env python3

import sys
import os

# Function to extract filenames and content
def create_filenames(filename, lines):
    '''
    Create filenames and content
    '''
    for line in lines:
        if "File:" in line:
            filename = line.split()[-1]
            with open(filename, "w") as file:
                # file.write("#!/usr/bin/node\n")
                pass

# Check if file name is provided as argument
if len(sys.argv) != 2:
    print("Usage: {} <filename>".format(sys.argv[0]))
    sys.exit(1)

# Get the file name from command line argument
filename = sys.argv[1]

# Check if file exists
if not os.path.isfile(filename):
    print("File not found:", filename)
    sys.exit(1)

# Read the content of the file
with open(filename, "r") as file:
    lines = file.readlines()

# Extract filenames and content
create_filenames(filename, lines)

