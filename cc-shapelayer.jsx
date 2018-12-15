/*
#www.lasselauch.com/lab/
#Use at your own risk
*/

function createCClayer(){
  app.beginUndoGroup('create-cc-layer');
  var comp = app.project.activeItem;

  if (comp != null){
      if (comp instanceof CompItem) {
          layers = comp.layers;
          sel_layer = comp.selectedLayers.pop();
      }
  }else {return write("No Comp selected.");}

  var size_expression = """x = thisComp.width; y = thisComp.height; [x,y]"""
  var pos_expression = """x = thisComp.width/2; y = thisComp.height/2; [x,y]"""

  oShape = layers.addShape();
  if (sel_layer){oShape.moveBefore(sel_layer);}
  oShape.name = ("CC");
  oShape.adjustmentLayer = true;

  shapeGroup = oShape.property("Contents").addProperty("ADBE Vector Group");
  var myRect = shapeGroup.property("Contents").addProperty("ADBE Vector Shape - Rect");
  var myFill = shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Fill");
  shapeGroup.property("Contents").property("ADBE Vector Shape - Rect").property("Size").expression = size_expression;
  oShape.property("Position").expression = pos_expression;

  app.endUndoGroup();

  }

createCClayer();
