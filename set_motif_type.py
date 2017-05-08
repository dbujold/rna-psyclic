#!/usr/bin/python
from __future__ import print_function
import sys
import os
import subprocess
import glob
import re
import json


def main(argv):
    file_path = argv[0]
    json_data = open(file_path).read()
    data = json.loads(json_data)


    for motif in data:
        try:
            graph = makeGraph(motif)
            graph_type = makeCycleString(motif, graph)
            motif['type'] = graph_type

        # print(json.dumps(graph, indent=2, sort_keys=True))
        # print('\n\n')
        except (KeyError, IndexError) as e:
            print('Warning: Possible cycle problem. (Descriptor "%s", PDB "%s", Position "%s")' % (motif['descriptor'], motif['pdb'], motif['residues'][0]['position']), file=sys.stderr)
            continue

    print(json.dumps(data, indent=2, sort_keys=True))


def makeCycleString(motif, graph):
    cyclic_graph = []

    first_res_key = make_key(motif['residues'][0])
    second_res_key = make_key(motif['residues'][1])
    last_res_key = make_key(motif['residues'][len(motif['residues']) - 1])

    str = ""
    if (first_res_key in graph) and (last_res_key in graph[first_res_key]):
        str += ''.join(graph[first_res_key][last_res_key])
    if (last_res_key in graph) and (first_res_key in graph[last_res_key]):
        str += ''.join(graph[last_res_key][first_res_key])
    cyclic_graph.append(str)

    str = ""
    if (first_res_key in graph) and (second_res_key in graph[first_res_key]):
        str += ''.join(graph[first_res_key][second_res_key])
    if (second_res_key in graph) and (first_res_key in graph[second_res_key]):
        str += ''.join(graph[second_res_key][first_res_key])
    cyclic_graph.append(str)

    for x in range(1, len(motif['residues']) - 1):
        str = ""
        key1 = make_key(motif['residues'][x])
        key2 = make_key(motif['residues'][x+1])

        if (key1 in graph) and (key2 in graph[key1]):
            str += ''.join(graph[key1][key2])
        if (key2 in graph) and (key1 in graph[key2]):
            str += ''.join(graph[key2][key1])
        cyclic_graph.append(str)

    return '-'.join(cyclic_graph)


def make_key(residue):
    key = residue['molecule'] + '-' + residue['position']
    return key


def makeGraph(motif):
    graph = {}

    residues = motif['residues']
    for i in range(0, len(residues)):
        for j in range(i, len(residues)):
            res1_pos = int(residues[i]['position']);
            res2_pos = int(residues[j]['position']);
            res1 = residues[i]['molecule'] + '-' + residues[i]['position']
            res2 = residues[j]['molecule'] + '-' + residues[j]['position']

            if residues[i]['molecule'] == residues[j]['molecule']:
                if (res2_pos == (res1_pos + 1)) or (res1_pos == (res2_pos + 1)):
                    graph.setdefault(res1, {})
                    graph[res1].setdefault(res2, [])
                    graph[res1][res2].append('L')

    base_pairs = motif['interactions']['base_pairs']
    for base_pair in base_pairs:
        res1 = base_pair['molecule_start'] + '-' + base_pair['position_start']
        res2 = base_pair['molecule_end'] + '-' + base_pair['position_end']
        graph.setdefault(res1, {})
        graph[res1].setdefault(res2, [])
        graph[res1][res2].append('P')

    na_stackings = motif['interactions']['non_adjacent_stacking']
    for na_stacking in na_stackings:
        res1 = na_stacking['molecule_start'] + '-' + na_stacking['position_start']
        res2 = na_stacking['molecule_end'] + '-' + na_stacking['position_end']
        graph.setdefault(res1, {})
        graph[res1].setdefault(res2, [])
        graph[res1][res2].append('S')

    #Kept separated in case we want to do more stuff that's adjacent stacking-specific
    a_stackings = motif['interactions']['adjacent_stacking']
    for a_stacking in a_stackings:
        res1 = a_stacking['molecule_start'] + '-' + a_stacking['position_start']
        res2 = a_stacking['molecule_end'] + '-' + a_stacking['position_end']
        graph.setdefault(res1, {})
        graph[res1].setdefault(res2, [])
        graph[res1][res2].append('S')

    return graph


if __name__ == "__main__":
    main(sys.argv[1:])