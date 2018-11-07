/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

(function() {
    try {
        app.beginUndoGroup("Freeze Frame & Adjust Length to Comp");
        var comp = app.project.activeItem;
        var layers = comp.selectedLayers;
        var numLayers = layers.length;
        for (var l = 0; l < numLayers; l++) {
            var layer = layers[l];
            app.executeCommand(app.findMenuCommandId("Freeze Frame"));
            layer.inPoint = comp.displayStartTime;
            layer.outPoint = comp.duration;
        }
    } catch(err) {
        alert(err);
    } finally {
        app.endUndoGroup();
    }
})();
