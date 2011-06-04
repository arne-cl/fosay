# -*- coding: ISO-8859-5 -*-
__author__="zoltan kochan"
__date__ ="$28 june 2010 1:02:10$"

# Standard states
STATE_START = 1
STATE_END = 1000000

STATE_CONJ_A1, \
STATE_CONJ_A2, \
STATE_CONJ_A3, \
STATE_CONJ_A4 = range(-4, 0)
STATE_CONJS = [
    STATE_CONJ_A1,
    STATE_CONJ_A2,
    STATE_CONJ_A3,
    STATE_CONJ_A4,
]

INDEFINITE = 100000


INHERIT_NAME = "inherit"
INHERIT_VALUE = None
#NEUTRAL_VALUE = "neutral"#0
NONE_VALUE = "none"


def create_dict(list):
    d = {}
    for item in list:
        d[item] = item
    return d

def create_dict_t(concept, list):
    d = {}
    for item in list:
        d[item] = item
    #    d["@" + item] = (concept, item)
    ########
    d["none"] = NONE_VALUE
    #d["@none"] = (concept, NONE)
    ###########
    d[INHERIT_NAME] = INHERIT_VALUE
    #d["@" + INHERIT_NAME] = (concept, INHERIT_VALUE)
    return d



def is_terminalc(const):
    if const is None: raise Exception("Type can't be None")
    return const in terminal

def is_nonterminalc(const):
    return const in nonterminal

def is_prop(c):
    return c in concept

terminal = create_dict([
    "preposition",
    "auxiliary",
    "article",
    "quantifier",
    "noun",
    "pronoun",
    "adjective",
    "verb",
    "adverb",
    "numeral",
    "negative",
    "conjunction",
    "punctuation"
])
nonterminals = [
    #"adverbial",
    "epithet",
    "preposition-phrase",
    "noun-phrase",
    "subject",
    "object",
    "verb-phrase",
    "numeral-phrase",
    "clause",
    "sentence",
    "paragraph",
    "text"
]

concept = create_dict([
    "personal-name",
    "use-of-to",
    "extra-1",
    "extra-2",
    "transcription",
    "text",
    "type",
    "truth",
    "quantity",
    "quantity-number",
    "quantity-case",
    "conj-type",
    "conj-str",
    "conj-function",
    "gender",
    "number",
    "participle",
    "voice",
    "mood",
    "persone",
    "clusivity",
    "modal",
    "poss-form",
    "clause-type",
    "pronoun-type",
    "adverb-type",
    "num-type",
    #"concept",
    "noun-type",
    "str-type",
    "position",
    "form",
    "object-persone",
    "subject-persone",
    "object-number",
    "object-difinity",
    "subject-number",
    "object-form",
    "subject-form",
    "stem",
    "lemma",
    "difinity",
    "case",
    "case-2",
    "tense",
    "transitivity",
    "aspect",
    "order-number",
    "real-number",
    "tags"
    ])

XFROM_FIRST,\
XFROM_LAST,\
XFROM_SUM,\
XFROM_NUMBER,\
XFROM_EVERY = range(1, 6)

langs = [
    "ukrainian",
    "hungarian",
    "russian",
    "rusyn",
    "english",
    ]

tags = create_dict_t(concept["tags"],
    langs + \
    [
    "slang",
    "math",
    "archaic",
    "literary",
    "official",
    ])

personal_name = create_dict_t(concept["personal-name"],
    [
    "first-name",
    "middle-name",
    "last-name",
    "surname",
    "given-name",
    "patronymic",
    "matronymic"
    ])

participle = create_dict_t(concept["participle"],
    [
    "participle",
    "not-participle"
    ])

strtype = create_dict_t(concept["str-type"],
    [
    "text",
    "digits",
    ])

sentence_end = create_dict(
    [
    "point",
    "uncomplited",
    "question",
    "exclamation",
    "question-exclamation",
    "uncomplited-question",
    "uncomplited-exclamation",
    ])

