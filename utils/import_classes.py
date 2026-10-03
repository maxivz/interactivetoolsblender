from . import user_prefs, custom_data


files = [user_prefs, custom_data]

def register():
    for file in files:
        file.register()


def unregister():
    for file in files:
        file.unregister()