#!/usr/bin/python
from __future__ import print_function
import sys
import re
import json

def main(argv):
    descriptor = argv[0]
    pdb = argv[1]
    mc_filepath = argv[2]

    with open(mc_filepath, 'r') as mc_file:
        mc_content = mc_file.read()

    motifs = tokenize_motif(mc_content)

    motifs_data = []
    for motif in motifs:
        residues = getResidueConformation(motif)
        interactions = getInteractions(motif)

        if len(residues) == 0:
            print("Unexpected residues specification. Skipping motif.", file=sys.stderr)
            continue

        motifs_data.append({
            'descriptor': descriptor,
            'pdb': pdb,
            'residues': residues,
            'interactions': interactions
        })

    print(json.dumps(motifs_data, indent=2, sort_keys=True))

def tokenize_motif(mc_content):
    motifs = re.findall(r"(Residue conformations -+.+?)((?=Residue conformations)|(?=$))", mc_content, re.DOTALL)
    motifs = [x[0] for x in motifs]
    return motifs

def getResidueConformation(motif):
    searchObj = re.match(r'^Residue conformations -+(.*)\nAdjacent stackings -+', motif, re.DOTALL)
    residues_string = searchObj.group(1)

    searchObj = re.findall(r'^\'?(\w)\'?(\d+) : (\w) (\w+) (\w+)$', residues_string, re.MULTILINE)
    res_conf = [{
        'molecule': x[0],
        'position': x[1],
        'residue': x[2],
        'conf': x[3],
        'orient': x[4]
    } for x in searchObj]

    return res_conf

def getInteractions(motif):
    searchObj = re.search(r'\nAdjacent stackings -+\n*(.*?)\nNon-Adjacent stackings', motif, re.DOTALL)
    adj_stacking_string = searchObj.group(1)
    searchObj = re.findall(r'^\'?(\w)\'?(\d+)-\'?(\w)\'?(\d+) : (\w+) (\w+)', adj_stacking_string, re.MULTILINE)
    adj_stack = [{
        'molecule_start': x[0],
        'position_start': x[1],
        'molecule_end': x[2],
        'position_end': x[3],
        'stack_mode': x[4],
        'orient': x[5]
    } for x in searchObj]

    searchObj = re.search(r'\nNon-Adjacent stackings -+\n*(.*?)\nNumber of stackings', motif, re.DOTALL)
    nadj_stacking_string = searchObj.group(1)
    searchObj = re.findall(r'^\'?(\w)\'?(\d+)-\'?(\w)\'?(\d+) : (\w+) (\w+)?', nadj_stacking_string, re.MULTILINE)
    nadj_stack = [{
                     'molecule_start': x[0],
                     'position_start': x[1],
                     'molecule_end': x[2],
                     'position_end': x[3],
                     'orient': x[4],
                 } for x in searchObj]

    searchObj = re.search(r'\nBase-pairs -+\n*(.*?)$', motif, re.DOTALL)
    base_pairs_string = searchObj.group(1)
    searchObj = re.findall(r'^\'?(\w)\'?(\d+)-\'?(\w)\'?(\d+) : (\w)-(\w) (.+)$', base_pairs_string, re.MULTILINE)
    base_pairs = [{
                     'molecule_start': x[0],
                     'position_start': x[1],
                     'molecule_end': x[2],
                     'position_end': x[3],
                     'residue_1': x[4],
                     'residue_2': x[5],
                     'type': x[6].rstrip()
                 } for x in searchObj]

    interactions = {
        'adjacent_stacking': adj_stack,
        'non_adjacent_stacking': nadj_stack,
        'base_pairs': base_pairs
    }
    return interactions

if __name__ == "__main__":
    main(sys.argv[1:])