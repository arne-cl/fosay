__author__="zoltan kochan"
__date__ ="$1 груд 2010 1:13:17$"

from core.constants import is_terminalc

def get_tranarr(st):
    if is_terminalc(st.type):
        return st.transcription
    r = []
    for c in st.left + st.cblocks + st.right:

        #r += get_tranarr(c)

        t = get_tranarr(c)
        if t != None:
            r += t
    return r

def get_wordarr(st):
    if is_terminalc(st.type):
        return st.text
    r = []
    for c in st.left + st.blocks + st.right:
        ###
        if is_terminalc(c.type) and c.meaning == None: continue
        ###
        if get_wordarr(c) != None:
            r += get_wordarr(c)
        #else:
        #    r += [0]
    return r

#def _eupony_score(st, r, v = None):
#    if is_terminalc(st.type):
#        if (v == True and )
#        pass
#    else:
#        for c in st.left + st.blocks + st.right:
#            pass

ipa_vow = ["a", "e", "u", "i", "o", "ø", "ɒ", "ɛ", "ɪ", "ə", "æ"]

def eupony_score(lang, st):
    "Оцінює милозвучність текста"
    r = 0
    v = None
    #print(get_wordarr(st))
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

#def pithiness_score1(lang, st):
#    return -1*len(str(st))



def order_score(lang, st):
    return -1*st.renumerate()[1]

#cлова з меншою кількістю лексичних значень або з ближчими за значення лексичними значеннями отримують вищий бал
def unambiguity_score(lang, st):
    pass















def the_bests9(lang, f1, f2, q):
    if q == []: return q
    ws = []
    for w in q:
        ws += [(f1(lang, w[1]), f2(lang, w[1]), w)]
    ws = sorted(ws, key = lambda d: (d[0], d[1]), reverse = True)

    i = 0
    px = []
    b = 2 ######
    while i < len(ws):
        k = ws[i][0], ws[i][1]
        pp = []
        while i < len(ws) and abs(ws[i][0] - k[0]) <= b and abs(ws[i][1] - k[1]) <= b:
            pp += [ws[i][2]]
            i += 1
        px += [pp]
    return px

def the_bests0(lang, f, q):
    if q == []: return q
    ws = []
    for w in q:
        ws += [(f(lang, w[2]), w)]
    ws = sorted(ws, key = lambda d: (d[0]), reverse = True)

    i = 0
    px = []
    while i < len(ws):
        k = ws[i][0]
        pp = []
        while i < len(ws) and ws[i][0] == k:
            pp += [ws[i][1]]
            i += 1
        px += [pp]
    return px

def the_bests(lang, f, q):
    if q == []: return q
    ws = []
    for w in q:
        ws += [(f(lang, w[2]), w)]
    ws = sorted(ws, key = lambda d: (d[0]), reverse = True)

    k = ws[0][0]
    i = 0
    px = []
    while i < len(ws) and ws[i][0] == k:
        px += [ws[i][1]]
        i += 1
    return px

#THE PROPER ONE!!!!!!!!!
def the_bests1(lang, f, q):
    #print("xxx")
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