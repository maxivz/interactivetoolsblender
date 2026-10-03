import bpy
from . ui import import_classes as ui_import_classes
from . op import import_classes as op_import_classes
from . utils import import_classes as utils_import_classes


bl_info = {
	"name": "Interactive Tools",
	"author": "Maxi Vazquez, Ajfurey",
	"description": "Collection of context sensitive tools",
	"blender": (4, 5, 0),
	"location": "View3D",
	"version": (1, 5, 0),
	"tracker_url": "https://github.com/maxivz/interactivetoolsblender/issues",
	"wiki_url": "https://maxivz.github.io/interactivetoolsblenderdocs.github.io/",
	"warning": "",
	"category": "Generic"
}

addon_files = [op_import_classes, ui_import_classes, utils_import_classes]

def register():
	for addon_file in addon_files:
		addon_file.register()


def unregister():
	for addon_file in addon_files:
		addon_file.unregister()


if __name__ == "__main__":
	register()
