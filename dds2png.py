import sys
import os

def print_help():
    print 'dds2png path'


 
def find_all_dds(rootDir): 
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:  
        for f in files: 
            if f[-3:] == 'dds':
                full_name =  os.path.join(root, f)
                target_name = full_name[:-3] + 'png'
                print 'convert dds 2 png'
                os.system('imconvert '+full_name + ' ' + target_name)
                if os.path.isfile(target_name):
                    print 'convert png success!'
                    print 'remove ' + full_name
                    os.remove(full_name)





print "script name:", sys.argv[0]

if len(sys.argv) <= 1:
    print_help()
    exit(0)
if sys.argv[1] == '-h':
    print_help()
    exit(0)

find_all_dds(sys.argv[1])
