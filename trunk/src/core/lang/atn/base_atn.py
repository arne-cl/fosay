__author__ = 'zoltan kochan'
__date__ ="$28 june 2010 1:02:10$"

from core.constants import type

label_types = {
    # Tokens
    "PUNCT": type["punctuation"],
    "JMP":   type["epsilon"],
    "CONJ":  type["conjunction"],
    "ADJ":   type["adjective"],
    "AUX":   type["auxiliary"],
    "ADV":   type["adverb"],
    "V":     type["verb"],
    "P":     type["preposition"],
    "PRON":  type["pronoun"],
    "ART":   type["article"],
    "QUA":   type["quantifier"],
    "N":     type["noun"],
    "NUM":   type["numeral"],
    "NOT":   type["negative"],

    # Parsing rules
    "ip": type["sentence"],
    "subj": type["subject"],
    "cps": type["subject"],
    ##"PRED": type["PREDICATE"],
    #"SPRED": type["PREDICATE"], ###
    #"PREDWO": type["PREDICATE"],
    "np1": type["noun-phrase"],
    "np": type["noun-phrase"],
    "ap": type["epithet"],
    ##"AdvP": type["adverbial"],
    ##"AdvTimeP": type["adverbial"],
    "time": type["time"],
    "vp": type["verb-phrase"],
    "vp1": type["verb-phrase"],
    "vp2": type["verb-phrase"],
    "mvp": type["verb-phrase"],
    "ivp": type["verb-phrase"],
    "pobj": type["accusative"],
    "inobj": type["inessive"],
    "illobj": type["illative"],
    "elobj": type["elative"],
    "obj": type["accusative"],
    "cpo": type["accusative"],
    "poss": type["possessive"],
    "poss1": type["possessive"],
    "pp": type["preposition-phrase"],
    "ppv": type["preposition-phrase"],
    "prcl": type["clause"],
    "subcl": type["clause"],
    "cpa": type["adverbial"], ############
    "nump": type["numeral-phrase"],
}

def to_type_code(label):
    return label_types[label.split(":")[0]]