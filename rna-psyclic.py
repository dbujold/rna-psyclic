#!/usr/bin/python
from __future__ import print_function
import sys
import os
import subprocess
import glob
import re
from shutil import copyfile


def main(argv):
    pdbs = glob.glob('./pdb/*.pdb')
    descriptors = glob.glob('./motif/*')

    # Transform PDB list into accessors
    acc_re = re.compile('\/(\w+)\.pdb$')
    pdbs = [acc_re.search(x, re.IGNORECASE).group(1) for x in pdbs]

    # Clean descriptors
    descriptor_re = re.compile('\/(\w+)$')
    descriptors = [descriptor_re.search(x, re.IGNORECASE).group(1) for x in descriptors]
    descriptors.sort()

    print('%d PDB files: %s' % (len(pdbs), pdbs))
    print('%d descriptor files: %s' % (len(descriptors), descriptors))

    print('Running MC-Search... ')
    for descriptor in descriptors:
        output_dir = './output/' + descriptor
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filtered_pdbs = []
        for pdb in pdbs:
            if not os.path.exists(os.path.join(output_dir, pdb + '_model_1.pdb')):
                filtered_pdbs.append(pdb)

        if len(filtered_pdbs) == 0:
            print('  Descriptor %s : All done.' % descriptor)
        else:
            print('  Descriptor %s on PDBs %s' % (descriptor, filtered_pdbs))
            sys.stdout.flush()

            pdb_files = ['../../pdb/'+x+'.pdb' for x in filtered_pdbs]
            subprocess.call(['../../mcsearch', '../../motif/' + descriptor] + pdb_files, cwd=output_dir)

            for pdb in filtered_pdbs:
                gz_file = os.path.join(output_dir, pdb + '_model_1.pdb.gz')
                if os.path.isfile(gz_file):
                    subprocess.call(['gunzip', '-f', gz_file])


    print('Running MC-Annotate...')
    for descriptor in descriptors:
        print('  Descriptor %s' % descriptor)
        sys.stdout.flush()

        wdir = './output/' + descriptor + '/'

        for pdb in pdbs:
            in_filename = pdb + '_model_1.pdb'
            out_filename = pdb + '_annotations'

            f = open(wdir + out_filename, "w")
            if os.path.isfile(wdir + in_filename):
                subprocess.call(['../../MC-Annotate', in_filename], cwd=wdir, stdout=f)
            f.close()


    print('Converting MC-Annotate output to JSON...')
    for descriptor in descriptors:
        print('  Descriptor %s' % descriptor)
        sys.stdout.flush()

        wdir = './output/' + descriptor + '/'

        for pdb in pdbs:
            in_filename = pdb + '_annotations'
            out_filename = pdb + '.json'

            f = open(wdir + out_filename, "w")
            subprocess.call(['python', '../../mc-annotate_to_json.py', descriptor, pdb, in_filename], cwd=wdir, stdout=f)


    print('Collating motif/PDB JSON to a single JSON...')
    merged_file = os.path.join('./output/', 'psyclic_db_temp.json')
    f = open(merged_file, "w")
    subprocess.call(['python', './merge_json.py'], stdout=f)
    f.close()

    print('Generating motifs type...')
    final_json_file = os.path.join('./output/', 'psyclic_db.json')
    f = open(final_json_file, "w")
    subprocess.call(['python', './set_motif_type.py', merged_file], stdout=f)
    f.close()

    copyfile("./output/psyclic_db.json", "./webapp/json/psyclic_db.json")
    print('Motifs database generated. You can now results by starting the web application in a browser.')


if __name__ == "__main__":
    main(sys.argv[1:])