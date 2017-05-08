var highlightingTextRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    var selected_row = instance.getSelected();
    if ((typeof selected_row !== 'undefined') && (selected_row[0] === row)) {
        td.className = 'hotSelectedCell';
    }
};

var highlightingNumericRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    var selected_row = instance.getSelected();
    if ((typeof selected_row !== 'undefined') && (selected_row[0] === row)) {
        td.className = 'hotSelectedCell';
    }
};