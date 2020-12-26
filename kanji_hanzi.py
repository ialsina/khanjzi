# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:58:30 2020

@author: Usuari
"""

from tqdm import tqdm
from time import sleep
from os import path

path_kanji = path.join(path.curdir, 'kanji.txt')
path_hanzi = path.join(path.curdir, 'hanzi.txt')
path_output = path.join(path.curdir, 'output.txt')

class Kanji:
    def __init__(self, line):
        linels = line.split('\t')
        self.id = int(linels[0])
        self.shin = linels[1]
        self.kyuu = linels[2]
        self.onyomi = linels[3]
        self.kunyomi = linels[4]
        self.spanish = linels[5]
        self.grade = linels[6]
    
    def oldest(self):
        return self.kyuu or self.shin
    
    def __repr__(self):
        return f"""Id:\t{self.id}\nKanji:\t{self.shin}\nOn'yomi:\t{self.onyomi}\nKun'yomi:\t{self.kunyomi}\n"""

class Hanzi:
    def __init__(self, line):
        linels = line.replace('\n','').split('\t')
        self.id = int(linels[0])
        self.simp = linels[1]
        self.trad = linels[2]
        self.pinyin = linels[3]
    
    def __repr__(self):
        return f"""Id:\t{self.id}\nSimplified:\t{self.simp}\nTraditional:\t{self.trad}\nPinyin:\t{self.pinyin}\n"""

kanji = []
hanzi = []

# Import ##################################################
with open(path_kanji,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == '#': continue
        kanji.append(Kanji(line))

with open(path_hanzi,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == '#': continue
        hanzi.append(Hanzi(line))        

del lines, line
###########################################################


print(f"Imported:\n{len(kanji)} Kanji\n{len(hanzi)} Hanzi")
print(f"Looking for matches...")
sleep(0.5)

# Compare #################################################
matches_id = []
matches_symb = []
matches = []

for k in kanji:
    kk = k.oldest()
    for h in hanzi:
        hh = h.trad
        
        if kk == hh:
            matches_id.append((k.id, h.id))
            matches_symb.append((kk, hh))
            matches.append((k, h))
###########################################################

print(f"{len(matches_id)} matches found!")

# Export ##################################################
with open(path_output,'w',encoding='UTF-8') as f:
    f.write("#Common\tKanji\tSimpl.\tKun'yomi\tOn'yomi\tPinyin\n")
    for (k, h) in matches:
        lineout = [k.oldest(), k.shin, h.simp, k.kunyomi, k.onyomi, h.pinyin]
        f.write('\t'.join(lineout)+'\n')
###########################################################

print('Matches exported')

# Stats ###################################################
id_match_kanji = sorted([el[0] for el in matches_id])
id_match_hanzi = sorted([el[1] for el in matches_id])
range_match = list(range(len(matches_id)))
normal_match = [el/len(matches_id)*100 for el in range_match]

import matplotlib.pyplot as plt

plt.figure()
plt.title('Cumulative percentage of matching')
plt.xlabel('Id')
plt.ylabel('%')
plt.plot(id_match_kanji, normal_match, label='Kanji')
plt.plot(id_match_hanzi, normal_match, label='Hanzi')
plt.legend()
plt.show()


