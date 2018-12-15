/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

(function() {
    try {
        app.beginUndoGroup("Add selected PreComps to RenderQueue");
        var comp = app.project.activeItem;
        var layers = comp.selectedLayers;
        var numLayers = layers.length;
        for (var l = 0; l < numLayers; l++) {
            var layer = layers[l];
            if (layer.source instanceof CompItem){
                app.project.renderQueue.items.add(layer.source);}
        }
    } catch(err) {
        alert(err);
    } finally {
        app.project.renderQueue.showWindow(true);
        app.endUndoGroup();
    }
})();
