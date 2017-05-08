//https://bl.ocks.org/mbostock/3750558
function drawCycle(motif) {

    //Set the SVG drawing area
    var width = 400,
    height = 400;

    //Each residue is a node
    var nodes = motif.residues;

    //Set initial position to residues to lower the chance of links being tangled
    nodes[0].x = width/2;
    nodes[0].y = height/2;
    nodes[1].x = width/2 + 5;
    nodes[1].y = height/2;
    nodes[2].x = width/2 + 5;
    nodes[2].y = height/2 + 5;
    if (nodes.length > 3) {
        nodes[3].x = width/2;
        nodes[3].y = height/2 + 5;
    }

    var links = getLinks();

    //Prepare force layout that will display the graph
    var force = d3.layout.force()
        .size([width, height])
        .charge(-2000)
        .linkDistance(80)
        .on("tick", tick);

    //Allow dragging the nodes manually
    var drag = force.drag()
        .on("dragstart", dragstart);


    //Prepare the SVG area
    d3.select("#chart").select("svg").remove();
    var svg = d3.select("#chart").append("svg")
        .attr("width", width)
        .attr("height", height);

    //Prepare a black arrow markey to clearly identify backbone links between residues
    var my_defs = svg.append("svg:defs");

    my_defs.append("svg:marker")
        .attr("id", "marker_backbone")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 5)
        .attr("markerWidth", 4)
        .attr("markerHeight", 4)
        .attr("orient", "auto")
      .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");


    var link = svg.selectAll(".link"),
        node = svg.selectAll(".node");

    force.nodes(nodes)
      .links(links)
      .start();

    link = link.data(links)
        .enter().append("polyline")
        .attr("class", function(p){return "link" + " " + p.class;})
        .on("mouseover", function (d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", 1);
            tooltip.html("<b>" + d.type + "</b><br/>" +
                         d.desc)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function (d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });

    node = node.data(nodes)
        .enter().append("svg:g")
        .attr("class", "node");

    node.append("circle")
        .attr("r", 25);

  //Position
    node.append("text")
        .attr("class", "pos_text")
        .attr("dx", function(d){return -15    ;})
        .attr("dy", function(d){return -5;})
        .text(function(p){return "'" + p.molecule + "'" + p.position;});

  //Residue
    node.append("text")
        .attr("class", "res_text")
        .attr("dx", function(d){return -5;})
        .attr("dy", function(d){return 10;})
        .text(function(p){return p.residue;});



    node.append("circle")
        .attr("r", 25)
        .style("fill", "none")
        .style("pointer-events", "all")
        .on("mouseover", function (d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", 1);
            tooltip.html("<b>Residue '" + d.molecule + "'" + d.position + ":</b>"
                + "<br/>Configuration: " + d.conf
                + "<br/>Orientation: " + d.orient)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function (d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("dblclick", dblclick)
      .call(drag);

    function tick(e) {
        node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";});

    link.attr("points", function(d) {
      return d.source.x + "," + d.source.y + " " +
             (d.source.x + d.target.x)/2 + "," + (d.source.y + d.target.y)/2 + " " +
             d.target.x + "," + d.target.y; });

    }

    function dblclick(d) {
        d3.select(this).classed("fixed", d.fixed = false);
    }

    function dragstart(d) {
        d3.select(this).classed("fixed", d.fixed = true);
    }



    function getLinks() {
         var links = [];

        //Establish backbone links
        for(var i=0; i<nodes.length; i++) {
            for (var j=i+1; j<nodes.length; j++) {
                res1 = nodes[i];
                res2 = nodes[j];

                res1_pos = parseInt(res1.position);
                res2_pos = parseInt(res2.position);

                if (res1.molecule == res2.molecule){
                    if (res2_pos == (res1_pos + 1) || res1_pos == (res2_pos + 1)) {
                        links.push({"source": i, "target": j, "type": "backbone", "desc": "", "class": "linkL"});
                    }
                }

            }
        }

        //Establishing stacking links
        for (var nas_idx in motif.interactions.non_adjacent_stacking) {
            var nas = motif.interactions.non_adjacent_stacking[nas_idx];

            idx_start = nodes.findIndex(x => (x.position==nas.position_start) && (x.molecule == nas.molecule_start));
            idx_end = nodes.findIndex(x => (x.position==nas.position_end) && (x.molecule == nas.molecule_end));

            links.push({"source": idx_start, "target": idx_end, "type": "non-adjacent stacking", "desc": nas.orient, "class": "linkNAS"});
        }

        for (var as_idx in motif.interactions.adjacent_stacking) {
            var as = motif.interactions.adjacent_stacking[as_idx];

            idx_start = nodes.findIndex(x => (x.position==as.position_start) && (x.molecule == as.molecule_start));
            idx_end = nodes.findIndex(x => (x.position==as.position_end) && (x.molecule == as.molecule_end));

            links.push({"source": idx_start, "target": idx_end, "type": "adjacent stacking", "desc": as.orient, "class": "linkAS"});
        }

        //Establishing base-pairing links
        for (var bp_idx in motif.interactions.base_pairs) {
            var bp = motif.interactions.base_pairs[bp_idx];

            idx_start = nodes.findIndex(x => (x.position==bp.position_start) && (x.molecule == bp.molecule_start));
            idx_end = nodes.findIndex(x => (x.position==bp.position_end) && (x.molecule == bp.molecule_end));

            links.push({"source": idx_start, "target": idx_end, "type": "base-pairing", "desc": bp.type, "class": "linkP"});
        }
        return links;
    }

}