# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:58:30 2020

@author: Usuari
"""

from tqdm import tqdm
from time import sleep
from os import path

from include.objects import Kanji, Hanzi, Container

path_kanji = path.join(path.curdir, 'kanji.txt')
path_hanzi = path.join(path.curdir, 'hanzi.txt')
path_output = path.join(path.curdir, 'output.txt')


kanji = Container(Kanji)
hanzi = Container(Hanzi)

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
matches_kanji = Container(Kanji)
matches_hanzi = Container(Hanzi)

for k in iter(kanji):
    kk = k.oldest()
    for h in hanzi:
        hh = h.trad
        
        if kk == hh:
            matches_kanji.append(k)
            matches_hanzi.append(h)
            break
    
###########################################################

print(f"{len(matches_kanji)} matches found!")

# Export ##################################################
with open(path_output,'w',encoding='UTF-8') as f:
    f.write("#Common\tKanji\tSimpl.\tKun'yomi\tOn'yomi\tPinyin\n")
    for (k, h) in zip(matches_kanji, matches_hanzi):
        lineout = [k.oldest(), k.shin, h.simp, k.kunyomi, k.onyomi, h.pinyin]
        f.write('\t'.join(lineout)+'\n')
###########################################################

print('Matches exported')

# Stats ###################################################
id_match_kanji = matches_kanji.sort('id')
id_match_hanzi = matches_hanzi.sort('id')
range_match = list(range(len(matches_kanji)))
normal_match = [el/len(matches_kanji)*100 for el in range_match]

import matplotlib.pyplot as plt

plt.figure()
plt.title('Cumulative percentage of matching')
plt.xlabel('Id')
plt.ylabel('%')
plt.plot(id_match_kanji, normal_match, label='Kanji')
plt.plot(id_match_hanzi, normal_match, label='Hanzi')
plt.legend()
plt.show()
