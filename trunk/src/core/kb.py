 # -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Knowladge base
#-------------------------------------------------------------------------------
__author__="zoltan kochan"
__date__ ="$28 june 2010 1:02:10$"

from core.models.ling_units import *
import core.constants as const
from core.constants import type as ltype
from core.constants import is_terminalc
from core.models.lang import Language
from core.lang.process import lang_to_case_frame

PRINT_TO_CONSOLE = False

jbo = Language("jbo")

#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM#ANTONYM
#antonym = [
#    ("man", "woman"),
#    ("girl", "boy"),
#]

#IS-A (is a type of)
SUPERTYPE = "@supertype"
SUBTYPE = "@subtype"



#IN CASE FRAME!!!!!!!!!!!!!
#diff = [
#    ("mensi", "fema tunba"), #("fem-tunba", ["fema tunba"]),
#    ("bruna", "mefa tunba"), #("mef-tunba", ["mefa tunba"]),
#    ("tunba", "mensi o bruna"),
##
##    ("homino", "fema homo"),
##    ("homulo", "mefa homo"),
##
##    ("yun-homo", "yuna homo"),
#    ("yun-homulo", "yuna homulo"), #boy = young male human
##    ("yun-homino", "yuna homino"),
##
##    ("adult-homo", "adulta homo"),
##    ("adult-homulo", "adulta homulo"),
##    ("adult-homino", "adulta homino"),
##
##    ("pordoc", "pordo", "pordos"),
##    ("pordos", "multa pordo"), #or more than one "pordo"
#
#]
diff = [
    ("mensi", "fetsi tunba"), #("fem-tunba", ["fema tunba"]),
    ("bruna", "nakni tunba"), #("mef-tunba", ["mefa tunba"]),
    ("tunba", "mensi a bruna"), #.inajo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#    ("homino", "fema homo"),
#    ("homulo", "mefa homo"),
#
#    ("yun-homo", "yuna homo"),
#    ("yun-homulo", "yuna homulo"), #boy = young male human
#    ("yun-homino", "yuna homino"),
#
#    ("adult-homo", "adulta homo"),
#    ("adult-homulo", "adulta homulo"),
#    ("adult-homino", "adulta homino"),
#
#    ("pordoc", "pordo", "pordos"),
#    ("pordos", "multa pordo"), #or more than one "pordo"

]

def gen_cf_diff(diff):

    #raise NotImplementedError
    #intlin = Language("jbo")#.......
    temp = {}
    for w, d in diff:
        st = jbo.init_sentence(d, "np")
        #if len(st) > 1:
        #    raise NotImplementedError
        temp[w] = lang_to_case_frame(st[-1])
        if PRINT_TO_CONSOLE:
            print(5*" ", w, "<=>", temp[w])
    return temp
    #but without dict

cf_diff = gen_cf_diff(diff)

###cf_diff = {
###    "yun-homo": {NONTERMINAL_EPITHET: {TERMINAL_ADJECTIVE: {CONCEPT_MEANING: "yuna"}}}
###    }

#diff = [
#    ("mensi", ["fema tunba"]), #("fem-tunba", ["fema tunba"]),
#    ("bruna", ["mefa tunba"]), #("mef-tunba", ["mefa tunba"]),
#    ("tunba", ["mensi", "bruna"]),
#
#    ("homino", ["fema homo"]),
#    ("homulo", ["mefa homo"]),
#
#    ("yun-homo", ["yuna homo"]),
#    ("yun-homulo", ["yuna homulo"]), #boy = young male human
#    ("yun-homino", ["yuna homino"]),
#
#    ("adult-homo", ["adulta homo"]),
#    ("adult-homulo", ["adulta homulo"]),
#    ("adult-homino", ["adulta homino"]),
#
#    ("pordoc", ["pordo", "pordos"]),
#    ("pordos", ["multa pordo"]), #or more than one "pordo"
#
#]

