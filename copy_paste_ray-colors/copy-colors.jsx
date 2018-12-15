/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

#include './aeq/aequery.js' // aequery is now available as aeq

//You can download the latest version from *aequery* here:
//https://bitbucket.org/motiondesign/aequery/downloads

(function() {
  try {
    app.beginUndoGroup("Copy Colors to Clipboard");

    comp = aeq.activeComp()
    if (comp == null) {
      alert("Sorry, no Comp selected.");
      return;
    }

    var string = ""
    //Let's collect the Layer-Name as Swatch-Group-Name
    string += comp.layer(1).name + ";";

    var effects = aeq.getEffects(comp.layer(1));
    if (effects == null || effects.length === 0) {
      alert("Sorry, no Effects found.")
      return;
    }

    for (i = 0; i < effects.length; i++) {
      var c = effects[i].property("ADBE Color Control-0001");
      if (c == null) {
        return;
      }
      //Add Colors to String with ; as Divider
      string += String(c.value) + ";";
    }

    //Copy String to Clipboard
    aeq.copyToClipboard(string);
    alert('Copied: "' + comp.layer(1).name + '" to your Clipboard!')

  } catch (err) {
    alert(err);
  } finally {
    app.endUndoGroup();
  }
})();
