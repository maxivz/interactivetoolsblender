from . import menus, pies, pannels
from .pie_menus import make_new, collections

files = [menus, pies, pannels, make_new, collections]

def register():
    for file in files:
        file.register()


def unregister():
    for file in files:
        file.unregister()