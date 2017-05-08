![RNA-Psyclic](img/rna-psyclic.png)

# RNA-Psyclic

RNA-Psyclic is a cyclic motifs detection pipeline, making use of [MC-Search](http://www.major.iric.ca/wiki/index.php/MC-Search_%28english_version%29) and [MC-Annotate](http://major.iric.ca/MajorLabEn/MC-Tools.html), and producing a nice HTML visualization interface. It's basically your psychic to spot RNA cyclic motifs in multiple PDBs.

It takes two things in input:

* A set of PDB files: Holds molecules structural information. Motifs will be searched on these.
* A set of descriptor files: Describes the motif that we're looking for in the molecules.

## Usage


### Detecting motifs

* Place your motif descriptor files in the ```motif``` directory
* Place your PDB files in the ```pdb``` directory
* From the project root directory, launch the pipeline with the following command:

```
python ./rna-psyclic.py
```

What will happen goes as follow:

* RNA-Psyclic runs MC-Search on all PDB files, using all descriptors. It produces PDB files containing the list of motifs detected for a descriptor.
* Motifs PDBs are fed to MC-Annotate, that will infer residue interactions composing the cycles.
* The output of MC-Annotate is then converted to JSON documents, one per PDB-descriptor combination.
* All JSON are collated into one big JSON database.
* A string describing the cyclic motif type is computed, when possible.
* The final JSON database is moved to the webapp directory.

It is then possible to visualize the results in the web application.

### Using the web application

* Go to the webapp folder, and start Python's SimpleHTTPServer:
```
cd webapp
python -m SimpleHTTPServer
```

* Open your web browser to the provided URL, such as: ```http://127.0.0.1:8000/```. From there, you can then explore the JSON database.  

* It's possible to re-execute the pipeline by adding more motifs and PDB files in their respective folders. Re-launching the pipeline will only compute what's missing, instead of redoing everything.


## Scripts

The following scripts have been developed for RNA-Psyclic:

### rna-psyclic.py

The main pipeline execution script, builds a JSON database of motifs defined in ```motif``` folder, for PDB files provided in ```pdb``` folder.

### mc-annotate_to_json.py

Converts the output of MC-Annotate to a JSON document.

### merge_json.py

Merges all motif descriptor/PDB JSONs in the folder structure produced by rna-psyclic.py.

### set_motif_type.py

Attempts to compute a cycle type string, as suggested in *Lemieux-Major 2006*. (L=Link, P=Pair, S=Stack)


## Future plans

* Running multiple instances of MC-Search by providing a number of threads with the parameter ```--threads```
* Detecting errors in provided descriptor files, by flagging if there is found motifs that could be broken into smaller pieces. 

