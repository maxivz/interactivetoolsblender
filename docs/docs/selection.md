##Selection


###Quick Vert Mode

*	If you are in object mode it will switch to vert selection mode.

*	If you are in face or edge mode it will switch to vert mode.

*	If you are in vertex selection mode it will switch to object mode.

*	If the selected object is a curve, and you are in object mode it will switch to edit mode.

*	If you are in the curve edit mode it will switch to object mode.

###Quick Edge Mode

*	If you are in object mode it will switch to edge selection mode.

*	If you are in vert or face mode it will switch to edge mode.

*	If you are in edge selection mode it will switch to object mode.

*	If the selected object is a curve, and you are in object mode it will switch to edit mode.

*	If you are in the curve edit mode it will switch to object mode.

###Quick Face Mode

*	If you are in object mode it will switch to face selection mode.

*	If you are in vert or edge mode it will switch to face mode.

*	If you are in face selection mode it will switch to object mode.

*	If the selected object is a curve, and you are in object mode it will switch to edit mode.

*	If you are in the curve edit mode it will switch to object mode.

###Sticky Selection(TODO)

![Alt Text](img/selection_sticky.gif)


###Smart Loop
If two continuous edges or one edge is selected, the edge loop is going to be selected.
![Alt Text](img/smartloop_01.gif)

If two edges are selected, it's going to get the edge loop between them.
![Alt Text](img/smartloop_02.gif)

If three edges are selected, and they have the same space between them a step selection will be made.
![Alt Text](img/smartloop_03.gif)

These modes work with multiple selections at the same time.
![Alt Text](img/smartloop_04.gif)

---

Support for vertex and face mode is limited, but some modes work.

---

###Smart Ring
If two continuous edges or one edge is selected, the edge ring is going to be selected.
![Alt Text](img/smartring_01.gif)

If two edges are selected, it's going to get the edge ring between them,
![Alt Text](img/smartring_02.gif)

If three edges are selected, and they have the same space between them a step selection will be made.
![Alt Text](img/smartring_03.gif)

These modes work with multiple selections at the same time.
![Alt Text](img/smartring_04.gif)

---

Support for vertex and face mode is limited, but some modes work.

There is a known bug with ring selections not working sometimes, a fix will be released on the future.

---
