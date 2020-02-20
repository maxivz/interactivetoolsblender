import os

dirlist = os.listdir(path='.')
classes = ()
for dir in dirlist:
    if dir in ['op','utils','ui']:
        #Find .py files
        files = os.listdir(path=dir)
        files = list(filter(lambda x: x[-3:] == '.py', files))
        print(files)

        #Find class list in files
        for f in files:
            try:
                f = f[:-3]
                from . dir import f
                print(f.classes_to_load)
            except:
                print("Couldnt find variables")