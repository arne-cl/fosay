__author__="zoltan kochan"
__date__ ="$28 june 2010 1:02:10$"

from core.lang.process import referencing
from core.lang.process import case_frame_to_lang, lang_to_case_frame, meaning_shift
from core.lang.scoring import eupony_score
from core.lang.scoring import pithiness_score
from core.lang.scoring import direct_pithiness_score
#from core.lang.scoring import order_score
from copy import deepcopy
from core.constants import concept


PRINT_TO_CONSOLE = False
prm_only_the_best = False
#UC = 35

def interlingua_to_str(dc, c = 0):
    d = 5
    b = d*c*" "
    b1 = b + d*" "
    res = b + "{" + "\n"
    for key in dc.keys():
        if dc[key] == None: continue
        if type(dc[key]) == list:
            if key == concept["tags"]:
                res += b1 + str(key) + ": " + ', '.join(dc[key]) + "\n"
            else:
                for item in dc[key]:
                    res += b1 + str(key) + ":" + "\n"
                    res += interlingua_to_str(item, c + 2)
        elif not isinstance(dc[key], int) and not isinstance(dc[key], str): #isinstance(dc, dict):!!!!!!!!!!
            res += b1 + str(key) + ":" + "\n"
            res += interlingua_to_str(dc[key], c + 2)
        else:
            res += b1 + str(key) + ": " + str(dc[key]) + "\n"
    return res + b + "}" + "\n"

def print_interlingua(dc, c = 0):
    d = 5
    b = d*c*" "
    b1 = b + d*" "
    print(b + "{")
    for key in dc.keys():
        if dc[key] == None: continue
        if type(dc[key]) == list:
            if key == concept["tags"]:
                print(b1 + str(key) + ":", ', '.join(dc[key]))
            else:
                for item in dc[key]:
                    print(b1 + str(key) + ":")
                    print_interlingua(item, c + 1)
        elif not isinstance(dc[key], int) and not isinstance(dc[key], str): #isinstance(dc, dict):!!!!!!!!!!
            print(b1 + str(key) + ":")
            print_interlingua(dc[key], c + 1)
        else:
            print(b1 + str(key) + ":", dc[key])
    print(b + "}")


from datetime import datetime

def text_to_interlingua(text, first, source_lang):
    """
    Translates the given text written on the source language
    into interlingua.
    """
    v = source_lang.init_sentence(text, first)
    for e in v:
        e.numerate(0)

    if PRINT_TO_CONSOLE:
        print()
        print("ways to understand", len(v))
#        print(v)
#        #tree = v[0]
    #begin_time = datetime.now()
    cfs = []
    for x in v:
        cfs += [lang_to_case_frame(x)]
    return cfs

