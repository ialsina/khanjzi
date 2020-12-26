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

class Container:
    
    def __init__(self, kind):
        self.items = []
        self.kind = kind
        
    def append(self, item):
        assert isinstance(item, self.kind)
        self.items.append(item)
    
    def get(self, attr):
        try:
            return [getattr(el, attr) for el in self.items]
        except:
            raise AttributeError
    