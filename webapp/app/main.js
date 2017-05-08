var hot_motifs;
var motifs;

var pdbs = psyclic_db().distinct("pdb");
var descriptors = psyclic_db().distinct("descriptor");

pdbs.unshift(null);
descriptors.unshift(null);

d3.select('#query_descriptor').selectAll("option").data(descriptors).enter().append("option").attr("value", function(p){return p;}).text(function(p){return p;});
d3.select('#query_pdb').selectAll("option").data(pdbs).enter().append("option").attr("value", function(p){return p;}).text(function(p){return p;});

// add the tooltip area to the webpage
    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 1)
        .style("position", "absolute")
        .style("opacity", 0);

update();



function update() {
    prepareData();
    updateMotifsCount();
    drawHandsOnTable(motifs);
    drawCycle(motifs[0]);
}



function prepareData() {
    //Filter data
    var filters = [];

    selected_pdb = d3.select('#query_pdb').property("value");
    if (selected_pdb) {
        filters.push({pdb: selected_pdb});
    }

    selected_descriptor = d3.select('#query_descriptor').property("value");
    if (selected_descriptor) {
        filters.push({descriptor: selected_descriptor});
    }

    motifs = psyclic_db.apply(this, filters).get();
}


function updateMotifsCount() {
    d3.select("#nb_motifs").text(motifs.length);
}


function drawHandsOnTable(pData) {
    hot_motifs = new Handsontable(document.getElementById('grid_container'), {
        data: pData,

        columns: [
            {data: 'pdb', width: 100, renderer: highlightingTextRenderer},
            {data: 'descriptor', width: 150, renderer: highlightingTextRenderer},
            {data: function(p){return p.residues.reduce(function(acc, val){acc.push(val.position); return acc;}, []).join();}, width: 350, renderer: highlightingTextRenderer},
            {data: 'type', width: 250, renderer: highlightingTextRenderer},
        ],

        colHeaders: ['PDB', 'Descriptor', 'Residues', 'Motif Type'],

        rowHeaders: true,
        multiSelect: false,

        afterSelection: function (r1, c1, r2, c2) {
            motif = this.getSourceDataAtRow(r1);
            this.render();

            drawCycle(motif);
        },

        height: 400
    });
}