import os

def find(path, key):
    #print('Find: %s' % path)
    for filename in os.listdir(path):
        fullname = os.path.join(path,filename)
        if os.path.isdir(fullname):
            find(fullname, key)
        if key in filename:
            print(filename)
            
def rename(path, str_from, str_to):
    #print('Rename: %s' % path)
    for filename in os.listdir(path):
        fullname = os.path.join(path,filename)
        if os.path.isdir(fullname):
            rename(fullname, str_from, str_to)
    
        new_name = filename.replace(str_from, str_to)
        if not (filename==new_name):
            print(filename, '->', new_name)
            os.rename(fullname, os.path.join(path,new_name))
            #if os.path.isfile(fullname):

if  __name__ == '__main__':
    path = './'
    
    rename(path, ' ', '.')
    print('\n')
    find(path, '?')
    
