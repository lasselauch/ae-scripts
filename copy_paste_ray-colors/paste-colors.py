#/*
#www.lasselauch.com/lab/
#Use at your own risk
#*/

"""
Name-US:Paste Colors from Ray Dynamic Color Palette
Description-US:[ DEFAULT ] Import Color-Swatches from Ray Dynamic Color Palette<br>[ ALT-CLICK ] Import only Planes with Colors, without any questions...
"""

import c4d
from c4d import gui
if c4d.GetC4DVersion() >= 20000:
    import maxon
    from maxon import vector4d as v4

def GetModifiers():
    # Check all keys
    bc = c4d.BaseContainer()
    ctrl, shift, alt = False, False, False
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            shift = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            ctrl = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            alt = True
    return ctrl, shift, alt

def InsertColorPlanes(myName, myColors):
    doc.StartUndo()

    null = c4d.BaseObject(c4d.Onull)
    null.SetName(myName)
    doc.InsertObject(null)

    for i in xrange(len(myColors)):
        plane = c4d.BaseObject(c4d.Oplane)
        name = """[ %s, %s, %s ]""" % (myColors[i][0], myColors[i][1], myColors[i][2])
        plane.SetName(name)

        plane[c4d.ID_BASEOBJECT_USECOLOR] = 1
        plane[c4d.PRIM_PLANE_SUBW] = 1
        plane[c4d.PRIM_PLANE_SUBH] = 1
        plane[c4d.PRIM_PLANE_WIDTH] = 100
        plane[c4d.PRIM_PLANE_HEIGHT] = 100
        plane[c4d.PRIM_AXIS] = 5

        plane[c4d.ID_BASEOBJECT_COLOR] = myColors[i]
        plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = i * plane[c4d.PRIM_PLANE_WIDTH]

        doc.AddUndo(c4d.UNDOTYPE_NEW, plane)
        doc.InsertObject(plane)
        plane.InsertUnder(null)

    doc.EndUndo()
    c4d.EventAdd()

def GetColors(string):
    #String for Testing purposes
    #string = "Ray - Rodrigo Moynihan ;1,1,1,1;0.28125,0.13671875,0.48828125,1;0.8828125,0.72265625,0.625,1;1,0.86328125,0,1;0.8828125,0,0.22265625,1;0.37109375,0.765625,0.88671875,1;0,0.5078125,0.765625,1;1,0.79840242862701,0.61587011814117,1;"
    if not isinstance(string, basestring):
        return

    if not c4d.GetClipboardType() == c4d.CLIPBOARDTYPE_STRING:
        return

    color_table = string.split(';')[:-1]

    if not color_table:
        return

    myName = color_table.pop(0)
    myColors, my4DColors = [], []

    for item in color_table:
        color_list = item.split(',')
        colors = [float(c) for c in color_list]
        v = c4d.Vector(colors[0], colors[1], colors[2])
        myColors.append(v)

        if c4d.GetC4DVersion() >= 20000:
            v4D = v4.ColorA(colors[0], colors[1], colors[2], colors[3])
            my4DColors.append(v4D)

    return myName, myColors, my4DColors

def InsertSwatchesR18(doc, group_name, colors):
    swatch_data = c4d.modules.colorchooser.ColorSwatchData(doc)
    if swatch_data is None:
        return

    group=swatch_data.AddGroup(group_name, False)
    if group is not None:
        group.AddColors(colors)
        group.SetName(group_name)
        swatch_data.SetGroupAtIndex(swatch_data.GetGroupCount() - 1, group)

    swatch_data.Save(doc)

def InsertSwatchesR20(doc, group_name, colors):
    swatch_data = c4d.modules.colorchooser.ColorSwatchData(doc)
    if swatch_data is None:
        return

    swatch_data.Load(doc, False, False)
    group = swatch_data.AddGroup(c4d.SWATCH_CATEGORY_DOCUMENT, group_name, False, -1, colors)
    swatch_data.Save(doc, False)

def main():
    #Check Modifiers
    ctrl, shift, alt = GetModifiers()

    #Get String from Clipboard
    clipboard = c4d.GetStringFromClipboard()
    myName, myColors, my4DColors = GetColors(clipboard)

    #Import only Planes with Colors, without any questions...
    if alt:
        InsertColorPlanes(myName, myColors)
        return

    #Handle Pre R18 Releases
    if c4d.GetC4DVersion() <= 18011:
        gui.MessageDialog("Sorry, Swatches haven't been introduced yet!")
        question = gui.QuestionDialog("Do you want to Create Planes with Colors?")
        if question:
            InsertColorPlanes(myName, myColors)
        return

    #Handle Post R18 Pre R20 Releases
    if c4d.GetC4DVersion() >= 18011 and c4d.GetC4DVersion() <= 20000:
        InsertSwatchesR18(doc, myName, myColors)

    #Handle Post R20 Releases
    if c4d.GetC4DVersion() >= 20000:
        InsertSwatchesR20(doc, myName, my4DColors)

    c4d.EventAdd()


if __name__=='__main__':
    main()
