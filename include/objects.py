#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 19:36:00 2020

@author: ivan
"""

class Kanji:
    def __init__(self, line):
        linels = line.split('\t')
        self.id = int(linels[0])
        self.shin = linels[1]
        self.kyuu = linels[2]
        self.radical = linels[3]
        self.strokes = linels[4]
        self.grade = linels[5]
        self.year_added = linels[6]
        self.english = linels[7]
        self.onyomi = linels[8]
        self.kunyomi = linels[10]
        self.roomaji_onyomi = linels[9]
        self.roomaji_kunyomi = linels[11]
    
    def oldest(self):
        return self.kyuu or self.shin
    
    def __call__(self):
        return self.shin
    
    def __str__(self):
        return f"""Id:\t{self.id}\nKanji:\t{self.shin}\nOn'yomi:\t{self.onyomi}\nKun'yomi:\t{self.kunyomi}\n"""

class Hanzi:
    def __init__(self, line):
        linels = line.replace('\n','').split('\t')
        self.id = int(linels[0])
        self.simp = linels[1]
        self.trad = linels[2]
        self.pinyin = linels[3]
        self.english = linels[4]
        self.radical = linels[5]
        self.strokes = linels[6]
        self.hsk_level = linels[7]
        self.general_standard = linels[8]
        self.frequency_rank = linels[9]

    
    def __call__(self):
        return self.simp
    
    def __str__(self):
        return f"""Id:\t{self.id}\nSimplified:\t{self.simp}\nTraditional:\t{self.trad}\nPinyin:\t{self.pinyin}\n"""

class Container:
    def __init__(self, kind):
        self.items = []
        self.kind = kind
        
    def __iter__(self):
        return ContainerIterator(self)
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __call__(self, length=20):
        for (i, el) in enumerate(iter(self)):
            print(el(), end=' ' if (i+1)%length!=0 else '\n')
        
    def append(self, item):
        assert isinstance(item, self.kind)
        self.items.append(item)
    
    def remove(self, item):
        self.items.remove(item)
    
    def get(self, attr):
        try:
            return [getattr(el, attr) for el in self.items]
        except:
            raise AttributeError
    
    def call(self, meth):
        try:
            return [getattr(el, meth)() for el in self.items]
        except:
            raise AttributeError
    
    def sort(self, attr):
        return sorted(self.get(attr))

class ContainerIterator:
    def __init__(self, container):
        self._index = 0
        self._container = container
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._container):
            x = self._index
            self._index += 1
            return self._container[x] 
        else:
            raise StopIteration