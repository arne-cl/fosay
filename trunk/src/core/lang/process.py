__author__="zoltan kochan"
__date__ ="$28 june 2010 1:02:10$"
__name__ == "process"

from core.constants import INDEFINITE
from core.models.ling_units import *
from copy import deepcopy
import core.constants as const
from core.constants import concept, difinity, form
from core.constants import STATE_START, STATE_END, STATE_CONJ_A1, STATE_CONJ_A4
from core.constants import NONE
from core.constants import is_nonterminalc, is_terminalc, eqx, is_prop

from core.constants import quantity
from core.lang.scoring import *

PRINT_TO_CONSOLE = False

def gen_conj(lang, label, parent, f, fend, objs, conj):
    #print(len(objs))
    for word in unparse(lang, label, STATE_START, objs.pop(0)):
        #print('*')
        #print(word.descr())
        if len(objs) == 0:
            ts = lang.conj_str3(conj[0], conj[1], conj[2])
            if ts == []:
                ts = lang.conj_str(conj[0], conj[1])
            for c in ts:
                par = deepcopy(parent)
                par.relation = c
                tus = fend(lang, par, word) if fend else [par]
                for tt in tus:
                    yield tt
        else:
            par = deepcopy(parent)
            tus = f(lang, par, word) if f else [par]
            for tt in tus:
                for res in gen_conj(lang, label, tt, f, fend, deepcopy(objs), conj):
                    yield res

#best_res = None

###TODO:
required = {
    const.type["article"]: [concept["difinity"]],
    const.type["quantifier"]: [concept["quantity"]],
}#thh
##maybe use subtype instead of determinerType!!!!!!!!!!!!!!? Or not!!
#
def req(clabl, caseframe):
    if not clabl in required.keys():
        return True
    return all(x in caseframe.keys() and not caseframe[x] is None for x in required[clabl])

def find_maxposs(caseframe):
    res = 0
    for c in caseframe.keys():
        if not is_prop(c):
            if type(caseframe[c]) == type([]):
                res += len(caseframe[c])
            else:
                res += 1
    return res

#synthesize
def unparse(lang, label, state, caseframe, parent = None):
    "Uses generator to yield all possible sentences"
    if lang.to_type_code(label) == const.type["epsilon"]: ############
        yield None ##########################
    if caseframe == None:
        return
    
    if is_terminal(label):
        w = Token()
        w.set_ghost(is_empty(label))
        w.type = lang.to_type_code(label)
        for c in transferred_attributes[lang.to_type_code(label)]:
            if c == concept["real-number"] and not c in caseframe:
                continue
            w.attr(c, caseframe[c])
        yield w
    elif state == STATE_END:
        if all(is_prop(key) for key in caseframe.keys()):
            yield parent
    else:
        net = lang.atn[label]
        if not parent:
            parent = FlowerLingUnit(lang.to_type_code(label), 0, 0)

            for key in caseframe.keys():
                if is_prop(key):
                    parent.attr(key, caseframe.get(key, None))

        if lang.to_type_code(label) in caseframe and \
            type(caseframe[lang.to_type_code(label)]) == list and \
            concept["conj-function"] in caseframe and \
            not caseframe[concept["conj-function"]] is None:

            if not STATE_CONJ_A1 in net: return ###it is needed when we go on a way of an empty alternative. Like NP:EMPTY
            objs = caseframe[lang.to_type_code(label)]
            conj = caseframe[concept["conj-function"]], caseframe[concept["conj-type"]], caseframe[concept["conj-str"]]
            for x in gen_conj(lang, label, deepcopy(parent), net[STATE_CONJ_A1][0][1], net[STATE_CONJ_A4][1][1], deepcopy(objs), conj):
                yield x
        else:
            p = net[state]
            q = {}
            mp = find_maxposs(caseframe)

            for labl, f, standard, nextState, maxel, minel in p:
                if maxel != INDEFINITE and not maxel >= mp >= minel:
                    continue
                if standard in q.keys():
                    q[standard] += [(labl, f, nextState)]
                else:
                    q[standard] = [(labl, f, nextState)]

            q = [value for key, value in sorted(q.items(), key = lambda x: -1*x[0])]

            i = 0
            good_speed = False
            while not good_speed and i < len(q):
                for labl, f, nextState in q[i]:
                    if nextState == STATE_CONJ_A1: continue

                    cl = lang.to_type_code(labl)
                    if cl in modificators and req(cl, caseframe):
                        tmp = deepcopy(caseframe)
                        words = [(Token(cl), tmp)]
                    elif type(caseframe.get(cl)) == type([]):
                        words = []
                        for i in range(len(caseframe.get(cl))):
                            tmp = deepcopy(caseframe)
                            if len(tmp[cl]) == 1:
                                cf = tmp[cl][0]
                                del tmp[cl]
                            else:
                                cf = tmp[cl].pop(i)
                            words += [(word, deepcopy(tmp)) for word in unparse(lang, labl, STATE_START, cf, None)]
                    else:
                        tmp = deepcopy(caseframe)
                        if cl in tmp:
                            del tmp[cl]
                        words = [(word, deepcopy(tmp)) for word in unparse(lang, labl, STATE_START, caseframe.get(cl), None)]

                    for word, cf in words:
                        par = deepcopy(parent)
                        for x in f(lang, par, word) if f else [par]:
                            for rest in unparse(lang, label, nextState, deepcopy(cf), x):
                                good_speed = True
                                yield rest
                i += 1


