#-------------------------------------------------------------------------------
# ATN generator. Contains functions for generating ATN.
#-------------------------------------------------------------------------------
__author__="zoltan kochan"
__date__ ="$26 лист 2010 1:49:08$"

from core.constants import STATE_START
from core.constants import STATE_END
from core.constants import type as ltype
from core.constants import modificators
from core.constants import preqconst
from core.constants import STATE_CONJS, STATE_CONJ_A1, STATE_CONJ_A2, STATE_CONJ_A3, STATE_CONJ_A4
from core.constants import INDEFINITE
from core.constants import position
from core.constants import conj_str
from copy import deepcopy

def betwcheck(lang, pr, ch): #if it returns True then the model isn't proper
    return not (pr.relation and (pr.relation.max_items and pr.relation.max_items < len(pr.blocks) or \
        ch.relation == pr.relation or \
        ch.relation and pr.relation.order < ch.relation.order))

def has_nothing_conj(conjs, pr):
    for c in conjs:
        if c.conj_str == conj_str['nothing']:
            pr.relation = c
            return True
    return False

def aftercheck(lang, pr, ch): #if it returns True then the model isn't proper
    return not (not pr.relation and not has_nothing_conj(lang.conjunctions, pr) or pr.relation and \
        (pr.relation.max_items and pr.relation.max_items < len(pr.blocks) or \
        pr.relation == ch.relation or len(pr.blocks) > 0 and (pr.blocks[0].relation == pr.relation or \
        pr.blocks[0].relation and pr.relation.order < pr.blocks[0].relation.order)))

def return_parent(lang, parent, child):
    return [parent]

def add_to_blocks(lang, parent, child):
    parent.blocks += [child]
    child.parent = parent
    if not child.refresh():
        return []
    return [parent]

def add_to_blocks_wr(lang, parent, child):
    parent.blocks += [child]
    child.parent = parent
    return [parent]

def add_to_lorr(lang, parent, child):
    if parent.blocks == []:
        parent.left += [child]
    else:
        parent.right += [child]
    child.parent = parent
    if not child.refresh():
        return []
    return [parent]

def add_to_left(lang, parent, child):
    parent.left += [child]
    child.parent = parent
    if not child.refresh():
        return []
    return [parent]

def add_to_right(lang, parent, child):
    parent.right += [child]
    child.parent = parent
    if not child.refresh():
        return []
    return [parent]

def add_to_conj_struct_before(lang, parent, conj):
    if conj.position != Position.BEFORE or \
        not parent.type in [x.type for x in conj.conjuction_structure.por]:
        return []
    parent.relation = conj.conjuction_structure
    return [parent]

def add_to_conj_struct_among(lang, parent, conj):
    if conj.position != position["among"] or \
        not parent.type in conj.conjuction_structure.por:
        return []
    if not parent.relation:
        if conj.conjuction_structure.before != None:
            return []
        parent.relation = conj.conjuction_structure
        return [parent]
    elif parent.relation != conj.conjuction_structure:
        return []
    return [parent]

def add_to_conj_struct_after(lang, parent, conj):
    pass

def fg_bch(af):
    return \
        lambda lang, par, ch: \
            add_to_blocks_wr(lang, par, ch) \
            if ch.add_attach(af.get('attach', [])) and \
                ch.add_fixed(af.get('fixed', [])) and \
                betwcheck(lang, par, ch) \
            else []

def fg_ach(af):
    return \
        lambda lang, par, ch: \
            add_to_blocks(lang, par, ch) \
            if ch.add_attach(af.get('attach', [])) and \
                ch.add_fixed(af.get('fixed', [])) and \
                aftercheck(lang, par, ch) \
            else []


def fgen(f = add_to_lorr, attach=[], fixed=[], up=[], down=[]):
    '''Generates a standard arc-function.'''
    return lambda lang, par, ch: \
        f(lang, par, ch) \
        if \
        all(preqconst(x, ch, y) for x, y in down) and \
        all(preqconst(x, par, y) for x, y in up) and \
        (ch == None and attach == fixed == [] or \
        ch.add_attach(attach) and \
        ch.add_fixed(fixed)) \
        else []

def fcomma(lang, p, c):
    return []

def fconjmp(lang, p, c):
    return []



from itertools import combinations, permutations

def all_combinations(p, lp):
    res = []
    for i in range(0, lp + 1):
        res += combinations(p, i)
    return res

def to_function(func):
    '''Generates function from lex info dictionary.'''
    if type(func) == dict:
        return fgen(
            f = to_function(func.get('f', add_to_lorr)),
            fixed = func.get("fixed", []),
            attach = func.get("attach", []),
            down = func.get("down", []),
            up = func.get("up", [])
        )
    else:
        return func

def dicts_to_funcs(atn):
    '''Generates functions from all lex info dictionaries in the ATN.'''
    natn = {}
    for atnkey in atn:
        states = atn[atnkey]
        nstates = {}
        for statekey in states:
            state = states[statekey]
            new_state = []
            for item in state:
                new_state += [(item[0], to_function(item[1]), item[2], item[3])]
            nstates[statekey] = new_state
        natn[atnkey] = nstates
    return natn

