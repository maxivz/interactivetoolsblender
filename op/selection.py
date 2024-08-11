import bpy
from ..utils import itools as itools
import itertools
import time

ITERATION_LIMIT = 400


def select_face_loops(ring=False):
    if ring:
        bpy.ops.mesh.loop_multi_select(ring=True)

    else:
        bpy.ops.mesh.loop_multi_select(ring=False)

    itools.set_mode('EDGE')
    bpy.ops.mesh.select_more()
    itools.set_mode('FACE')
    bpy.ops.mesh.select_less()


# Review this function later
def select_vert_loops(ring=False):
    bm = itools.get_bmesh()
    vert = itools.get_selected('VERT', item=False)
    edges = [edge.index for edge in bm.verts[vert[0]].link_edges]
    itools.select(edges, 'EDGE', item=False)

    if ring:
        bpy.ops.mesh.loop_multi_select(ring=True)

    else:
        bpy.ops.mesh.loop_multi_select(ring=False)


def distance_between_elements(elements, mode, ring=False):
    itools.select(elements, mode, item=False, replace=True)
    bpy.ops.mesh.shortest_path_select()
    selection = itools.get_selected(mode, item=False)

    if ring:
        distance = len(selection) - 3
    else:
        distance = len(selection) - 2

    if distance > 0:
        return distance
    else:
        return 0


def organize_elements_by_loop(elements, mode, ring=False):
    selected_elements = []
    elements_to_check = elements

    while len(elements_to_check) > 0:
        itools.select([elements_to_check[0]], mode, item=False, replace=True)

        if mode == 'VERT':
            select_vert_loops(ring=ring)
        elif mode == 'EDGE':
            bpy.ops.mesh.loop_multi_select(ring=ring)
        elif mode == 'FACE':
            select_face_loops(ring=ring)

        element_loop = itools.get_selected(mode, item=False)
        selected_elements.append(itools.list_intersection(element_loop, elements_to_check))
        elements_to_check = itools.list_difference(elements_to_check, element_loop)

    return selected_elements


def is_step_selection(selection, mode, ring=False):
    if len(selection) > 2:
        selection_results = []
        results = []
        # OPTIMIZATION: ONLY CHECK FIRST 3
        if len(selection) > 3:
            selection = selection[:3]

        for a in selection:
            min = []
            other_elements = itools.list_difference(selection, [a])

            for b in other_elements:
                distance = distance_between_elements([a, b], mode, ring)

                if len(min) == 0 or min[1] > distance:
                    min = [[a, b], distance]

            results.append(min)

        distances = list(set([x[1] for x in results]))
        itools.select(selection, item=False, replace=True, add_to_history=True)

        if len(distances) == 1:
            return [True, distances[0]]

        else:
            return [False, 0]

    else:
        return [False, 0]


# Think of new way to complete step selection for future updates to fix bugs with
# step selections in loops and rings that are not cyclical
def complete_step_selection(mode):
    iteration = 0
    last_selection = []
    selected_elements = itools.get_selected(mode, item=False)

    while not selected_elements == last_selection and iteration < ITERATION_LIMIT:
        bpy.ops.mesh.select_next_item()
        last_selection = selected_elements
        selected_elements = itools.get_selected(mode, item=False)
        iteration += 1


def smart_loop(ring=False):
    final_selection = []
    mode = itools.get_mode()
    selection = itools.get_selected(mode, item=False)
    organized_loops = organize_elements_by_loop(selection, mode, ring)

    for loop in organized_loops:
        step_selection_result = is_step_selection(loop, mode, ring)

        if step_selection_result[0]:
            complete_step_selection(mode)

        elif len(loop) == 2:
            distance = distance_between_elements([loop[0], loop[1]], mode, ring)

            if distance > 0:
                itools.select(loop, mode, item=False, replace=True, add_to_history=True)

                if ring:
                    bpy.ops.mesh.shortest_path_select(use_face_step=True)

                else:
                    bpy.ops.mesh.shortest_path_select()

            elif distance == 0:
                itools.select(loop, mode, item=False, replace=True, add_to_history=True)
                bpy.ops.mesh.loop_multi_select(ring=ring)

        else:
            if mode == 'EDGE':
                itools.select(loop, mode, item=False, replace=True, add_to_history=True)
                bpy.ops.mesh.loop_multi_select(ring=ring)

        final_selection += itools.get_selected(mode, item=False)

    itools.select(final_selection, mode, item=False, replace=True, add_to_history=True)