sentence_type = create_dict(
    [
    "declarative",
    "imperative",
    "interrogative",
    "exclamatory",
    ])

poss_form = create_dict_t(concept["poss-form"],
    [
    "conjoint",
    "absolute",
    ])

transitivity = create_dict_t(concept["transitivity"],
    [
    "intransitive",
    "transitive",
    #"ambitransitivity", = none
    ])

tense = create_dict_t(concept["tense"],
    [
    "infinitive",
    "past",
    "present",
    "future",
    ])

aspect = create_dict_t(concept["aspect"],
    [
    "indefinite",
    "continuous", #progressive
    "perfect",
    "perfect-continuous-durative",
    "perfect-continuous-not-durative",
    "indefinite-in-the-past",
    "perfect-in-the-past",
    "continuous-in-the-past"
    "prospective"
    ])

#http://en.wikipedia.org/wiki/grammatical_aspect
#perfective: 'i struck the bell.' (a unitary event)
#momentane: 'the mouse squeaked once.' (contrasted to 'the mouse squeaked/was squeaking.')
#perfect (a common conflation of aspect and tense): 'i have arrived.' (brings attention to the consequences of a situation in the past)
#recent perfect ~ after perfect: 'i just ate' or: 'i am after eating." (hiberno-english)
#prospective (a conflation of aspect and tense): 'i am about to eat', 'i am going to eat." (brings attention to the anticipation of a future situation)
#imperfective (an unfinished action, combines the meanings of both the progressive and the habitual aspects): 'i am walking to work' (progressive) or 'i walk to work every day' (habitual).
#progressive ~ continuous: 'i am eating.' (action is in progress; a subtype of imperfective)
#habitual: 'i used to walk home from work', 'i would walk home from work.' (past habitual) (a subtype of imperfective)
#gnomic/generic: 'fish swim and birds fly' (general truths)
#episodic: 'the bird flew' (non-gnomic)
#continuative: 'i am still eating.'
#inceptive ~ inchoative: 'i fell in love'
#terminative ~ cessative: 'i finished my meal.'
#defective : 'i almost fell.'
#pausative: 'i stopped working for a while.'
#resumptive: 'i resumed sleeping.'
#punctual: 'i slept.'
#durative: 'i slept and slept.'
#delimitative: 'i slept for an hour.'
#protractive: 'the argument went on and on.'
#iterative: 'i read the same books again and again.'
#frequentative: 'it sparkled', contrasted with 'it sparked'. or, 'i run around', vs. 'i run'.
#experiential: 'i have gone to school many times.'
#intentional: 'i listened carefully.'
#accidental: 'i knocked over the chair.'
#intensive: 'it glared.'
#moderative: 'it shone.'
#attenuative: 'it glimmered.'

#aspect:
#phase          continue
#iteration          once
#duration           prolonged
#telicity               false

voice = create_dict_t(concept["voice"],
    [
    "active",
    "passive",
    ])

#what is: realis
mood = create_dict_t(concept["mood"],
    [
    "generic",
    "indicative",
    "mirative",
    "conditional",
    "subjunctive",
    "alethic",
    "deliberative",
    "hortative",
    "imperative",
    "jussive",
    "necessitative",
    "permissive",
    "precative",
    "prohibitive",
    "desiderative",
    "imprecative",
    "optative",
    "quotative-evidential",
    "sensory-evidential",
    "assumptive",
    "declarative",
    "deductive",
    "dubitative",
    "energetic",
    "hypothetical",
    "inferential",
    "renarrative",
    "interrogative",
    "potential",
    "presumptive",
    "speculative",
    ])

pronoun_type = create_dict_t(concept["pronoun-type"],
    [
    "personal",
    "possessive",
    "reflexive",
    "reciprocal",
    "demonstrative",
    "interrogative",
    "conjunctive",
    "indefinite",
    "negative",
    "defining",
    "quantitative",
    ])

noun_type = create_dict_t(concept["noun-type"],
    [
    "common",
    "proper",
    "abbreviation",
    ])

