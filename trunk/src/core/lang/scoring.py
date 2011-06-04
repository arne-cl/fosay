__author__="zoltan kochan"
__date__ ="$1 груд 2010 1:13:17$"

from core.constants import is_terminalc

def get_tranarr(st):
    if st.type is None:
        raise Exception('%s has None type' % st.meaning)
    if is_terminalc(st.type):
        return st.transcription
    r = []
    for c in st.left + st.cblocks + st.right:
        t = get_tranarr(c)
        if t != None:
            r += t
    return r

def get_wordarr(st):
    if is_terminalc(st.type):
        return st.text
    r = []
    for c in st.left + st.blocks + st.right:
        if is_terminalc(c.type) and c.meaning == None: continue
        if get_wordarr(c) != None:
            r += get_wordarr(c)
    return r

ipa_vow = ["a", "e", "u", "i", "o", "ø", "ɒ", "ɛ", "ɪ", "ə", "æ"]

def eupony_score(lang, st):
    "Оцінює милозвучність текста"
    r = 0
    v = None
    for w in get_tranarr(st):
        if (v == None):
            v = w[-1] in ipa_vow
        elif (w in [",", "-", "."]):
            v = None
        else:
            v1 = w[0] in ipa_vow
            if (v1 != v): r += 1
            v = w[-1] in ipa_vow
    return r

def pithiness_score(lang, st):
    return -1*len(get_wordarr(st))

def direct_pithiness_score(lang, st):
    return -1*len(str(st))


def order_score(lang, st):
    return -1*st.renumerate()[1]

#cлова з меншою кількістю лексичних значень або
#з ближчими за значення лексичними значеннями отримують вищий бал
def unambiguity_score(lang, st):
    pass

def the_bests(lang, f, q):
    if q == []: return q
    ws = []
    for w in q:
        ws += [(f(lang, w), w)]
    ws = sorted(ws, key = lambda d: (d[0]), reverse = True)

    k = ws[0][0]
    i = 0
    px = []
    while i < len(ws) and (ws[i][0]) == k:
        px += [ws[i][1]]
        i += 1
    return px

import random

def the_best(lang, f, q):
    tmp = the_bests(lang, f, q)
    return tmp[random.randint(0, len(tmp)-1)]