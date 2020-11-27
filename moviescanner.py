from fuzzywuzzy import process
import os

ignore = [	
    # audio
    'AC3LD', ' MIC ', 'DTS', 'AC3D', 'AC3',  'Dubbed', ' 5 1 ', ' 6ch ', 
    ' LD ', ' DL ', ' MD ', 
    ' Line ', 'aac51', ' aac', ' avc', ' 128kbit', 'ac3md', 
    # video
	'1080p', '720p', '360p', 'BluRay', 'microhd', 
	'SCR', ' HD ', ' SD ', 
	'x264', 'x265', 'h264', 'mpeg2', '4k', 
	'HDTV', ' HDDVD ', ' 3D ', '30fps', '24fps', 'rsvcd'
	'BRRip', 'HDRip', 'BDRiP', ' WS ', 'R5', 'R6', 'XViD', 'DVDSCR', 
	'DVDRip', 'WebHD', 'Rip', ' BD ', ' TV ', ' WEB', 'DiVX', 'mvcdv', 'mvcd', ' DVD',
	# language
	'German', 'English', 'Hindi', 'Multi', ' de ', ' ML ', ' eng ', ' ger ',
	# tags
	'DirCut', 'unrated', 'rogue cut', 'uncut', 'limited', 'remastered', 'REMUX',
	# release
	'iNTERNAL', 'filecrypt.cc', 'PROPER', 'repack', 'read.nfo', 'nfo',
	'CD1', 'CD2',
]

extentions = ['mkv', 'avi', 'mp4', 'mpg', 'iso', 'flv', 'vob', 'mpeg']
strange = [ 'log', 'txt', 
            'acl', 'rar', 'bup', 
            'inf', 'exe', 'dll', 'log', 
            'zip'
] # sfv, db, mta
split_token = ['.', '-', '_', '[', ']', '(', ')', ' ']

def splitrep(str_inp, tokens, sep=' '):
    for sp in tokens:
        str_list = list(filter(None, str_inp.split(sp)))
        str_inp = sep.join(str_list)
    return str_inp

def ExtSelector(filename, ext_list):
    head, tail = os.path.split(filename)
    name, ext = os.path.splitext(tail)
    ext = ext.replace('.', '').lower()
    return (ext in ext_list), head, name, ext

def FileSelector(path, file_list, ext_list):
    sel_list = []
    for filename in file_list:
        fullname = os.path.join(path,filename)
        if os.path.isfile(fullname):
            ret, _, name, _ = ExtSelector(filename, ext_list)
            if ret:
                ratios = process.extract(name, sel_list)
                if len(ratios)<1:
                    sel_list.append(name)
                elif ratios[0][1]<90:
                    sel_list.append(name)
                    
    return sel_list
    
def DeCrewCut(str_inp, verbose=False, export=False):
    decrew = str_inp.split('-')
    if len(decrew)>1:
        if not (' ' in decrew[-1]):
            if verbose:
                if not export:
                    print('-\t', decrew[-1])
                else:
                    print(decrew[-1])
            decrew = decrew[:-1]
        else:
            if verbose and not export:
                print('+\t', decrew[-1])
            
    str_inp = '-'.join(decrew)
    return str_inp

def NameNormalizer(str_inp):
    str_inp = splitrep(str_inp.lower(), ['.', '_', ' '], ' ')
    
    #from parse_crew import DeCrewList
    #str_inp = DeCrewList(str_inp)
    
    str_inp = DeCrewCut(str_inp, export=False)
    
    return str_inp

def NameSelector(path, head, tail, file_list, ext_list):
    head = head.split('/')
    #return head[-1] + '/' + tail
    sel_list = FileSelector(path, file_list, ext_list)
    if len(sel_list)>1:
        return tail
    else:
        return head[-1]

items_name = []
items_path = []

lost = []
def parse(path, base, verbose=True):
    file_list = os.listdir(path)
    idx = 0
    for filename in file_list:
        fullname = os.path.join(path,filename)
        if os.path.isdir(fullname):
            parse(fullname, base)
        elif os.path.isfile(fullname):
            ret, head, name, ext = ExtSelector(fullname, extentions)
            head = head.replace(base,'')
            if ret:
                new_name = NameSelector(path, head, name, file_list, extentions)
                new_name = NameNormalizer(new_name)
                for rep in ignore:
                    new_name = new_name.replace(rep.lower(), '')
                new_name = splitrep(new_name, split_token)
                ratios = process.extract(new_name, items_name)
                if len(ratios)<1 or ratios[0][1]<100:
                    items_name.append(new_name)
                    items_path.append(fullname)
                    idx = idx+1

                    for r in ratios:
                        if r[1]>90:
                            if verbose:
                                print('%i (%i) %s' % (idx, len(file_list), new_name))
                                print('\t(%i%%) %s'%(r[1],r[0]))
            else:
                if ext in strange:
                    pass
                    #print('/'.join([*(head[-2:]), tail]))
                if not ext in lost:
                    lost.append(ext)


if  __name__ == '__main__':
    path = '/media/Movies/'
    parse(path, path)
    print(lost)
    
