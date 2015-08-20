import sys
import os

def print_help():
    print 'dds2png path'


 
def find_all_dds(rootDir): 
    if rootDir[-1] == '\\' or rootDir[-1] == '/':
        rootDir = rootDir[:-1]

    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:  
        for f in files: 
            if f[-3:] == 'dds':
                troot = root.replace(rootDir,rootDir + '_output')
                if not os.path.exists(troot):
                    os.makedirs(troot)
                full_name =  os.path.join(root, f)
                target_name = os.path.join(troot, f)
                target_name = target_name[:-3] + 'png'

                os.system('imconvert '+full_name + ' ' + target_name)
                print 'origin :' + full_name
                print 'imconverted :' + target_name

 





print "script name:", sys.argv[0]

if len(sys.argv) <= 1:
    print_help()
    exit(0)
if sys.argv[1] == '-h':
    print_help()
    exit(0)

find_all_dds(sys.argv[1])