def translate(text, first, source_lang, tlangs):
    d = datetime.now()
    #source_lang = slang
    target_langs = [x for x in tlangs]
    #source_lang =

    cfs = text_to_interlingua(text, first, source_lang)

    ###############cfs = [x for x in cfs if is_proper_case_frame(x)]
    cfs = [referencing(x) for x in cfs]
    if PRINT_TO_CONSOLE:
        print()
        for c in cfs:
            print_interlingua(c)
            print(190*"=")
            #print(c)
            print()

    #region TESTING FOR IDENTICAL CASE FRAMES
    id = 0
    for i in range(len(cfs) - 1):
        for j in range(i + 1, len(cfs)):
            #print(i, j)
            if str(cfs[i]) == str(cfs[j]):
                id += 1
    if PRINT_TO_CONSOLE:
        if id > 0: print("WARNING: there are", id, "identical caseframes\n")
    #endregion

    shift = 3 * " "
    #pr = "translating:\n" #print("translating:")
    #pr += shift + text + "\n" #print(shift + text)
    #pr += UC*"_" + "\n" #print(40*"=")

    #building_cf = datetime.now() - begin_time
    #begin_time = datetime.now()

    tr = []
    #ln = 1
    for target_lang in target_langs:
        if PRINT_TO_CONSOLE:
            print("translating to:", target_lang.name)
        #target_lang_syntax_trees = [case_frame_to_lang(x, target_lang) for x in cfs]
        target_lang_syntax_trees = []
        ct = 0
        loc_cfs = [meaning_shift(deepcopy(x), target_lang) for x in cfs]
        #print(loc_cfs) #
    #    print()
    #    for c in loc_cfs:
    #        print(c)
    #        print()
        for x in loc_cfs:
            temp = [y for y in case_frame_to_lang(x, target_lang, first)] #case_frame_to_lang(x, target_lang)
            ct += len(temp)
            target_lang_syntax_trees += [temp]
        if PRINT_TO_CONSOLE:
            print("alternatives:", ct)
    ##    ct = 0
    ##    for x in target_lang_syntax_trees:
    ##        if type(x) == list:
    ##            ct += len(x)
    ##        else:
    ##            ct += 1
    ##    #ct = sum(len(x) for x in target_lang_syntax_trees)
    ##    print(target_lang_syntax_trees, ct)
        #####################################
    #    ncf = []
    #    for x in target_lang_syntax_trees:
    #        nncf = []
    #        for c in x:
    #            nncf += [(eupony_score(target_lang, c), pithiness_score(target_lang, c), order_score(target_lang, c), c)]
    #        #nncf = sorted(nncf, key = itemgetter(1), reverse = True)
    #        nncf = sorted(nncf, key = lambda d: (d[1], d[0]), reverse = True)
    #        k = nncf[0][0], nncf[0][1]
    #        i = 0
    #        px = []
    #        while i < len(nncf) and (nncf[i][0], nncf[i][1]) == k:
    #            px += [nncf[i]]
    #            i += 1
    #        nncf = px
    #        ncf += [nncf]
    #NEM J?, MERT NEM N?ZI A CONJUNCTION-OKAT!!!!!!!!!!!!!!!!!!
    #among, after... like words with transcription!
        ncf = []
        for x in target_lang_syntax_trees:
            nncf = []
            if len(x) == 0:
                if PRINT_TO_CONSOLE:
                    print("WARNING: EMPTY ALTERNATIVE")
                continue

            for c in x:
                nncf += [(eupony_score(target_lang, c), pithiness_score(target_lang, c), direct_pithiness_score(target_lang, c), c)] #, order_score(target_lang, c)
            #nncf = sorted(nncf, key = itemgetter(1), reverse = True)
            #nncf = sorted(nncf, key = lambda d: (d[1], d[0], d[2]), reverse = True)
            nncf = sorted(nncf, key = lambda d: (d[1], d[2], d[0]), reverse = True)
            k = nncf[0][0], nncf[0][1], nncf[0][2]
            i = 0
            px = []
            while i < len(nncf) and (not prm_only_the_best or (nncf[i][0], nncf[i][1], nncf[i][2]) == k):
                px += [nncf[i]]
                i += 1
            nncf = px
            ncf += [nncf]
        ##########################################################

        #case_frame_to_lang(None, None)
        #cfs = [case_frame_to_lang(x, ukr) for x in cfs]

        #
        #if len(cfs) == 1:
        #    #we can teach Ester
        #    pass
        #else:
        #    #delete the uncorrect LLMs
        #    pass
        #
        #pr += "\n" #
        #print()
        #print cfs #english_to_case_frame(tree)

        #print cfs[0] #[str(x) for x in cfs]
        tl = []
        #pr += "translating to " + target_lang.name + ":\n" #; ln += 1 #print("translating #" + str(ln) + ":"); ln += 1
        for x in ncf:
            temp = 0
            for r, p, dr, t in x:
                #pr += shift + str(r) + ", " + str(p) + ": " + str(t) + "\n" #print((shift + str(ccfs[i])).encode("utf-8"))
                tl += [str(t)] #tl += [t]
                #pr += shift + str(t) + "\n" #print((shift + str(ccfs[i])).encode("utf-8"))
                temp += 1
            if PRINT_TO_CONSOLE:
                if temp > 1: print("There can't be more then one alternative with the same meaning!") #raise Exception("There can't be two alternatives with the same meaning!")
            #pr += "\n"
            #tkMessageBox.showinfo("Say Hello", str(ccfs[i]))
            #print(shift + str(r) + ": " + str(t))
        tr += [tl]
        if PRINT_TO_CONSOLE:
            print("translating duration =", datetime.now() - d)
            print()

    return tr
