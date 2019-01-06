/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

(function() {
    try {
      app.beginUndoGroup("Stretch and Sequence Layer");
      var comp = app.project.activeItem;
      var s = comp.selectedLayers;
      if (s == null || s.length == 0) {
        return;
      }

      // Stretch-Layers
      var stretchVal = prompt("Stretch-Factor: ( % ) ", 100);
      for (var i = 0; i < s.length; i++) {
        s[i].stretch = stretchVal;
      }

      //Handle Sequencing
      for (var i = 0; i < s.length; i++) {
        var base = comp.time;

        // Diff
        if (s[i].startTime != s[i].inPoint) {
          diff = s[i].inPoint - s[i].startTime;
        } else if (s[i].startTime == s[i].inPoint) {
          diff = 0;
        }

        s[i].startTime -= s[i].inPoint;
        s[0].startTime = comp.time;
        // Move
        if (i != 0) {
          v = s[i - 1].outPoint;
          s[i].startTime = ((base - diff) + v) - comp.time;
        }
      }
  } catch (err) {
    alert(err);
  } finally {
    app.endUndoGroup();
  }
})();
