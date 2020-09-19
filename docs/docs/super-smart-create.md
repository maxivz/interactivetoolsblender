# Super Smart Create

This tool executes many creation based operations depending on the context and selection, allowing to pack a lot of actions in one hotkey.

###Object Mode
Brings up an object creation Pie Menu if nothing is selected.
![Alt Text](img/supersmartcreate_obj_01.gif)

Bring up a duplication menu if at least a object is selected.
![Alt Text](img/supersmartcreate_obj_02.gif)

###Vert Mode
If Nothing is selected it executes the cut tool.
![Alt Text](img/supersmartcreate_vert_01.gif)

Connects verts that belong to the same face.
![Alt Text](img/supersmartcreate_vert_02.gif)

If you select one vert or two verts that share the same edge and are on a border it will invoke f2 (make sure you have f2 enabled)
![Alt Text](img/supersmartcreate_vert_03.gif)

If you select multiple verts that belong to the same face, they will all be connected to the last selected vert.
![Alt Text](img/supersmartcreate_vert_04.gif)

###Edge Mode
If nothing is selected it invokes the edge loop tool
![Alt Text](img/supersmartcreate_edge_01.gif)

If you select an edge it will divide it in 2, putting a vert in the middle of the edge
![Alt Text](img/supersmartcreate_edge_02.gif)

Connects the selected edges if they are part of a ring.
![Alt Text](img/supersmartcreate_edge_03.gif)

Caps selected borders
![Alt Text](img/supersmartcreate_edge_04.gif)

Bridges selected edges if possible
![Alt Text](img/supersmartcreate_edge_05.gif)

When you select 2 adjacent edges it creates a face
![Alt Text](img/supersmartcreate_edge_06.gif)

###Face Mode
Bridges selected polys
![Alt Text](img/supersmartcreate_face_01.gif)
If a single face is selected it will try to make quads on it

![Alt Text](img/supersmartcreate_face_02.gif)

This last feature works pretty good if you select a border, run the script to make a face and then run the script again to make quads out of it:
![Alt Text](img/supersmartcreate_face_03.gif)

When Mmltiple connected faces are selected they will be subdivided
![Alt Text](img/supersmartcreate_face_04.gif)

###Curve Mode
If one point is selected it will extrude it
![Alt Text](img/supersmartcreate_curve_01.gif)

If two unconnected points are selected it will connect them
![Alt Text](img/supersmartcreate_curve_02.gif)

If two connected points are selected it will make a segment between them
![Alt Text](img/supersmartcreate_curve_03.gif)
