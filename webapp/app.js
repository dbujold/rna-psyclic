requirejs.config({
    baseUrl: './',
    paths: {
        app: 'app',
        text: 'lib/text',
        json: 'lib/json'
    },
    urlArgs: "bust=" + (new Date()).getTime()   //Solve caching problem during development: http://stackoverflow.com/questions/8315088/prevent-requirejs-from-caching-required-scripts
});

//Load datasets accession numbers database
var psyclic_db;
requirejs(["lib/d3.v3.min",
    "lib/taffy-min",
    "app/hot_renderers",
    "app/cycle_viewer",
    "json!/json/psyclic_db.json"
], function (d3, taffy, hot_renderers, cycle_viewer, db) {

    console.log("Loaded D3 version " + d3.version);
    console.log("Loaded TaffyDB");
    console.log("Loaded custom Handsontable renderers");

    psyclic_db = TAFFY(db);

    requirejs(['app/main']);
});



