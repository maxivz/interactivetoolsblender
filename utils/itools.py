import bpy
import bmesh
from collections import OrderedDict, Counter


MAX_ITERATIONS = 400
DOUBLECLICK_TIME = 0.1


def list_union(a, b):
    return list(set(a) | set(b))


def list_intersection(a, b):
    temp = set(b)
    result = [item for item in a if item in temp]
    return result
    # return list(set(a) & set(b))


def list_difference(a, b):
    temp = set(b)
    result = [item for item in a if item not in temp]
    return result
    # return list(set(a) - set(b))


def list_reduce_ordered(items):
    new_list = list(OrderedDict.fromkeys(items))
    return new_list


def get_mode():
    mode = bpy.context.mode
    if mode == 'EDIT_MESH':
        selection_mode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
        if selection_mode[0]:
            return 'VERT'
        elif selection_mode[1]:
            return 'EDGE'
        elif selection_mode[2]:
            return 'FACE'

    if mode == 'EDIT_GPENCIL':
        return bpy.context.scene.tool_settings.gpencil_selectmode_edit

    return mode


def set_mode(mode, grow=False):
    actual_mode = get_mode()
    if mode == 'OBJECT' and actual_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    elif mode in ['VERT', 'EDGE', 'FACE']:
        if actual_mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type=mode, use_expand=grow)


def get_bmesh():
    if get_mode() in ['VERT', 'EDGE', 'FACE']:
        return bmesh.from_edit_mesh(bpy.context.edit_object.data)
    else:
        print("Must be in obj mode to get bmesh")


def to_index(items):
    return [element.index for element in items]


# Return item or index for selected mesh elements or names for objects
# Add selection order by using print([a.index for a in bm.select_history])
def get_selected(mode='', item=True, ordered=False, all=False):
    selection = []
    if not mode:
        mode = get_mode()

    if mode == 'OBJECT':
        if item:
            return [obj for obj in bpy.context.selected_objects]

        else:
            return [obj.name for obj in bpy.context.selected_objects]

    elif mode in ['VERT', 'EDGE', 'FACE']:
        bm = get_bmesh()

        if ordered:
            if mode == 'VERT':
                selection = [vert for vert in bm.select_history if isinstance(vert, bmesh.types.BMVert)]
            elif mode == 'EDGE':
                selection = [edge for edge in bm.select_history if isinstance(edge, bmesh.types.BMEdge)]
            elif mode == 'FACE':
                selection = [face for face in bm.select_history if isinstance(face, bmesh.types.BMFace)]

        if all:
            if mode == 'VERT':
                selection = [vert for vert in bm.verts]
            elif mode == 'EDGE':
                selection = [edge for edge in bm.edges]
            elif mode == 'FACE':
                selection = [face for face in bm.faces]

        else:
            if mode == 'VERT':
                selection = [vert for vert in bm.verts if vert.select]
            elif mode == 'EDGE':
                selection = [edge for edge in bm.edges if edge.select]
            elif mode == 'FACE':
                selection = [face for face in bm.faces if face.select]

        if item:
            return selection
        else:
            return [element.index for element in selection]

    elif mode == 'EDIT_CURVE':
        curves = bpy.context.active_object.data.splines
        points = []

        if all:
            for curve in curves:
                if curve.type == 'BEZIER':
                    points.append([point for point in curve.bezier_points])

                else:
                    points.append([point for point in curve.points])

        else:
            for curve in curves:
                if curve.type == 'BEZIER':
                    points.append([point for point in curve.bezier_points
                                   if point.select_control_point])

                else:
                    points.append([point for point in curve.points
                                   if point.select])

        points = [item for sublist in points for item in sublist]
        return points

    else:
        return []


# Returns active object name
def active_get(item=True):
    if item:
        return bpy.context.active_object
    else:
        return bpy.context.active_object.name


# Sets active object based on name
def active_set(obj, item=True):
    if item:
        print(obj)
        bpy.context.view_layer.objects.active = obj
    else:
        bpy.context.view_layer.objects.active = bpy.data.objects[obj]


