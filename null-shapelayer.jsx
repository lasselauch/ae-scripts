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

  oShape = layers.addShape();
  if (sel_layer){oShape.moveBefore(sel_layer);}
  oShape.name = ("Null");
  oShape.label = 2;

  shapeGroup = oShape.property("Contents").addProperty("ADBE Vector Group");
  shapeGroup.property("Contents").addProperty("ADBE Vector Shape - Rect");
  shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Fill");
  shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Stroke");

  shapeGroup.property("ADBE Vectors Group").property("ADBE Vector Graphic - Stroke").property("ADBE Vector Stroke Width").setValue(1);
  shapeGroup.property("ADBE Vectors Group").property("ADBE Vector Graphic - Stroke").property("ADBE Vector Stroke Color").setValue([1,0.5,0.5,0]);
  shapeGroup.property("ADBE Vectors Group").property("ADBE Vector Graphic - Fill").enabled = false;
  shapeGroup.property("ADBE Vectors Group").property("ADBE Vector Graphic - Stroke").enabled = true;

  shapeGroup.property("Contents").property("ADBE Vector Shape - Rect").property("Size").setValue([100,100]);
  shapeGroup.property("Contents").property("ADBE Vector Shape - Rect").property("Position").setValue([50,50]);

  app.endUndoGroup();

  }

createCClayer();