def is_terminal(symbol):
    return not symbol[0].islower()
    #return symbol <= LAST_TERMINAL


def is_empty(n):
    return n[-6:].upper() == ":EMPTY"

def empty_type(n):
    return n[:-6]

def next_step(lang, label, state, mem, wc, parent, deep, u1, f):
    tus = f(lang, parent, u1) if f else [parent]
    for tt in tus:
        for mem, i2, u2 in parse(lang, label, state, mem, wc, tt, deepcopy(deep)): #deepcopy(deep) => deep
            yield mem, i2, u2

#match, analyze
def parse(lang, label, state, mem, wc = 0, parent = None, deep = None):
    if not deep: deep = {}
    #print(" "*4*deep.get(label, 0), label)
    if state == STATE_END:
        yield mem, wc, parent
    elif wc == len(mem):
        return
    elif is_terminal(label):
        if is_empty(label):
            w = Token(lang.to_type_code(empty_type(label)))
            w.set_ghost(True)
            #w.meaning = "_"
            yield mem, wc, w
        elif lang.to_type_code(label) == const.type["epsilon"]:
            yield mem, wc, None 
        elif label in mem[wc]:
            for w, l in mem[wc][label]:
                yield mem, l, w
    else:
        net = lang.atn[label]
        n = net[state]
        if not parent: parent = FlowerLingUnit(lang.to_type_code(label), 0, 0)
        m = [(deep.get(item[0], 0), item) for item in n]
        mr = [x[1] for x in sorted(m, key = lambda d: d[0])]
        for labl, f, standard, next_state, maxel, minel in mr:
            dp = deepcopy(deep)
            if labl in mem[wc]:
                for u1, to_ in mem[wc][labl]:
                    for mem, i2, u2 in next_step(lang, label, next_state, \
                    mem, to_, deepcopy(parent), deepcopy(deep), deepcopy(u1), f):
                        yield mem, i2, u2
            elif not labl in deep.keys() or deep[labl] < 3: #2                
                dp[labl] = 1 if not labl in dp.keys() else dp[labl] + 1
                tm = []
                
                #hogyha a maximalis mejseg elerese miat nem ad ki semmit akkor nem szabad beirni!! es amugy is at kel 
                #csinalni hogy ezen ne fugjon!
                for mem, i1, u1 in parse(lang, labl, STATE_START, \
                mem, wc, None, deepcopy(dp)):
                    tm += [(deepcopy(u1), i1)] #maybe witout deepcopy...
                    for mem, i2, u2 in next_step(lang, label, next_state, \
                    mem, i1, deepcopy(parent), deepcopy(deep), deepcopy(u1), f):
                        yield mem, i2, u2
                if dp[labl] == 1:
                    mem[wc][labl] = tm
            

def parse1(lang, label, state, mem, wc = 0):
    for x, y, z in parse(lang, label, STATE_START, mem, wc):
        mem = x
        if z:
            if not mem[wc].has_key(label):
                mem[wc][label] = [(z, y)]
        yield mem, y, z