def any_sequence(atn, optional, maxop = None, standard = 1.0, standard_seqs = [],
        starts = STATE_START, ends = STATE_END):
    '''Generates an ATN in which the states can be achieved in any sequence.'''
    maxop = len(optional) if maxop is None else maxop

    res = {}

    #print([x for x in combinations_without_reiterations(atn)])
    res[starts] = []

    #print([x for x in combinations_without_reiterations(optional)])
    shift = starts
    #for q in combinations_without_reiterations(optional):
    for q in all_combinations(optional, maxop):
        t = atn + [[i[0]] for i in q if len(i) > 0]
        for r in permutations(t, len(t)):
            curr = [m[0][0] for m in r]
            #print(curr)
            #if any([ss == curr for ss in standard_seqs]): print(curr)
            stn = standard if any([ss == curr for ss in standard_seqs]) else 0.0
            #print(stn)
            #print(",,,,,,",r)
            shift += 1
            #res[starts] += [("JMP", shift + 1, None)]
            #it would work with left too. (left = True)
            j = 1

            p = r[0]

            if j == len(r):
                next = ends
            else:
                next = shift + j + 1

            for m in p:
                res[starts] += [(m[0], m[1], stn, next)]





            j += 1
            for p in r[1:]:

                res[shift + j] = []
                if j == len(r):
                    next = ends
                else:
                    next = shift + j + 1

                for m in p:
                    res[shift + j] += [(m[0], m[1], stn, next)]
                j += 1
            shift += len(t)
            #stn = 0.0

    #print(len(res[1]), res)
    #res = compr(res)
    return res

def equal_dfuncs(f, g):
    '''Retuns true if two dictionaries with lexical info are equal.'''
    if None in [f, g]:
        return f is None and g is None
    return f.get('f', None) == g.get('f', None) and \
        set(f.get('up', [])) == set(g.get('up', [])) and \
        set(f.get('down', [])) == set(g.get('down', [])) and \
        set(f.get('attach', [])) == set(g.get('attach', [])) and \
        set(f.get('fixed', [])) == set(g.get('fixed', []))

def compr(res, dug=False):
    '''Compress's ATN state sequences.
        @dug - delete unreachable groups from way.'''
    on_way = set([(STATE_START, STATE_START)])
    for key in [x for x in sorted(res.keys())]:#sorted(res.keys()):
        if not key in res.keys():
            continue
        i = 0
        while i < len(res[key]) - 1:
            j = i + 1
            while j < len(res[key]):
                if res[key][i][3] <= res[key][j][3]:
                    ti = i
                    tj = j
                else:
                    ti = j
                    tj = i
                if res[key][ti][0] == res[key][tj][0] and \
                   res[key][ti][2] == res[key][tj][2] and \
                   (not STATE_END in [res[key][ti][3], res[key][tj][3]] or
                   STATE_END == res[key][ti][3] == res[key][tj][3]) and \
                   equal_dfuncs(res[key][ti][1], res[key][tj][1]):

                    if res[key][ti][3] != STATE_END:
                        res[res[key][ti][3]] += res[res[key][tj][3]]
                        res[key][ti] = (
                            res[key][ti][0],
                            res[key][ti][1],
                            res[key][ti][2],#max(res[key][tj][2], res[key][ti][2]),
                            res[key][ti][3]
                        )
                        del res[key][tj]
                    else:
                        if res[key][tj][2] <= res[key][ti][2]:
                            del res[key][tj]
                        else:
                            del res[key][ti]
                else:
                    j += 1
            on_way.add((key, res[key][i][3]))
            i += 1
        on_way.add((key, res[key][-1][3]))

    # delete unreachable groups from on_way
    if dug:
        nw = []
        next = [STATE_START]
        while next != []:
            nnext = []
            for p, n in on_way:
                if n > p and p in next:
                    nnext += [n]
            nw += next
            next = nnext
    else:
        nw = [n for p, n in on_way]
    

    # deleting unreachable states
    for key in [x for x in res]:
        if not key in nw:
            del res[key]
    return res


def can_jump(label, func=None, next=None):
    '''When the 'label' state is not obvious'''
    if next is None:
        return [(label, func, 0.0),
            ("JMP", None, 0.0)]
    return [(label, func, 0.0, next),
            ("JMP", None, 0.0, next)]

def jump(next):
    return ("JMP", None, next)

def _add_row(d, num, next, m):
    if not num in d.keys():
        d[num] = []
    for item in m:
        if len(item) == 1 or type(item) != tuple:
            tmp = item[0] if type(item) == tuple else item
            label = tmp
            func = None
            standard = 0.0
            shift = 0
        elif len(item) == 2:
            label, func = item
            standard = 0.0
            shift = 0
        elif len(item) == 3:
            if not is_float(item[2]):
                label, func, shift = item
                standard = 0.0
                shift -= 1
            else:
                label, func, standard = item
                shift = 0
        else:
            raise Exception(item)
        if next == STATE_END:
            shift = 0
        d[num] += [(label, func, standard, next + shift)]

