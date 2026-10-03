from . import super_smart_create
from . import radial_symmetry 
from . import quick_align 
from . import pivot 
from . import smart_extrude 
from . import mesh_modes 
from . import misc 
from . import smart_delete 
from . import smart_modify 
from . import selection 
from . import smart_transform 
from . import quick_lattice 
from . import quick_pipe 
from . import visibility
from . import rebase_cylinder 
from . import collision_ops 
from . import uv_functions 
from . import collection_ops 

files = [super_smart_create, radial_symmetry, quick_align, pivot, smart_extrude, mesh_modes, misc,
        smart_delete, smart_modify, selection, smart_transform, quick_lattice, quick_pipe, visibility,
        rebase_cylinder, collision_ops, uv_functions, collection_ops]

def register():
    for file in files:
        file.register()


def unregister():
    for file in files:
        file.unregister()