def get_mem(lang, label, state, mem, wc = 0):
    for mem, y, z in parse1(lang, label, STATE_START, mem, wc):
        pass
    return mem



#TODO: Add required and default

min_str = {
    const.type["noun-phrase"]: [const.type["noun"]],
    const.type["epithet"]: [const.type["adjective"]],
    const.type["verb-phrase"]: [const.type["verb"]],
    const.type["clause"]: [const.type["subject"], const.type["verb-phrase"]]
    }

default_value = {
    concept["truth"]: 1.0
}

transferred_attributes = {
    const.type["noun"]:
    [
        concept["lemma"],
        concept["order-number"],
        concept["noun-type"],
        concept["real-number"],
        concept["form"],
        concept["tags"],
        concept["personal-name"],
    ],
    const.type["pronoun"]:
    [
        concept["lemma"],
        concept["order-number"],
        concept["noun-type"],
        concept["real-number"],
        concept["form"],
        concept["persone"],
        concept["gender"]
    ],
    const.type["adjective"]:
    [
        concept["lemma"],
        concept["order-number"],
    ],
    const.type["verb"]:
    [
        concept["lemma"],
        concept["order-number"],
    ],
    const.type["adverb"]:
    [
        concept["lemma"],
        concept["order-number"],
    ],

    const.type["sentence"]: [],
    const.type["clause"]: [],
    const.type["epithet"]: [],
    const.type["verb-phrase"]:
    [
        concept["tense"],
        concept["mood"],
        concept["aspect"],
        concept["truth"]
    ],
    const.type["noun-phrase"]:
    [
        concept["persone"],
        concept["difinity"],
        concept["quantity"],
        concept["quantity-number"],
    ],
    const.type["time"]:
    [
        concept["tense"],
    ],
    const.type["subject"]: [],#[concept["case"]],
    const.type["inessive"]: [],#[concept["case"]],
    const.type["illative"]: [],#[concept["case"]],
    const.type["elative"]: [],#[concept["case"]],
    const.type["accusative"]: [],#[concept["case"]],
    const.type["possessive"]: [],#[concept["case"]],
    const.type["preposition-phrase"]: [],
}

default = {
    concept["form"]: form["formal"] ##########
}

exclusions = [
    concept["difinity"],
    concept["quantity"],
    concept["quantity-number"]
]

def lang_to_case_frame(unit):
    '''Translates the source language AST to Interlingua'''
    cf = {}
    if is_terminalc(unit.type):
        for c in transferred_attributes[unit.type]:
            cf[c] = unit.attr(c)
            if cf[c] == None and c in default.keys():
                cf[c] = default[c]
    elif len(unit.blocks) > 1 and not unit.relation is None:
        t = unit.blocks[0].type
        cf[concept["conj-str"]] = unit.relation.conj_str
        cf[concept["conj-type"]] = unit.relation.conj_type
        cf[concept["conj-function"]] = unit.relation.function_number
        cf[t] = [lang_to_case_frame(y)[y.type] for y in unit.blocks]
    else:
        for e in unit.left + unit.right:
            if not e.type in modificators: ##and (e.type != TERMINAL_DETERMINER or not e.attr(concept["difinity"])): #OR JUST TERMINAL_ARTICLE
                cf.update(lang_to_case_frame(e))
        for c in transferred_attributes[unit.type]:
            if unit.attr(c) == None:
                if c in default_value:
                    cf[c] = default_value[c]
                elif not c in exclusions:
                    print(unit.type, c)
                    raise NotImplementedError
                    #continue
            cf[c] = unit.attr(c)

        if len(unit.blocks) == 1:
            if not cf.get(concept["quantity"], None) in [None, NONE]:
                transferred_attributes[const.type["noun"]].remove(concept["real-number"])
            cf.update(lang_to_case_frame(unit.blocks[0]))
            if not cf.get(concept["quantity"], None) in [None, NONE]:
                transferred_attributes[const.type["noun"]].append(concept["real-number"])
        else:
            for b in unit.blocks:
                if b.type in cf:
                    cf[b.type] += [lang_to_case_frame(b)[b.type]]
                else:
                    cf[b.type] = [lang_to_case_frame(b)[b.type]]

