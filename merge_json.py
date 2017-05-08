#!/usr/bin/python
from __future__ import print_function
import sys
import os
import subprocess
import glob
import re
import json


def main(argv):
    pdbs = glob.glob('./pdb/*.pdb')
    descriptors = glob.glob('./motif/*')

    #Transform PDB list into accessors
    acc_re = re.compile('\/(\w+)\.pdb$')
    pdbs = [acc_re.search(x, re.IGNORECASE).group(1) for x in pdbs]

    #Clean descriptors
    descriptor_re = re.compile('\/(\w+)$')
    descriptors = [descriptor_re.search(x, re.IGNORECASE).group(1) for x in descriptors]
    descriptors.sort()

    mega_json = []
    for descriptor in descriptors:
        for pdb in pdbs:
            file_path = './output/' + descriptor + '/' + pdb + '.json'
            json_data = open(file_path).read()
            data = json.loads(json_data)

            # mega_json.setdefault(descriptor, {})[pdb] = data
            mega_json += data

    print(json.dumps(mega_json, indent=2, sort_keys=True))

if __name__ == "__main__":
    main(sys.argv[1:])