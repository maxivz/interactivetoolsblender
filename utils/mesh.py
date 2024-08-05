import bpy
import bmesh
from functools import reduce
from . import itools as itools

# Shared Mesh utilities and operations


def verts_share_edge(verts):
    if len(verts) == 2:
        return len(itools.list_intersection(verts[0].link_edges,
                   verts[1].link_edges)) == 1

    else:
        return False


# Aproximation, might not work all the times. Will replace later
def verts_share_face(verts):
    face_list = []
    for vert in verts:
        face_list.append(vert.link_faces)
    face_list = reduce(lambda x, y: itools.list_intersection(x, y), face_list)
    if len(face_list) > 0:
        return True
    else:
        return False


def is_corner_vert(vert):
    return len([face for face in vert.link_faces]) > 2


def is_border_vert(vert):
    return len([edge for edge in vert.link_edges if len(edge.link_faces) == 1]) > 1


def are_border_verts(verts):
    return all(is_border_vert(vert) for vert in verts)


def is_border_edge(edge):
    return all(is_border_vert(vert) for vert in edge.verts)


def is_border(selection):
    # every edge must be adjacent with two other edges, if its a closed
    # border the number of adjacent edges should be at least 2 X number edges
    adjacent_edges = [neightbour for edge in selection for verts in edge.verts
                      for neightbour in verts.link_edges if neightbour in selection and neightbour != edge]
    return (all(is_border_edge(edge) for edge in selection) and len(adjacent_edges) >= len(selection) * 2)


def is_partial_border(selection):
    return (all(is_border_edge(edge) for edge in selection))


def is_adjacent(selection, mode):
    if mode == 'EDGE':
        vert_list = [edge.verts for edge in selection]
        common_vert = reduce(lambda x, y: itools.list_intersection(x, y), vert_list)
        return len(common_vert) == 1

    elif mode == 'FACE':
        edge_list = [edge for face in selection for edge in face.edges]
        print("Edge list :", edge_list)
        vert_list = [edge.verts for edge in edge_list]
        print("Vert list :", vert_list)
        common_vert = reduce(lambda x, y: itools.list_intersection(x, y), vert_list)
        return len(common_vert) > 0


def organize_faces_by_continuity(selection):
        groups = []
        ordered_groups = []
        temp = []

        for face in selection:
                adjacent_faces = []
                adjacent_faces = [face2.index for edge in face.edges
                                  for face2 in edge.link_faces
                                  if face2 in selection]
                adjacent_faces.append(face.index)
                adjacent_faces = list(set(adjacent_faces))
                groups.append(adjacent_faces)

        while len(groups) > 0:
                temp = groups[0]
                for group in groups[1:]:
                        intersection = itools.list_intersection(temp, group)
                        if len(intersection) > 0:
                                temp = itools.list_union(temp, group)

                ordered_groups.append(temp)

                groups = [group for group in groups
                          if not any(element in temp
                                     for element in group)]

        return ordered_groups


def is_ring(selection):
    """
    # Aproximation that should work 98% for now
    # Gets false positives when corners are selected like this: I_ or _I
    """
    neightbour_numbers = [edge for edge in selection
                          if len([face for face in edge.link_faces if any(edge2 for edge2 in face.edges
                                  if edge2 in selection and edge2 != edge)]) > 0]
    return len(neightbour_numbers) == len(selection)
