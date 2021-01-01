#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:12:19 2021

@author: ivan
"""

ALLOW = [' ', '-', ',', '.']

def syllabary(inp):
    def single(char):
        unicode = ord(char)
        if 12353 <= unicode <= 12440:
            return 1
        elif 12449 <= unicode <= 12540:
            return 2
        elif 12288 <= unicode <= 12321:
            return 4
        elif char in ALLOW:
            return 5
        else:
            return 0
    
    cum = []
    for char in inp:
        cum.append(single(char))
    
    cum = [el for el in cum if el < 4]
    
    if all(el==cum[0] for el in cum):
        return cum[0]
    else:
        return -1