#!/usr/bin/python
from __future__ import print_function
from Bio.PDB import PDBParser

parser = PDBParser()

structure = parser.get_structure('3cxc', './mcsearch/output/3cxc_model_1.pdb')
header = parser.get_header()
trailer = parser.get_trailer()

for model in structure:
    print('----------------------')
    print('Model %s' % model)
    for chain in model:
        for residue in chain:
            print(residue)
            # for atom in residue:
            #     print(atom)