#for adverbs, pronouns and clauses
adverb_types = \
    [
    "quality",
    "reason",
    "time",
    "repetition-and-frequency",
    "degree",
    "place",
    "manner",
    "association",
    "thing",
    "amount",
    "individual",
    ]


#http://en.wikipedia.org/wiki/determiner_(linguistics)


num_type = create_dict_t(concept["num-type"],
    [
    "cardinal",
    "ordinal",
    ])

conj_type = create_dict_t(concept["conj-type"],
    [
    "non-contrasting", #and, nor
    "contrasting", #but, yet
    "consequence", #so ###########
    ])

conj_str = create_dict_t(concept["conj-str"],
    [
    "before",
    "among",
    "after",
    "before-among",
    "before-after",
    "before-among-after",
    "among-after",
    "nothing",
    ])

quantity = create_dict_t(concept["quantity"],
    [
    "all", #всі/кожна
    "few", #кілька
    "many", #багато
    "no", #жодна/жодні
    "any", #будь-яка/будь-які
    "some" #якась/якісь/деякі
    ]
)

clause_type = create_dict_t(concept["clause-type"],
    [
    "principal",
    "subordinate",
    ])


clusivity = create_dict_t(concept["clusivity"],
    [
    "exclusive",
    "inclusive"
    ])

gender = create_dict_t(concept["gender"],
    [
    "lifeless",
    "vivacious",
    "divine",
    "masculine",
    "feminine",
    #"masculine_feminine",
    ])

###################################################
position = create_dict(
    [
    "before",
    "before-1",
    "before-2",
    "before-3",
    "among",
    "after",
    ])


cases = [
    "accusative", #házat
    "direct",
    "ergative",
    "intransitive",
    "nominative",
    "oblique",
    "ablative", #hazto'l (ha'ztul)
    "antessive",
    "dative", #indirect object, recipient, daval'nyj
    "distributive", #fejenk'ent
    "distributive-temporal", #naponta
    "essive",
    "essive-formal", #emberként
    "essive-modal", #emberül
    "formal", #emberk'eppen
    "genitive",
    "instructive",
    "instrumental", #valami -val -vel
    "instrumental-comitative",
    "ornative",
    "possessed", #(n''o) h'az'at (the opposite of possessive)
    "possessive", #john's, rodovyj
    "postpositional",
    "prepositional",
    "pertingent",
    "prolative",
    "prosecutive",
    "proximative",
    "sociative", #ruh'astul
    "temporal",
    "vialis",
    "adessive", #ha'zna'l
    "allative", #ha'zhoz
    "apudessive",
    "associative",
    "comitative", #emberrel
    "delative", #ha'zro'l
    "elative", #ha'zbo'l
    "exessive",
    "illative", #a fiu' megy a !ha'zba
    "inelative",
    "inessive", #ha'zban
    "inessive-time", #added by me!#added by me!#added by me!#added by me!#added by me!#added by me!#added by me!#added by me!#added by me!#added by me!#added by me!
    "intrative",
    "lative",
    "locative",
    "perlative",
    "subessive",
    "sublative", #ha'zra
    "superessive", #ha'zon
    "superlative",
    "terminative", #ha'zig (holnapig)
    "translative", #emberré	(eredmény)
    "comparative",
    "equative",
    "aversive",
    "benefactive",
    "evitative",
    "abessive",
    "addirective",
    "adelative",
    "adverbial", ######
    "caritive",
    "causal",
    "causal-final",
    "final", #emberért(ok, cél)
    "modal",
    "multiplicative",
    "partitive",
    "pegative",
    "privative",
    "postelative",
    "postdirective",
    "postessive",
    "separative",
    "subdirective",
    "vocative",
    "absolutive",
    ]
##########################################################
#http://hu.wikipedia.org/wiki/esetek_a_magyar_nyelvben
case = create_dict_t(concept["case"], cases)
case_2 = create_dict_t(concept["case-2"], cases)
quantity_case = create_dict_t(concept["quantity-case"], cases)
adverb_type = create_dict_t(concept["adverb-type"], adverb_types)