#        #mosaic translation
#        if not curr_type in cf.keys():
#            for i in min_str.get(curr_type, []):
#                if not i in cf.keys():
#                    print(str(i), str(curr_type), cf)
#                    raise NotImplementedError()

    return {unit.type: cf}

def nouns(cf, ord = None):
    p = []
    #print(cf)
    for key in cf.keys():
        if key == const.type["noun-phrase"]:
            if concept['conj-str'] in cf[key].keys():
                for x in cf[key][key]:
                    if const.type["noun"] in x.keys():
                        p += [(x[const.type["noun"]].get(concept["order-number"], None) if ord == None else ord, x)]
                    elif const.type["pronoun"] in x.keys():
                        p += [(x[const.type["pronoun"]].get(concept["order-number"], None) if ord == None else ord, x)]
                    elif const.type["noun-phrase"] in x.keys():
                        p += nouns(x, cf[key].get(concept["order-number"], None))
            else:
                if const.type["noun"] in cf[key].keys():
                    if type(cf[key][const.type["noun"]]) == type([]):
                        for item in cf[key][const.type["noun"]]:
                            p += [(item.get(concept["order-number"], None) if ord == None else ord, {key: item})]
                    else:
                        p += [(cf[key][const.type["noun"]].get(concept["order-number"], None) if ord == None else ord, cf[key])]
                elif const.type["pronoun"] in cf[key].keys():
                    p += [(cf[key][const.type["pronoun"]].get(concept["order-number"], None) if ord == None else ord, cf[key])]
                elif const.type["noun-phrase"] in cf[key].keys():
                    p += nouns(cf[key], cf.get(concept["order-number"], None))


        elif is_nonterminalc(key):
            p += nouns(cf[key], cf.get(concept["order-number"], None))
    return p

#def nouns(cf, ord = None):
#    p = []
#    for key in cf.keys():
#        if not is_nonterminalc(key):
#            continue
#        if const.type["noun"] in cf[key].keys():
#            p += [(cf[key][const.type["noun"]].get(concept["order_number"], None) if ord == None else ord, cf[key])]
#        elif const.type["pronoun"] in cf[key].keys():
#            p += [(cf[key][const.type["pronoun"]].get(concept["order_number"], None) if ord == None else ord, cf[key])]
#        p += nouns(cf[key], cf.get(concept["order_number"], None))
#    return p

#there can't be pronouns in the case frame. (And general words should be changed with proper ones if it's possible)
def referencing(cf): #words
    #print(cf)
    p = [x[1] for x in sorted(nouns(cf), key = lambda d: (d[0]))]
    #print(p)
    i = 0
    while i < len(p):
        if const.type["noun"] in p[i].keys():
            j = i + 1
            if p[i].get(concept["quantity"], None) == quantity["none"] and p[i].get(concept["difinity"], None) == None:
                if p[i][const.type["noun"]][concept["noun-type"]] == noun_type["proper"]:
                    p[i][concept["difinity"]] = difinity["difinite"]
                else:
                    p[i][concept["difinity"]] = difinity["undifinite"]
            while j < len(p):
                if const.type["noun"] in p[j].keys() and \
                p[j][const.type["noun"]][concept["lemma"]] == p[i][const.type["noun"]][concept["lemma"]] and \
                p[i].get(concept["quantity"], None) == quantity["none"] and \
                p[j].get(concept["difinity"], None) == None:
                    p[j][concept["difinity"]] = difinity["difinite"]
                    del p[j]
                else:
                    j += 1
        i += 1
    #print("------------>", p)
    return cf








#choosing the ones that match better the tags
def eq_score(a, b):
    id = 0
    t1 = [] if a is None else a
    t2 = [] if b is None else b
    for i in t1:
        for j in t2:
            if i == j:
                id += 1
    if id == 0:
        return -(len(t1)+len(t2))
    return id

def props_score(token, st):
    s = 0
    for key in st._attrs.keys():
        if key == concept["tags"] or token.attr(key) == st.attr(key):
            s += 1
    return s

