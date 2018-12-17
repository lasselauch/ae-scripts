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
    #string = "AE-C4D-CopyPasteColors;Ray - AEC4D-PRO;0.84313726425171,0.83137255907059,0.83137255907059,1;0.54901963472366,0.53725492954254,0.53725492954254,1;0.27058824896812,0.27058824896812,0.27058824896812,1;0.38431373238564,0.5137255191803,0.86274510622025,1;0.33333334326744,0.30588236451149,0.81960785388947,1;0.50196081399918,0,1,1;0.14509804546833,0.14117647707462,0.47843137383461,1;0.84705883264542,0.62745100259781,0.98039215803146,1;0.83137255907059,0.2392156869173,0.43137255311012,1;1,0.25,0.25,1;0.97647058963776,0.678431391716,1,1;"

    if not c4d.GetClipboardType() == c4d.CLIPBOARDTYPE_STRING and not string.startswith('AE-C4D-CopyPasteColors'):
        return

    color_table = string.split(';')[:-1]

    if not color_table:
        return

    #Remove Identifier > 'AE-C4D-CopyPasteColors'
    identifier = color_table.pop(0)

    #Pop Palette-Name from String
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

    message = 'Imported: %s Colors as "%s" into your Color-Swatches.' % (len(colors), group_name)
    gui.MessageDialog(message)

def InsertSwatchesR20(doc, group_name, colors):
    swatch_data = c4d.modules.colorchooser.ColorSwatchData(doc)
    if swatch_data is None:
        return

    swatch_data.Load(doc, False, False)
    group = swatch_data.AddGroup(c4d.SWATCH_CATEGORY_DOCUMENT, group_name, False, -1, colors)
    swatch_data.Save(doc, False)

    message = 'Imported: %s Colors as "%s" into your Color-Swatches.' % (len(colors), group_name)
    gui.MessageDialog(message)

def main():
    #Check Modifiers
    ctrl, shift, alt = GetModifiers()

    #Get String from Clipboard
    clipboard = c4d.GetStringFromClipboard()
    if not clipboard.startswith('AE-C4D-CopyPasteColors'):
        gui.MessageDialog('Please, use "copy-colors.jsx" for After Effects first...')
        return

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
