__author__="zoltan kochan"
__date__ ="$12 лют 2011 14:43:42$"

#from core.models.ling_units import *
from core.models.ling_units import ConjuctionStructure, Token
from core.constants import sentence_end
from core.constants import conj_type
from core.constants import concept
from core.constants import position
from core.constants import tags
from core.constants import case, number ##
import core.constants
from core.constants import INHERIT_NAME, INHERIT_VALUE, STATE_START
from core.constants import type as ltype
import sys
import os
from string import digits
from core.lang.process import parse
from copy import deepcopy
import core.compilers.cws as cws
import core.compilers.atnl as atnl
import os, glob

curr_dict = sys.modules[core.constants.__name__].__dict__

def markov(s, tr):
    '''Markov's algorithm.'''
    for old, new in tr:
        if s.find(old) != -1:
            s = s.replace(old, new)
    return s

class Language():
    '''Language is an object that stores all the info about a language.
    Like dictionary, grammar, contradictions, etc.'''
#    uncomplited = ["..."] #""
#    exclamation = ["!"]
#    question = ["?"]
#    question_exclamation = ["?!"]
    space = " "
    comma = ","
    semicolon = ";"
    colon = ":"
    # new_par = "~"
    question = "?"
    exclamation = "!"
    point = "."
    sent_end = {".": sentence_end["point"],
        "...": sentence_end["uncomplited"]}
       # "?": SENTENCE_END_QUESTION,
       # ""}
       
    def __str__(self):
        return self.name

    def __init__(self, lang_name):
        curr = str(os.path.dirname(sys.argv[0]))
        path = os.path.join(os.path.join(curr, "data"), lang_name)

        self.name = lang_name
        self.path = path
        self.separators = [", ", ". "]
        self.space = " "

        self._init_conjunctions()
        self._init_dictionary()
        self._init_grammar()
        self._init_contr()

        #print "ready"

    def to_type_code(self, label):
        return self.label_types[label.split(":")[0]]

    @staticmethod
    def _parse_bool(s):
        return s == "True"
    def _read_file(self, file_path):
        global f,s
        try:
            f = open(file_path, encoding = 'utf-8')
            s = [x.split('#')[0].strip() for x in f.readlines()]
            i = 0
            while i < len(s):
                if len(s[i]) == 0:
                    del s[i]
                elif s[i][-1] != '\\':
                    i += 1
                else:
                    s[i] = s[i][:-1] + ' ' + s[i + 1]
                    del s[i + 1]
        except IOError:
            print("can't open file '" + os.path.join(self.path, file_path) + "'")
        finally:
            f.close()
        return s

    def divide_into_words(self, text):
        """Lexing : Input is split into tokens"""
        res = [text.strip(self.space) + self.space]
        
        if text in self.separators:
            return res

        for sep in self.separators:
            res1 = []
            for x in res:
                t = x.split(sep)
                tt = []
                for y in t[:-1]:
                    tt += [y, sep]
                tt += [t[-1]]
                res1 += tt
            res = res1

        start = res
        res = []
        for x in start:
            if x in self.separators:
                res += [x]
            else:
                res += x.split(self.space)
        res = [w for w in res if w != ""]
        return res

    def _init_contr(self):
        d = {}
        for s in self._read_file(os.path.join(self.path, "contr.txt")):
            a, b = s.split("->")
            a = a.strip()[1:-1]
            b = b.strip()[1:-1]
            if a in d:
                d[a].append(b)
            else:
                d[a] = [b]
        self.contr = []
        for k in d.keys():
            self.contr.append((k, d[k]))

    def gen_to_ipa(self):
        return lambda text: [markov(s, self.tr) for s in text]

    def _init_tr(self):
        s = self._read_file(os.path.join(self.path, "ipa.txt"))
        self.tr = []
        if s == [] or s == None or s[0] == "": return
        i = 0
        while i < len(s):
            t1, t2 = [x.strip() for x in s[i].split("->")]
            if (not (t1[0] == t1[-1] == t2[0] == t2[-1] == "\"")):
                raise Exception("invalid text in _init_tr")
            self.tr += [(t1[1:-1], t2[1:-1])]
            i += 1

    def _init_grammar(self):
        print("Initializing %s grammar" % self.name)
        res = atnl.parse_file(os.path.join(os.path.join(self.path, "grammar"), "atnl.txt"))
        if res is None:
            print('error')
        else:
            print('done')
            self.atn, self.label_types = res

    def _init_dictionary(self):
        self._init_tr()
        files = []
        for infile in glob.glob(os.path.join(os.path.join(self.path, 'base'), '*.txt')):
            files += [infile]
        for infile in glob.glob(os.path.join(os.path.join(self.path, 'dictionary'), '*.txt')):
            files += [infile]

        self.vocabulary, self.meanings = cws.parse_files(files, self.gen_to_ipa(), True)
        
        self.words = []
        for k in self.vocabulary.keys():
            self.words += self.vocabulary[k]

    def _init_conjunctions(self):
        s = self._read_file(os.path.join(self.path, "conj.txt"))
        i = 0
        self.conjunctions = []
        while i < len(s):
            c = ConjuctionStructure()
            self.conjunctions.append(c)
            c.function_number = int(s[i].strip()[1:-1])
            i += 2
            c.por = [ltype[x.strip()] for x in s[i].split(':')[1].split(",")]# self._conditions(s[i].split(':')[1])
            i += 1
            while i < len(s) and s[i] != "}":
                p = [x.strip().lower() for x in s[i].split(':')]
                if len(p) == 1:
                    c.__dict__[p[0]] = True
                elif p[0] in ["order", "max-items"]:
                    c.__dict__[p[0]] = int(p[1])
                elif p[0] == "conj-type":
                    c.conj_type = conj_type[p[1]]
                else:
                    c.__dict__[p[0].replace("-", "_")] = p[1][1:-1]
                i += 1
            i += 1

    def is_punctuation(self, text):
        return text in [self.comma, self.semicolon, self.colon,\
            self.exclamation, self.question, self.point]

    def is_number(self, t):
        for s in t:
            if not s in digits:
                return False
        return True

    def init_words(self, text, start = 0, end = 0):
        result = []
        words = []
        tt = text.pop(0)
        t = tt.lower()

        if self.is_number(t):
            w = Token(type["numeral"], [tt], start, end)
            w.meaning = t
            w.num_type = NUM_TYPE_CARDINAL
            w.str_type = STR_TYPE_DIGITS
            return [([w], text)]
        if t[-3:] in ["1st", "2nd", "3rd"] or t[-2:] == "th" and self.is_number(t[:-2]):
            w = Token(type["numeral"], [tt], start, end)
            w.meaning = t[:-2]
            w.num_type = NUM_TYPE_ORDINAL
            w.str_type = STR_TYPE_DIGITS
            return [([w], text)]


        if self.is_punctuation(t):
            w = Token(ltype["punctuation"], [tt], start, end)
            words += [w]
        for x in self.conjunctions:
            if t == x.before:
                pos = position["before"]
            elif t == x.among:
                pos = position["among"]
            elif t == x.after:
                pos = position["after"]
            else:
                continue
            w = Token(ltype["conjunction"], [tt], start, end)
            w.position = pos
            #w.type = type["conjunction"]
            w.conjuction_structure = deepcopy(x)
            words += [w]

        if words != []: #EITHER MAKE AN ERROR HERE OR LET IT WORK WHEN THE FIRST WORD IS KNOWN THE SECOND ISN'T AND IT IS AN IDIOM
            result += [(words, deepcopy(text))]

        for x in self.vocabulary.get(t, []):
            p = [t] + deepcopy(text)
            for q in x.text:
                if q.lower() != p.pop(0).lower():
                    break
            else:
                result += [([deepcopy(x)], p)]

        if not result or result == []:
            raise Exception("Word '" + t + "' not found in the vocabulary.")
        return result

    def morphan(self, text):
        '''Morphological analyzation'''
        for w, rest in self.init_words(text):
            if rest == []:
                yield [w]
            else:
                for ww in self.morphan(rest):
                    yield [deepcopy(w)] + ww


    def remove_contr(self, text):
        '''Removes all contradictions from the text'''
        ss = [text]
        for old, news in self.contr:
            for i in range(len(ss)):
                temp = ss[0]
                del ss[0]
                if temp.find(old) != -1:
                    for new in news:
                        ss.append(temp.replace(old, new))
                else:
                    ss.append(temp)
        return ss

    def type_labels(self, type):
        return [label for label in self.label_types.keys() if self.label_types[label] == type]

    def zz(self, s):
        t = self.type_labels(s)
        if len(t) > 1:
            print(self.label_types, s)
            raise NotImplementedError
        return t[0]

    def words_to_mem(self, wss):
        mem = []
        for ws in wss:
            mem += [{}]
            for w in ws:
                if self.zz(w.type) in mem[-1]:
                    mem[-1][self.zz(w.type)] += [(w, len(mem))]
                else:
                    mem[-1][self.zz(w.type)] = [(w, len(mem))]
        return mem

    def init_sentence(self, sent, first = "IP"):
        ss = self.remove_contr(sent)
        res = []
        for s in ss:
            y = self.divide_into_words(s)
            for r in self.morphan(y):
                mr = self.words_to_mem(r)
                res += [x[2] for x in parse(self, first, STATE_START, mr)]
        return res

    def conj_str3(self, fn, ct, cs):
        return [x for x in self.conjunctions if fn == x.function_number and ct == x.conj_type and cs == x.conj_str]
    def conj_str(self, fn, ct):
        return [x for x in self.conjunctions if fn == x.function_number and ct == x.conj_type]

    def is_one_conjuction(self, before, among, after):
        pass

    def synset(self, meaning):
        return [w for w in self.meanings[meaning] if w.contains(case["@nominative"]) and w.contains(number["@singular"])]

    def definition(self, meaning):
        raise NotImplementedError

#global_props = [CONCEPT_CASE, CONCEPT_TENSE, CONCEPT_PARTICIPLE, CONCEPT_PERSONE]