types_hierarchy = [
    ("tunba", "mensi"),
    ("tunba", "bruna"),
    ("state", "like"),
    ("entity", "animate"),
    ("entity", "physical object"),
    ("animate", "animalo"),
    ("animalo", "hundo"),
    ("animalo", "hom'e"),
    ("hom'e", "homa"),
    ("evento", "akto"),
    ("akto", "bite"),
    ("tcika", "lunto"),
    ("tcika", "solto"),
    ("tcika", "avroro"), #dawn
    ("tcika", "mateno"), #morning #IT'S NOT A TYPE OF DAYTIME!! RATHER A PART OF
    ("tcika", "medisolto"), #noon #media solto #IT ALSO MEANS MIDNIGHT!!! I MUST USE AN ARTIFICIAL LANGUAGE!!!
    ("tcika", "posmeso"), #afternoon
    ("tcika", "vespero"),
    ("tcika", "medilunto"), #midnight
    ("tcika", "momento"),
    ("tcika", "milisekondo"),
    ("tcika", "snidu"),
    ("tcika", "mentu"),
    ("tcika", "cacra"),
    ("tcika", "djedi"), #"day" like day and night
    ("djedi", "padjed"), #monday
    ("tcika", "jeftu"), #week
    ("tcika", "masti"), #month
    ("tcika", "citsi"), #season
    ("tcika", "semestro"), #semester
    ("tcika", "anio"), #year
    ("tcika", "tsentano"), #century
    ("tcika", "milenio"), #millenium
    ("tcika", "epoko"), #era
    ("loko", "lokalito"), #place
    ("lokalito", "viladjeto"), #locality, hamlet
    ("lokalito", "viladjo"), #
    ("lokalito", "viladjego"), #urban village
    ("lokalito", "urbeto"), #town
    ("lokalito", "urbo"), #city
    ("lokalito", "urbego"), #megapolis
    ("loko", "lando"),
    ("lando", "la ukrayina"),
    ("lando", "la m'ady'arorsag"),
    ("lando", "la rasiya"),
    ("lando", "la slovakiya"),
    ("lando", "la gr'eyt brit'eyn"),
    ("urbego", "la lyviv"),
    ("urbego", "la k'eyiv"),
]

def is_supertype(sup, sub):
    if sup == SUPERTYPE or sub == SUBTYPE: return True
    if (sup, sub) in types_hierarchy: return True
    for sp, sb in types_hierarchy:
        if sb != sub: continue
        if is_supertype(sup, sp): return True
    return False

def get_first_subtypes(sup):
    sub = []
    for sp, sb in types_hierarchy:
        if sp == sup: sub += [sb]
    return sub

case_frame = {
    #FROM, TO, WORD: SUPERTYPE, DEFAULT VALUE
    #(Case.INESSIVE, Case.ILLATIVE, SUPERTYPE): ["yuyi"],
    (ltype["clause"], ltype["subject"], "vidi"): (["animalo"], None),
    (ltype["clause"], ltype["instrumental"], "grafi"): (["grafanto"])

#    (CONCEPT_PREDICATE, CONCEPT_AGENT, "akto"): (["animate"], None),
#    (CONCEPT_PREDICATE, CONCEPT_INSTRUMENT, "akto"): (["entity"], None),
#    (CONCEPT_PREDICATE, CONCEPT_OBJECT, "state"): (["entity"], None),
    }



#prep_f = {
#    CASE_INESSIVE: ["place", ],
#    CASE_ILLATIVE: ["place", ]
#}
#
#case_frame = {
#    "act": {
#        CONCEPT_AGENT: "animate", #maybe a default value...
#        CONCEPT_INSTRUMENT: "entity"
#        },
#    "state": {
#        #CONCEPT_EXPERIENCER: "animate", #!!!!!!!!!!!!!!!!!!!!!????????????????
#        CONCEPT_OBJECT: "entity"
#        },
#    "event": {
#        CONCEPT_OBJECT: "entity"
#        },
#    "imagine":
#        {
#        CONCEPT_AGENT: "person",
#        CONCEPT_OBJECT: "univ_type",
#        },
#    "scan":
#        {
#        CONCEPT_AGENT: "machine",
#        CONCEPT_OBJECT: "univ_type",
#        },
#    "see":
#        {
#        CONCEPT_AGENT: "animate",
#        CONCEPT_OBJECT: "univ_type",
#        },
#    }

#if there is not some word in the aim lang
def meaning_shift(cf, lang):
    '''Interlingua approximation'''
    if type(cf) != type({}):
        return cf
    for key in [x for x in cf.keys()]: #beacause of conjunctions is the error!
        #print(key)
        if is_terminalc(key):
            lemma = cf[key][concept["lemma"]]
            if not lemma is None and not lemma in lang.meanings.keys():
                #replace with deffination
                #checking for properness
                #print(cf[key][concept["lemma"]], cf_diff[cf[key][concept["lemma"]]])
                q = cf_diff[cf[key][concept["lemma"]]]
                temp = meaning_shift(q, lang)
                tt = cf[key][concept["order-number"]]
                del cf[key]
                h = temp[[k for k in temp.keys()][0]] #because of {16: {16:
                #WTF? IT WILL CHACK IT TWICE!!!
                for key in h.keys():
                    cf[key] = h[key]
                cf[concept["order-number"]] = tt
                #print(cf)
        elif type(cf[key]) == tuple:
            ci, children = cf[key]
            r = []
            for c in children:
                r += [meaning_shift(c, lang)]
            cf[key] = ci, r
        else:
            cf[key] = meaning_shift(cf[key], lang)
    return cf