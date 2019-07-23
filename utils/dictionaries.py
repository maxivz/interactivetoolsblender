import bpy

itools_dic = {"selected_verts": [],
              "selected_edges": [],
              "selected_faces": []}


def write(data_block, values, obj=""):
    if obj == "":
        obj = bpy.context.active_object

    if "itools" not in bpy.context.object:
        obj['itools'] = itools_dic

    obj['itools'][data_block] = values


def read(data_block, obj=""):
    if obj == "":
        obj = bpy.context.active_object

    if "itools" in bpy.context.object:
        return obj['itools'][data_block]

    else:
        return ""