nonterminal = create_dict(nonterminals + adverb_types)

from copy import copy
type = copy(terminal)
type.update(nonterminal)
type.update(create_dict(cases))
type["epsilon"] = "epsilon"
#type.update(concept)

numbers = [
    "uncountable",
    "singular",
    "dual",
    "trial",
    "quadral",
    "plural",
    ]

number = create_dict_t(concept["number"], numbers)
subject_number = create_dict_t(concept["subject-number"], numbers)
object_number = create_dict_t(concept["object-number"], numbers)
real_number = create_dict_t(concept["real-number"], numbers)
quantity_number = create_dict_t(concept["quantity-number"], numbers)

persones = [
    "first",
    "second",
    "third",
    "infinitive",
    ]
persone = create_dict_t(concept["persone"], persones)
subject_persone = create_dict_t(concept["subject-persone"], persones)
object_persone = create_dict_t(concept["object-persone"], persones)

forms = [
    "meek", #Юлічка
    "informal", #Юля
    "formal", #Юлія
    "insolent", #sértő, образливий
    ]
form = create_dict_t(concept["form"], forms)
subject_form = create_dict_t(concept["subject-form"], forms)
object_form = create_dict_t(concept["object-form"], forms)

difs = [
    "difinite",
    "undifinite",
    "participle",
    "quantifier"
    ]
difinity = create_dict_t(concept["difinity"], difs)
object_difinity = create_dict_t(concept["object-difinity"], difs)












    





modificators = [
    terminal["preposition"],
    terminal["punctuation"],
    terminal["article"],
    terminal["quantifier"],
    terminal["auxiliary"],
    terminal["negative"]
    ]



concept_type = {
    "personal-name": "ident",
    "use-of-to": "bool",
    "extra-1": "int",
    "extra-2": "int",
    "transcription": "str",
    "text": "str",
    "type": "ident",
    "truth": "float",
    "quantity": "ident",
    "quantity-number": "ident",
    "quantity-case": "ident",
    "conj-type": "ident",
    "conj-str": "ident",
    "conj-function": "ident",
    "gender": "ident",
    "number": "ident",
    "participle": "ident",
    "voice": "ident",
    "mood": "ident",
    "persone": "ident",
    "clusivity": "ident",
    "modal": "bool",
    "poss-form": "ident",
    "clause-type": "ident",
    "pronoun-type": "ident",
    "adverb-type": "ident",
    "num-type": "ident",
    "noun-type": "ident",
    "str-type": "ident",
    "position": "ident",
    "form": "ident",
    "object-persone": "ident",
    "subject-persone": "ident",
    "object-number": "ident",
    "object-difinity": "ident",
    "subject-number": "ident",
    "object-form": "ident",
    "subject-form": "ident",
    "stem": "str",
    "lemma": "str",
    "difinity": "ident",
    "case": "ident",
    "case-2": "ident",
    "tense": "ident",
    "transitivity": "ident",
    "aspect": "ident",
    "order-number": "int",
    "real-number": "ident",
    "tags": "ident",
}






def eq(a, b):
    #print(a, b)
    return a == b or \
        a == INHERIT_VALUE or \
        b == INHERIT_VALUE
        #a == INHERIT_VALUE and b != NONE_VALUE or \
        #b == INHERIT_VALUE and a != NONE_VALUE

def eqx(name, a, b):
    return eq(a.attr(name), b.attr(name))

neq = lambda a, b: not eq(a, b)

#повертає істину, коли a чи b рівне value
#def omega(name, a, b, value):
#    if a.attr(name) == None and b.attr(name) == None:
#        return False
#    if a.attr(name) != None:
#        return a.attr(name) == value
#    return b.attr(name) == value

def preqconst(name, a, c):
    if a.attr(name) == None:
        a.attr(name, c)
        return True
    return eq(a.attr(name), c)