def show_message(message="", title="Message Box", icon='INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class SmartSelectLoop(bpy.types.Operator):
    """
    BUGS:
     *Step Face Loop only goes in one direction for faces
     *Sometimes top and bottom is ignored on loops of spheres, investigate
     *Complete step selection only works in one direction
    """
    bl_idname = "mesh.smart_select_loop"
    bl_label = "Smart Select Loop"
    bl_description = "Context sensitive smart loop selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        smart_loop()
        return{'FINISHED'}


class SmartSelectRing(bpy.types.Operator):
    """
    BUGS:
     *Step Face Loop only goes in one direction for faces
    """
    bl_idname = "mesh.smart_select_ring"
    bl_label = "Smart Select Ring"
    bl_description = "Context sensitive smart ring selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        smart_loop(ring=True)
        return{'FINISHED'}


def select_loop_directional(edge, directional=True, direction=0):
    """
    Future selection algorithm, not fully implemented, still in developments
        *Bugs: Improve selection of edges that dont have two faces
        Selects more than intended
    FEATURES:
        *Select border if the selection is in a border
    """
    counter = 0
    iterations = 0
    selection = [edge]
    selected = selection
    new_selection = selection
    iterate = True
    directionality_loop = True
    mesh = itools.get_bmesh()
    print("SELECT LOOP DIRECTIONAL STARTS")
    now = time.time()
    # update_indexes(mesh, edges=True)
    while directionality_loop and counter < 2:
        while iterations < ITERATION_LIMIT and iterate:
            print("")
            print("----------------------------")
            print(iterations)
            print("Current Edge")
            print(selection)
            if direction == 0:
                new_selection = [selection[0].link_loops[0].link_loop_next.link_loop_radial_next.link_loop_next.edge]

            else:
                new_selection = [selection[0].link_loops[0].link_loop_prev.link_loop_radial_next.link_loop_prev.edge]

            if new_selection[0].select:
                # print("CHANGE DIRECTION")
                if direction == 0:
                    new_selection = [selection[0].link_loops[0].link_loop_prev.link_loop_radial_next.link_loop_prev.edge]
                else:
                    new_selection = [selection[0].link_loops[0].link_loop_next.link_loop_radial_next.link_loop_next.edge]
                # Check if new selection is still selected after correcting direction
                if new_selection[0].select:
                    print("COMPLETE LAP")
                    iterate = False
            if len(itools.list_intersection(list(new_selection[0].verts), list(selection[0].verts))) < 1:
                # Correct selection for cases where theres holes close by
                print("HOLES CLOSEBY, CORRECTING")
                new_selection = [selection[0].link_loops[0].link_loop_radial_next.link_loop_prev.link_loop_radial_next.link_loop_prev.edge]
            if len([face for face in new_selection[0].link_faces if (selection[0] in face.edges)]) > 0:
                # Make sure you cant accidentally select a loop on top or below of it
                print("LOOP WILL JUMP ROW")
                new_selection = selection
                iterate = False
            if len([face for face in new_selection[0].link_faces if len(list(face.verts)) != 4]) != 0:
                # End selection on ngons or triangles
                print("END LOOP")
                iterate = False
            selection = new_selection
            new_selection[0].select = True
            iterations += 1
        # If not directional reset and start the other way
        if not directional:
            iterate = True
            iterations = 0
            direction = 1
            selection = [edge]
            new_selection = selection
        else:
            directionality_loop = False
        counter += 1
    end = time.time()
    print("SELECT LOOP DIRECTIONAL ENDS TIME: %s", time)
