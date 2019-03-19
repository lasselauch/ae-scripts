/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

(function() {
    try {
        app.beginUndoGroup("Reload Footage and Outpoint");
        var comp = app.project.activeItem;
        var layers = comp.selectedLayers;
        var numLayers = layers.length;
        for (var l = 0; l < numLayers; l++) {
            var layer = layers[l];
            if (layer.source instanceof FootageItem) {
                layer.source.mainSource.reload();
                layer.outPoint = comp.duration;
            }
        }
    } catch (err) {
        alert(err);
    } finally {
        app.endUndoGroup();
    }
})();
