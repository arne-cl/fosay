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
from core.lang.atn.base_atn import label_types
from string import digits
from core.lang.process import parse
from copy import deepcopy
import core.compilers.cws as cws
import core.compilers.atnl as atnl
import os, glob

curr_dict = sys.modules[core.constants.__name__].__dict__

def xx(s):
    r = []
    for key in label_types.keys():
        if label_types[key] == s:
            r += [key]
    return r

def zz(s):
    t = xx(s)
    if len(t) > 1:
        print(label_types, s)
        raise NotImplementedError
    return t[0]

def markov(s, tr):
    '''Markov's algorithm.'''
    for old, new in tr:
        if s.find(old) != -1:
            s = s.replace(old, new)
    return s

class Language():
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

    def _fstr_to_cond(self, s):
        #left, right = [x.strip() for x in s.split(":")]
        f = s.find(":")
        left = s[:f].strip()
        right = s[f+1:].strip()
        if left == "type":
            m = concept["type"], curr_dict[right]
        elif left == "text":
            if (not (right[0] == right[-1] == "\"")):
                raise Exception("invalid text '" + right + "'")
            m = concept["text"], right[1:-1]
        elif left == "transcription":
            if (not (right[0] == right[-1] == "\"")):
                raise Exception("invalid transcription '" + right + "'")
            m = concept["transcription"], right[1:-1]
        elif right in ["True", "False"]:
            m = concept[left], Language._parse_bool(right)
        elif right[0] == right[-1] == '"':
            #print(right)
            m = concept[left], right[1:-1]
        elif right[0] in digits + "-":
            #print "right"
            m = concept[left], int(right)
        else:
                #print(left.capitalize(), right)
                #print(left[0].upper() + left[1:], )
                #SubjNumber = Number
            #print(m.meaning)
            #print(concept[left])
            #print("xx")
            if right == "inherit":
                m = concept[left], None
            else:
                m = concept[left], curr_dict[left.replace("-", "_")][right.lower()]
            #m = concept[left], curr_dict[left[0].upper() + left[1:]].__getattr__(right.upper())
        return m

#    def _left_to_enum(self, left):
#        if left.find("_") != -1:
#            a, b = left.split("_")
#            return a[0].upper() + a[1:] + b[0].upper() + b[1:]
#        else:
#            return left[0].upper() + left[1:]

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

    def modif_text(self, pattern, text):
        if pattern.find("|") != -1:
            left, right = pattern.split("|")
            text = self.modif_text(left, text)
            text = self.modif_text(right, text)
            return text
        
        if pattern.find(">") != -1:
            n, wo = pattern.split(">")
            temp = text if n == "0" else text[:-int(n)]
            if len(wo) > 1 and wo[0] == ":":
                if temp[-1] == "y":
                    temp = temp[:-1] + temp[-2] + temp[-1]
                else:
                    temp += temp[-1]
                wo = wo[1:]
            return temp + wo
        if pattern.find("<") != -1:
            wo, n = pattern.split("<")
            temp = text[int(n):]
            return wo + temp
        return pattern

    def _init_tr(self):
        s = self._read_file(os.path.join(self.path,"ipa.txt"))
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
        #import WConio
        #WConio.textcolor(WConio.BLUE)
        print("Initializing %s grammar" % self.name)
        self.atn = atnl.parse_file(os.path.join(os.path.join(self.path, "grammar"), "atnl.txt"))
        #f = open(os.path.join(os.path.join(self.path, "grammar"), "atnl.txt"), encoding = 'utf-8')
        #self.atn = atnl.parse("".join(f.readlines()))
        #atnl.parse("iyiu")

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

#    def _init_pronouns(self):
#        self.pronouns = self._init_modificators("pron.txt")
    def is_punctuation(self, text):
        return text in [self.comma, self.semicolon, self.colon,\
            self.exclamation, self.question, self.point]
#    def is_modifier(self, word):
#
#        pass
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
            #print "!!!!!!!!!"
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
    def words_to_mem(self, wss):
        mem = []
        for ws in wss:
            mem += [{}]
            for w in ws:
                if zz(w.type) in mem[-1]:
                    mem[-1][zz(w.type)] += [(w, len(mem))]
                else:
                    mem[-1][zz(w.type)] = [(w, len(mem))]
        return mem

    def init_sentence(self, sent, first = "IP"):
        ss = self.remove_contr(sent)
        res = []
        for s in ss:
            y = self.divide_into_words(s)
            #r = [self.init_word(x) for x in y]
            for r in self.morphan(y):
#               ### res += [x for x in match1_mem(self.atn, "IP", STATE_START, r)]
                mr = self.words_to_mem(r)
                ##print mem
                res += [x[2] for x in parse(self, first, STATE_START, mr)] # MAYBE self.words_to_mem(r)
                #res += [x for x, y in mem[0]["IP"]] #!!!!!!!!!!!!!!!!!!!!!!!!

                #mem = total_mem(self.atn, mr) #MUSTN'T BE!!!!!!!!!
#                for m in self.look_for_patterns(mr): #TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!
#                    #print m
#                    res += [x[2] for x in parse(self, first, STATE_START, m)]
        return res

    def conj_str3(self, fn, ct, cs):
        return [x for x in self.conjunctions if fn == x.function_number and ct == x.conj_type and cs == x.conj_str]
    def conj_str(self, fn, ct):
        return [x for x in self.conjunctions if fn == x.function_number and ct == x.conj_type]

    def is_one_conjuction(self, before, among, after):
        pass

#    #comparing only the needed properties (from w[])
#    def find_all(self, word):
#        words = []
#        #print(word._props, word.type)
#        for key in self.vocabulary.keys():
#            for w in self.vocabulary[key]:
#                if w.type == word.type:
#                    for p in w._props.keys():
#                        #print key
#                        if p in word._props.keys() and w._props[p] != word._props[p]:
#                            break
#                    else:
#                        cw = deepcopy(w)
#                        cw.text = None
#                        if not cw in words:
#                            words += [cw]
#        #print words
#        return words
##        #raise NotImplementedError
##        words = []
##        #print(word._props, word.type)
##        for key in self.vocabulary.keys():
##            for w in self.vocabulary[key]:
##                if w.type == word.type:
##                    cw = deepcopy(w)
##                    cw.text = None
##                    if not cw in words:
##                        words += [cw]
##        #print words
##        return words
##        #raise NotImplementedError


    def synset(self, meaning):
        return [w for w in self.meanings[meaning] if w.contains(case["@nominative"]) and w.contains(number["@singular"])]

    def definition(self, meaning):
        raise NotImplementedError


#global_props = [CONCEPT_CASE, CONCEPT_TENSE, CONCEPT_PARTICIPLE, CONCEPT_PERSONE]

#TODO: Mosaic translation
#required leafs
