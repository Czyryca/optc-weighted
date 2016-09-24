from collections import defaultdict
import operator
import re
import linecache
def main():
    
    #Get ids of characters in global
    flags_file = open('flags.js','r')
    pattern_global = re.compile('\d+:.*global: 1')
    global_ids = [int(str(line).split(':')[0]) for line in pattern_global.findall(flags_file.read())]

    #Get ids of fully evo'd characters
    evo_file = open('evolutions.js','r')
    pattern_no_evo = re.compile('\d+:')    
    unevod_ids = [str(line).split(':')[0] for line in pattern_no_evo.findall(evo_file.read())]
    evod_ids = [ id for id in range(1,1250) if str(id) not in unevod_ids ]
    #TODO: fix this range!!

    #get intersection of lists
    ids = [ id for id in global_ids if id in evod_ids ]

    #get stats for chars
    characters = {}
    for id in ids:
        pattern_info = re.compile('(".*?"), (".*?")') 
        info_line = linecache.getline('units.js',id+1) #+1 fixes indexing
        info = pattern_info.search(info_line)
        stats = info_line.split(',')
        try:
            hp  = int(stats[-5])
            atk = int(stats[-4])
            rcv = int(stats[-3])
        except ValueError: #char has weird growth rates
            hp = int(stats[-7])
            atk = int(stats[-6])
            rcv = int(stats[-5])
        name,weighted=info.group(1),hp/5+atk/2+rcv
        characters[name] = weighted
    print [key+': '+str(value) for (key, value) in reversed(sorted(characters.items(), key = operator.itemgetter(1)))]

if __name__ == "__main__":
    main()