def straight_sequences(xx):
    d = {}
    st = STATE_START + 1
    for x in xx:
        i = st
        _add_row(d, STATE_START, i if len(x) > 1 else STATE_END, x[0])
        for m in x[1:]:
            j = i + 1
            if i - st + 2 == len(x):
                st = j
                j = STATE_END
            _add_row(d, i, j, m)
            i = j
    return d

def straight_sequence(x):
    return straight_sequences([x])

def single(x):
    return straight_sequences([[x]])

def unite(b1, b2):
    '''Adds a way which starts at the begining.'''
    if STATE_CONJ_A1 in b1 and \
        STATE_CONJ_A1 in b2:
            raise Exception("INTERNAL ERROR: Can't unite to ways with conjunctions.")
    a1, a2 = deepcopy(b1), deepcopy(b2)
    shift = max(a1.keys()) - 1
    for label, f, standard, next in a2[STATE_START]:
        nxt = next + shift if next != STATE_END else next
        a1[STATE_START] += [(label, f, standard, nxt)]
    del a2[STATE_START]
    for key in a2.keys():
        new = key + shift if not key in STATE_CONJS else key
        a1[new] = []
        for label, f, standard, next in a2[key]:
            nxt = next + shift if next != STATE_END else next
            #if nxt == 18740: print(next, shift, STATE_END)
            a1[new] += [(label, f, standard, nxt)]
    #print("------", a1)
    return a1

def is_float(b):
    return type(b) == float# b is True or b is False

def to_full_atn(atn):
    '''Adds the missing parts of the ATN.'''
    for key in atn.keys():
        for k in atn[key].keys():
            if not k + 1 in atn[key].keys():
                next = STATE_END
            else:
                next = k + 1
            temp = []
            for i in atn[key][k]:
                if len(i) == 1:
                    temp += [(i[0], None, 0.0, next)]
                elif len(i) == 2:
                    temp += [(i[0], i[1], 0.0, next)]
                elif len(i) == 3:
                    if is_float(i[2]):
                        temp += [(i[0], i[1], i[2], next)]
                    else:
                        temp += [(i[0], i[1], 0.0, i[2])]
                elif len(i) == 4:
                    temp += [i]
                else:
                    raise Exception(str(i))
            atn[key][k] = temp
    return atn

POSITIVE_INFINITY = float('inf')

def subnet_deepness(atn, to_type_code, num = STATE_START):
   #7 iyui78i
    if num == STATE_END:
        return atn, 0, 0
    mx = -1
    mn = POSITIVE_INFINITY
    for i in range(len(atn[num])):
        item = atn[num][i]
        if item[3] != STATE_CONJ_A1 and item[3] <= num:
            mx = INDEFINITE
            mn = INDEFINITE
            atn[num][i] = atn[num][i][0], atn[num][i][1], atn[num][i][2], atn[num][i][3], mx, mn
            continue
        atn, mxtmp, mntmp = subnet_deepness(atn, to_type_code, item[3])
        mxtmp += 0 if to_type_code(item[0]) in modificators + [ltype["epsilon"]] else 1
        mntmp += 0 if to_type_code(item[0]) in modificators + [ltype["epsilon"]] else 1
        atn[num][i] = atn[num][i][0], atn[num][i][1], atn[num][i][2], atn[num][i][3], mxtmp, mntmp
        mx = max(mxtmp, mx)
        mn = min(mntmp, mn)
    return atn, mx, mn

def init_weights(atn, to_type_code):
    '''Initializes the maximum and minimum number of tokens
        that can be on the rest of the way.'''
    for key in atn.keys():
        atn[key], mx, mn = subnet_deepness(atn[key], to_type_code)
    return atn

def finish_atn(atn, to_type_code):
    atn = to_full_atn(atn)
    for key in atn:
        atn[key] = compr(atn[key])
    return init_weights(dicts_to_funcs(atn), to_type_code)


def with_conj(key, w, d):
    '''Adds the ability to be tied with conjunctions to the structure.'''
    if STATE_CONJ_A1 in d:
        raise Exception('Only one conjstruct is possible for one subATN now.')
    d[STATE_START] += [("JMP", None, 0.0, STATE_CONJ_A1)]
    d[STATE_CONJ_A1] = [(key, fg_bch(w), 0.0, STATE_CONJ_A2)]
    d[STATE_CONJ_A2] = [("PUNCT", fcomma, 0.0, STATE_CONJ_A3), ("JMP", None, 0.0, STATE_CONJ_A3)]
    d[STATE_CONJ_A3] = [("CONJ", add_to_conj_struct_among, 0.0, STATE_CONJ_A4), ("JMP", fconjmp, 0.0, STATE_CONJ_A4)]
    d[STATE_CONJ_A4] = [(key, fg_bch(w), 0.0, STATE_CONJ_A2), (key, fg_ach(w), 0.0, STATE_END)]
    return d