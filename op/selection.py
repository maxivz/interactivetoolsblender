import bpy
from ..utils import itools as itools

# Needs optimization pass, possibly merge both into one. Make them proper operators.
# Needs serious improvements.


def select_loop_directional(edge, directional=True, direction=0):
    """
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
    mesh = get_bmesh()
    update_indexes(mesh, edges=True)
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
                print("CHANGE DIRECTION")
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
            if len([face for face in new_selection[0].link_faces if len(list(face.verts)) is not 4]) is not 0:
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


class SmartSelectLoop(bpy.types.Operator):
    """
    BUGS:
     *Step Face Loop only goes in one direction for faces
    """
    bl_idname = "itools.smart_select_loop"
    bl_label = "Smart Select Loop"
    bl_description = "Context sensitive smart loop selection"
    bl_options = {'REGISTER', 'UNDO'}

    def select_face_loops(self):
        bpy.ops.mesh.loop_multi_select(ring=False)
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.mesh.select_more()
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]
        bpy.ops.mesh.select_less()

    def select_vert_loops(self):
        "Not sure it works correctly"
        bm = get_bmesh()
        vert = get_selected(verts=True)
        print(vert)
        edges = []
        for edge in bm.verts[vert[0]].link_edges:
            print(edge.index)
            edges.append(edge.index)
        select_from_index(edges, edges=True)
        bpy.ops.mesh.loop_multi_select(ring=False)

    def distance_between_elements(self, element_a, element_b, verts=False, edges=False, faces=False, ring=False):
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        select_from_index([element_a, element_b], verts=sel_set[0], edges=sel_set[1], faces=sel_set[2], replace=True)
        bpy.ops.mesh.shortest_path_select()
        selection = get_selected( verts = sel_set[0], edges = sel_set[1], faces = sel_set[2])
        if ring:
            distance = len(selection)-3
        else:
            distance = len(selection)-2
        if distance > 0:
            return distance
        else:
            return 0 
        
    def organize_elements_by_loop(self, element_selection,verts = False, edges = False, faces = False):
        selected_elements = []
        elements_to_check = element_selection
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        while len(elements_to_check) > 0:
            select_from_index(indexes = [elements_to_check[0]], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
            if verts:
                self.select_vert_loops()
            elif edges:
                bpy.ops.mesh.loop_multi_select(ring=False)
            elif faces:
                self.select_face_loops()
            element_loop = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            selected_elements.append(itools.list_intersection(element_loop, elements_to_check))
            elements_to_check = itools.list_difference(elements_to_check,element_loop)
        select_from_index(indexes =element_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
        return selected_elements
    
    def is_step_selection(self, elements_selection, verts = False, edges = False, faces = False):
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        if len(elements_selection)>2:
            selection_results = []
            results = []
            for element_a in elements_selection:
                min = []
                other_elements = itools.list_difference(elements_selection,[element_a])
                for element_b in other_elements:
                    distance = self.distance_between_elements(element_a,element_b, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
                    if len(min) == 0 or min[1] > distance: 
                        min = [list(set([element_a,element_b])),distance]
                results.append(min)
            results = list(results for results,_ in itertools.groupby(results))
            if len(list(set(list(map(lambda x: x[1], results))))) == 1:
                #print(results[0][0])
                return [True,results[0][0]]
            else:
                return [False,[]]
        else:
            return [False,[]]
    
    def complete_step_selection(self, verts = False, edges = False, faces = False):
        iteration = 0
        last_selection = []
        if verts:
            sel_set = [True, False, False]
        elif edges:
                sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        selected_elements = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
        while not selected_elements == last_selection and iteration < ITERATION_LIMIT:
            bpy.ops.mesh.select_next_item()
            last_selection = selected_elements
            selected_elements = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            iteration += 1

    def smart_loop(self, context):
        #print("")
        selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
        if selectionMode[0]:
            sel_set = [True, False, False]
        elif selectionMode[1]:
                sel_set = [False, True, False]
        elif selectionMode[2]:
            sel_set = [False, False, True]
        final_selection = []
        selection = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
        #print(organize_elements_by_loop(selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]))
        for loop in self.organize_elements_by_loop(selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]):
            step_selection_result = self.is_step_selection(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            #print(step_selection_result)
            if step_selection_result[0]: 
                select_from_index(step_selection_result[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)         
                self.complete_step_selection(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            elif len(loop) == 2:
                if self.distance_between_elements(loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) > 0:
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    bpy.ops.mesh.shortest_path_select()
                elif self.distance_between_elements(loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) == 0:
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    self.complete_step_selection(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])                    
            else:
                if selectionMode[1] == True: 
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    bpy.ops.mesh.loop_multi_select(ring=False)
            final_selection += get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            #print(final_selection)
        select_from_index(final_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)    

    def execute(self, context):
        self.smart_loop(context)
        return{'FINISHED'}

class SmartSelectRing(bpy.types.Operator):
    """
    BUGS:
     *Step Face Loop only goes in one direction for faces
    """
    bl_idname = "itools.smart_select_ring"
    bl_label = "Smart Select Loop"
    bl_description = "Context sensitive smart ring selection"
    bl_options = {'REGISTER', 'UNDO'}

    def select_face_rings(self):
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.context.tool_settings.mesh_select_mode = [False,True,False]
        bpy.ops.mesh.select_more()
        bpy.context.tool_settings.mesh_select_mode = [False,False,True]
        bpy.ops.mesh.select_less()

    def select_vert_rings(self):
        "Not sure it works correctly"
        bm = get_bmesh()
        vert = get_selected(verts = True)
        print(vert)
        edges=[]
        for edge in bm.verts[vert[0]].link_edges:
            print(edge.index)
            edges.append(edge.index)
        select_from_index(edges, edges=True)
        bpy.ops.mesh.loop_multi_select(ring=True)

    def distance_between_elements(self, element_a,element_b,verts = False, edges = False, faces = False, ring = False):
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        select_from_index([element_a,element_b], verts = sel_set[0], edges = sel_set[1], faces = sel_set[2], replace = True)
        bpy.ops.mesh.shortest_path_select()
        selection = get_selected( verts = sel_set[0], edges = sel_set[1], faces = sel_set[2])
        if ring:
            distance = len(selection)-3
        else:
            distance = len(selection)-2
        if distance > 0:
            return distance
        else:
            return 0 
        
    def organize_elements_by_ring(self, element_selection,verts = False, edges = False, faces = False):
        selected_elements = []
        elements_to_check = element_selection
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        while len(elements_to_check) > 0:
            select_from_index(indexes = [elements_to_check[0]], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
            if verts:
                self.select_vert_rings()
            elif edges:
                bpy.ops.mesh.loop_multi_select(ring=True)
            elif faces:
                self.select_face_rings()
            element_loop = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            selected_elements.append(itools.list_intersection(element_loop, elements_to_check))
            elements_to_check = itools.list_difference(elements_to_check,element_loop)
        select_from_index(indexes =element_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True)
        return selected_elements
    
    def is_step_selection(self, elements_selection, verts = False, edges = False, faces = False):
        if verts:
            sel_set = [True, False, False]
        elif edges:
            sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        if len(elements_selection)>2:
            selection_results = []
            results = []
            for element_a in elements_selection:
                min = []
                other_elements = itools.list_difference(elements_selection,[element_a])
                for element_b in other_elements:
                    distance = self.distance_between_elements(element_a,element_b, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], ring = True)
                    if len(min) == 0 or min[1] > distance: 
                        min = [list(set([element_a,element_b])),distance]
                results.append(min)
            results = list(results for results,_ in itertools.groupby(results))
            if len(list(set(list(map(lambda x: x[1], results))))) == 1:
                return [True,results[0][0]]
            else:
                return [False,[]]
        else:
            return [False,[]]
    
    def complete_step_selection(self, verts = False, edges = False, faces = False):
        iteration = 0
        last_selection = []
        if verts:
            sel_set = [True, False, False]
        elif edges:
                sel_set = [False, True, False]
        elif faces:
            sel_set = [False, False, True]
        selected_elements = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
        while not selected_elements == last_selection and iteration < ITERATION_LIMIT:
            bpy.ops.mesh.select_next_item()
            last_selection = selected_elements
            selected_elements = get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            iteration += 1

    def smart_ring(self, context):
        #print("")
        selectionMode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
        if selectionMode[0]:
            sel_set = [True, False, False]
        elif selectionMode[1]:
                sel_set = [False, True, False]
        elif selectionMode[2]:
            sel_set = [False, False, True]
        final_selection = []
        selection =  get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
        #print(organize_elements_by_loop(selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]))
        for loop in self.organize_elements_by_ring(selection,verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]):
            step_selection_result = self.is_step_selection(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            print(step_selection_result)
            if step_selection_result[0]: 
                select_from_index(step_selection_result[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)         
                self.complete_step_selection(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            elif len(loop) == 2:
                if self.distance_between_elements(loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) > 0:
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    bpy.ops.mesh.shortest_path_select(use_face_step=True)
                elif self.distance_between_elements(loop[0],loop[1], verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2]) == 0:
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    self.complete_step_selection(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])                    
            else:
                if selectionMode[1] == True: 
                    select_from_index(loop, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)
                    bpy.ops.mesh.loop_multi_select(ring=True)
            final_selection += get_selected(verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2])
            #print(final_selection)
        select_from_index(final_selection, verts = sel_set[0] , edges = sel_set[1], faces = sel_set[2], replace = True, add_to_history = True)    

    def execute(self, context):
        self.smart_ring(context)
        return{'FINISHED'}