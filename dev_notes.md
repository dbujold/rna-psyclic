## MC-Search usage

* Step 1: Identify motives in desired structure
Example for identifying all 7 nt loops:
```
cd output
../mcsearch -r ../motif/loop7.txt ../pdb/3cxc.pdb
gunzip 3cxc_model_1.pdb
```

* Step 2: Convert the output PDB into a structure database
```
../parse_pdb.py 
```




* MC-Annotate
```
../MC-Annotate -f 150 ./3cxc_model_1.pdb > 3cxc_annotations.txt
../mc-annotate_to_json.py 3cxc_annotations.txt
```



http://rna.bgsu.edu/rna3dhub/nrlist





http://www.major.iric.ca/wiki/index.php/MC-Search