#choosing the ones that match better
def tbt(tokens, st):
    nncf = []
    if len(tokens) == 0:
        return []
    for c in tokens:
        nncf += [(eq_score(c.attr(concept["tags"]), st.attr(concept["tags"])),
            props_score(c, st), c)]
    nncf = sorted(nncf, key = lambda d: (d[0], d[1]), reverse = True)
    k = nncf[0][0], nncf[0][1]
    #print(k)
    i = 0
    px = []
    while i < len(nncf) and (nncf[i][0], nncf[i][1]) == k:
        px += [nncf[i][2]]
        i += 1
    return px

def is_empty_word(w):
    return w.get_ghost()

def pre_morphen(lang, st, ind = 0):
    '''Init's the main morpho-groups before doing morphological generation'''
    st.parent = None
    if is_terminalc(st.type):
        if not st.fixed or is_empty_word(st):
            yield st
            return
        rr = [x for x in lang.words if all(y == concept["tags"] or eqx(y, x, st) for y in concept)] #musteq
        rr = tbt(rr, st)
        newr = []
        if PRINT_TO_CONSOLE and len(rr) > 1: print("CAUTION: Ambiguity in 'pre_morphen' at %s" % st.descr())
        for r in rr:
            for nr in newr:
                for f in st.fixed:
                    if r.attr(f) != nr.attr(f):
                        break
                else:
                    break
            else:
                for f in st.fixed: #################################################
                    if r.attr(f) == NONE:
                        print("xxxxxxxxxxxpre_morphenpre_morphenpre_morphenpre_morphen")
                        break#############################################################################################################################
                else:
                    newr += [r]
        rr = newr
        if rr == []:
            return
        for r in rr:
            c = deepcopy(st)
            for f in c.fixed:
                c.attr(f, r.attr(f))
            yield c
        return

    res = []
    for x in pre_morphen(lang, (st.left + st.blocks + st.right)[ind]):
        c = deepcopy(st)
        if ind < len(c.left):
            c.left[ind] = x
        elif ind < len(c.left + c.blocks):
            c.blocks[ind - len(c.left)] = x
        else:
            c.right[ind - len(c.left + c.blocks)] = x
        x.parent = c
        if not x.refresh(): continue
        res += [c]

    res = the_bests1(lang, eupony_score, res)

    for c in res:
        if ind + 1 == len(c.left + c.blocks + c.right):
            yield c
        else:
            for y in pre_morphen(lang, c, ind + 1):
                yield y

def morphen(lang, st, ind = 0):
    '''Morphological generation'''
    st.parent = None
    if is_terminalc(st.type):
        if is_empty_word(st):
            yield st
            return

        rr = [x for x in lang.words if all(y == concept["tags"] or eqx(y, x, st) for y in concept)] #musteq
        rr = tbt(rr, st)

        if rr == [] or rr is None: raise Exception("Not found in the '%s' dictionary %s" % (lang.name,  st.descr()))
        if PRINT_TO_CONSOLE and len(rr) > 1:
            tmp = str([x.descr() for x in rr])
            print("CAUTION: Ambiguity in 'morphen' at %s alternatives %d (%s)" % (st.descr(), len(rr), tmp))
        for r in rr:
            c = deepcopy(st)
            c.text = r.text
            c.transcription = r.transcription
            for p in concept: c.attr(p, r.attr(p))
            yield c
        return
    res = []
    for x in morphen(lang, (st.left+st.blocks+st.right)[ind]):
        c = deepcopy(st)
        if ind < len(c.left):
            c.left[ind] = x
        elif ind < len(c.left + c.blocks):
            c.blocks[ind - len(c.left)] = x
        else:
            c.right[ind - len(c.left + c.blocks)] = x
        x.parent = c
        if not x.refresh():
            continue
        res += [c]

    res = the_bests1(lang, eupony_score, res)
    for c in res:
        if ind + 1 == len(c.left+c.blocks+c.right):
            yield c
        else:
            for y in morphen(lang, c, ind + 1):
                yield y

def case_frame_to_lang(caseframe, target_lang, first=const.type['sentence']):
    '''Translates Interlingua to the target language AST'''
    for first_label in target_lang.type_labels(first):
        for x in unparse(target_lang, first_label, STATE_START, caseframe[first]):
            for y in pre_morphen(target_lang, x):
                for z in morphen(target_lang, y):
                    yield z