# Make selection based on indexes for selected mesh elements or names for objects
def select(target, mode='', item=True, replace=False, deselect=False, add_to_history=False, safe_mode=False):
    if not mode:
        mode = get_mode()

    if safe_mode:
        existing_items = get_selected(mode=mode, item=item, all=True)

    selection_value = True

    if deselect:
        selection_value = False

    if type(target) != list:
        target = [target]

    if mode == 'OBJECT':
        if replace:
            bpy.ops.object.select_all(action='DESELECT')

        if item:
            for obj in target:
                target.select_set(selection_value)

        else:
            for obj in target:
                bpy.data.objects[obj].select_set(selection_value)

    elif mode in ['VERT', 'EDGE', 'FACE']:
        bm = get_bmesh()

        if replace:
            bpy.ops.mesh.select_all(action='DESELECT')

        if item:
            target = [item.index for item in target]

        if safe_mode:
            if mode == 'VERT':
                for vert in target:
                    if vert in existing_items:
                        bm.verts[vert].select = selection_value
                        if add_to_history:
                            bm.select_history.add(bm.verts[vert])

            elif mode == 'EDGE':
                for edge in target:
                    if edge in existing_items:
                        bm.edges[edge].select = selection_value
                        if add_to_history:
                            bm.select_history.add(bm.edges[edge])

            elif mode == 'FACE':
                for face in target:
                    if face in existing_items:
                        bm.faces[face].select = selection_value
                        if add_to_history:
                            bm.select_history.add(bm.faces[face])

        else:
            if mode == 'VERT':
                for vert in target:
                    bm.verts[vert].select = selection_value
                    if add_to_history:
                        bm.select_history.add(bm.verts[vert])

            elif mode == 'EDGE':
                for edge in target:
                    bm.edges[edge].select = selection_value
                    if add_to_history:
                        bm.select_history.add(bm.edges[edge])

            elif mode == 'FACE':
                for face in target:
                    bm.faces[face].select = selection_value
                    if add_to_history:
                        bm.select_history.add(bm.faces[face])

    elif mode == 'EDIT_CURVE':
        print("Curve")
        curves = bpy.context.active_object.data.splines
        points = []
        for curve in curves:
            if safe_mode:
                if curve.type == 'BEZIER':
                    for point in curve.bezier_points:
                        if point in existing_items:
                            point.select_control_point = True
                else:
                    for point in curve.points:
                        if point in existing_items:
                            point.select = True
            else:
                if curve.type == 'BEZIER':
                    for point in curve.bezier_points:
                        point.select_control_point = True
                else:
                    for point in curve.points:
                        point.select = True


def convert_selection(selection, to):
    mode = get_mode()

    if mode == 'VERT':
        if to == 'EDGE':
            new_selection = [edge for vert in selection
                             for edge in vert.link_edges]

        elif to == 'FACE':
            new_selection = [face for vert in selection
                             for face in vert.link_faces]

        new_selection = [item for item, count
                         in Counter(new_selection).items()
                         if count > 1]

    elif mode == 'EDGE':
        if to == 'VERT':
            new_selection = [vert for edge in selection
                             for vert in edge.verts]

        elif to == 'FACE':
            new_selection = [face for edge in selection
                             for face in edge.link_faces]

    elif mode == 'FACE':
        if to == 'VERT':
            new_selection = [vert for face in selection
                             for vert in face.verts]

        elif to == 'EDGE':
            new_selection = [edge for face in selection
                             for edge in face.edges]

    new_selection = remove_duplicates(new_selection)

    return new_selection


def update_indexes(mode=''):
    bm = get_bmesh()
    if not mode:
        print("Try to get mode")
        mode = get_mode()
        print(mode)

    if 'VERT' or 'ALL' in mode:
        bm.verts.index_update()
        bm.verts.ensure_lookup_table()

    if 'EDGE' or 'ALL' in mode:
        bm.edges.index_update()
        bm.edges.ensure_lookup_table()

    if 'FACE' or 'ALL' in mode:
        bm.faces.index_update()
        bm.faces.ensure_lookup_table()

    bmesh.update_edit_mesh(bpy.context.edit_object.data)


def remove_duplicates(target):
    return list(set(target))


def get_children(obj_name):
    children = []
    for ob in bpy.data.objects:
        if ob.parent != None:
            if ob.parent.name == obj_name:
                children.append(ob)
    return children
