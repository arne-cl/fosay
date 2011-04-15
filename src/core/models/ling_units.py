__author__="zoltan kochan"
__date__ ="$30 жовт 2010 15:55:57$"

import sys
from core.constants import concept, noun_type, modificators, conj_str, number
from core.constants import NONE
from core.constants import eq
from core.constants import XFROM_NUMBER, XFROM_EVERY, XFROM_FIRST, XFROM_LAST, XFROM_SUM
from core.constants import type as ltype
from types import *

#TODO: All numbers have the same meaning or doesn't have any. And we know which exatly number is it from real_number! It's genious!!! Then I can use numbers for meanings.
#TODO: use codes instead of interlingua-words

dict = sys.modules[__name__].__dict__

class LingUnit:
    parent = None
    _attrs = None

    def get_ghost(self):
        pass

    def is_proper(self, eqto):
        pass

    def attr(self, name, value=-898):
        '''Gets or sets the attribute of the object.'''
        if value == -898:
            return self._attrs.get(name, None)
        self._attrs[name] = value
        return self._agree(name)

    def contains(self, p):
        return self.attr(p[0]) == p[1]

    def fixed_with(self, name):
        pass

    def numerate(self, num):
        pass

    def renumerate(self, num):
        pass
    
    
    def add_attach(self, names):
        "the parametheres which must be the same here and in the parent"
        for n in names:
            if type(n) == tuple:
                self._attach_up[n[0]] = n[1]
                self._attach_down[n[1]] = n[0]
            else:
                self._attach_up[n] = n
                self._attach_down[n] = n

        #self._attach += names
        #return all([])
        for n in names:
            if type(n) == tuple and not self._agree(n[0]) or \
                type(n) != tuple and not self._agree(n):
            #if type(n) != tuple and not self._agree(n):#####################
                return False
        return True

    def add_fixed(self, fixed):
        self.fixed = fixed
        return self.add_attach(fixed)

    def refresh(self):
        for a in self._attach_up:
            if not self._agree(a):
                return False
        return True


    rx = {
        1: {
        concept["number"]: XFROM_NUMBER,
        concept["case"]: XFROM_EVERY,
        concept["tense"]: XFROM_EVERY,
        concept["aspect"]: XFROM_EVERY,
        concept["mood"]: XFROM_EVERY,
        concept["gender"]: XFROM_SUM,
        concept["persone"]: XFROM_SUM,
        concept["subject-persone"]: XFROM_EVERY, #############
        concept["subject-number"]: XFROM_EVERY, #############
        concept["subject-form"]: XFROM_EVERY, #############
        concept["object-persone"]: XFROM_EVERY, #############
        concept["object-number"]: XFROM_EVERY, #############
        concept["object-difinity"]: XFROM_EVERY, #############
        concept["object-form"]: XFROM_EVERY, #############
        concept["difinity"]: XFROM_FIRST,
        concept["participle"]: XFROM_FIRST,##########
        },
        7: {
        concept["number"]: XFROM_NUMBER,
        concept["case"]: XFROM_EVERY,
        concept["tense"]: XFROM_EVERY,
        concept["aspect"]: XFROM_EVERY,
        concept["mood"]: XFROM_EVERY,
        concept["gender"]: XFROM_SUM,
        concept["persone"]: XFROM_SUM,
        concept["subject-persone"]: XFROM_EVERY, #############
        concept["subject-number"]: XFROM_EVERY, #############
        concept["subject-form"]: XFROM_EVERY, #############
        concept["object-persone"]: XFROM_EVERY, #############
        concept["object-number"]: XFROM_EVERY, #############
        concept["object-difinity"]: XFROM_EVERY, #############
        concept["object-form"]: XFROM_EVERY, #############
        concept["difinity"]: XFROM_FIRST,
        concept["participle"]: XFROM_FIRST,##########
        },
    }

    def _eko(self, children, name): #АЛЕ ЦЕ ТРЕБА РОБИТИ ЛИШ В КІНЦІ, БО МІНЯТИ МОЖНА РАЗ
        if type(children) != list:
            if not (name in children._attach_down):
                return True
            return self._shift_value(self, name, children.attr(children._attach_down[name]))
        if len(children) == 0 or not name in children[0]._attach_down: return True
        if len(children) == 1: return self._shift_value(self, name, children[0].attr(children[0]._attach_down[name]))
        



        #it is neendeble in any case. but maybe use all not any???
        if any([c.attr(name) == None for c in children]): return True

        

        
        tx = self.rx[self.relation.function_number][name]
        if tx == XFROM_NUMBER:
            return self._shift_value(self, name, number["plural"])
        elif tx == XFROM_EVERY:
            f = children[0].attr(name)
            for i in range(len(children) - 1):
                if children[i + 1].attr(name) != f:
                    return False
            return self._shift_value(self, name, children[0].attr(name))
        elif tx == XFROM_SUM:
            return self._shift_value(self, name, children[0].attr(children[0]._attach_down[name]))
        elif tx == XFROM_FIRST:
            return self._shift_value(self, name, children[0].attr(children[0]._attach_down[name]))
        raise NotImplementedError

    def _bottom_up_refresh(self, name):
        b = []
        for l in self.left + [self.blocks] + self.right:
            b += [self._eko(l, name)]
        if not all(b):
            return False
        if not self._agree(name): ################################################
            return False #########################################################
        return True


    def _shift_value(self, to_obj, name, value):
        temp = to_obj.attr(name)
        if temp == None:
            return to_obj.attr(name, value)
        return eq(temp, value)

    def _parent_agree(self, name):
        if self.parent and name in self._attach_up:#name in self._attach and self.parent:
            if not self.parent._bottom_up_refresh(self._attach_up[name]):
                return False
        return True

    def _agree(self, name):
        if not self._parent_agree(name):
            return False
        return True





    def __init__(self, type, start, end):
        self._attrs = {}
        self.type = type
        self.start = start
        self.end = end
        self._attach_up = {}
        self._attach_down = {}
        self.left = []
        self.blocks = []
        self.right = []
    def get_focused_ling_unit(self, cursor):
        """ Returns the focused object """
        if self.start <= cursor <= self.end:
            return self
        return None
    def get_tree(self): raise NotImplementedError
        #return new TreeNode(this.ToString());
        #return TreeNode(str(self))
    def to_rtf(self):
        raise NotImplementedError



    def get_type(self):
        return self.attr(concept["type"])

    def set_type(self, type):
        return self.attr(concept["type"], type)

    type = property(get_type, set_type)


class NodeLingUnit(LingUnit):
    blocks = None
    def __init__(self, type, start, end):
        self.blocks = []
        LingUnit.__init__(self, type, start, end)
    def get_focused_ling_unit(self, cursor):
        for x in self.blocks:
            temp = x.get_focused_ling_unit(cursor)
            if temp: return temp
        return LingUnit.get_focused_ling_unit(self, cursor)
    def get_tree(self): raise NotImplementedError
        #if len(blocks):
        #    return blocks[0].gtree()
#        if (Blocks.Count == 1)
#            return Blocks[0].GetTree();
#        TreeNode t = new TreeNode(this.ToString());
#        foreach (T n in Blocks)
#        {
#            t.Nodes.Add(n.GetTree());
#        }
#        return t;


class RelationLingUnit(NodeLingUnit):
    relation = None
    def __init__(self, type, start, end):
        NodeLingUnit.__init__(self, type, start, end)


class FlowerLingUnit(RelationLingUnit):
    left = None
    right = None

    def __init__(self, type, start, end):
        self.left = []
        self.right = []
        RelationLingUnit.__init__(self, type, start, end)
    def get_focused_ling_unit(self, cursor): raise NotImplementedError
    def get_tree(self): raise NotImplementedError

    def __str__(self):
        s = ""
        if self.left:
            for l in self.left:
                if not l.get_ghost():
                    s += str(l) + " "
        if self.relation:
            if self.relation.before:
                bef = self.relation.before + " "
            else:
                bef = ""
            if self.relation.among:
                am = self.relation.among + " "
            else:
                am = ""
            if self.relation.after:
                af = self.relation.after + " "
            else:
                af = ""
            if self.relation.with_comma:
                comma = ","
            else:
                comma = ""
        else:
            bef, am, af, comma = "", "", "", ""

        s += bef
        for b in self.blocks[:-1]:
             if not b.get_ghost():
                s += str(b) + comma + " " + am # + " "
        s += str(self.blocks[-1])
        s += af


        if self.right:
            for r in self.right:
                if not r.get_ghost():
                    s += " " + str(r) if r.type != ltype["punctuation"] else str(r)
        if self.type == ltype["sentence"]:
            #s += "."
            s = s[0].upper() + s[1:]
        return s.strip()

    def fixed_with(self, name):
        return any([x.fixed_with(name) for x in self.left + self.blocks + self.right])

    def get_ghost(self):
        return any([x.get_ghost() for x in self.left + self.blocks + self.right])

    def _top_down_shift(self, obj, name, value):
        return value == NONE or value != NONE and self._shift_value(obj, name, value)

    def _agree(self, name):
        value = self._attrs.get(name, None)
        if value != None:
            #top-down refresh
            #if not all([self._shift_value(b, b._attach_down[name], value) for b in self.left if name in b._attach_down]):
            #    return false #IT IS ANALOGICAL
            
            for b in self.left:
                if name in b._attach_down:
                    if not self._top_down_shift(b, b._attach_down[name], value):
                        return False
            #print(len(self.blocks))
            if len(self.blocks) <= 1 or self.rx[self.relation.function_number].get(name, None) == XFROM_EVERY:
                for b in self.blocks:
                    if name in b._attach_down:
                        if not self._top_down_shift(b, b._attach_down[name], value):
                            return False

            for b in self.right:
                if name in b._attach_down:
                    if not self._top_down_shift(b, b._attach_down[name], value):
                        return False

        return LingUnit._agree(self, name)

    def numerate(self, num):
        for e in self.left + self.blocks + self.right:
            num = e.numerate(num)
        return num

    def renumerate(self, num=None):
        if self.attr(concept["order-number"]) != None:
            if num == None:
                return self.attr(concept["order-number"]) + 1, 0
            res = abs(self.attr(concept["order-number"]) - num)
            return num + 1, res

        res = 0
        for e in self.left + self.blocks + self.right:
            num, diff = e.renumerate(num)
            res += diff
        return num, res

    
    def get_cblocks(self):
        if self.relation == None:
            return self.blocks

        bl = []
        if self.relation.before != None:
            w = Token(self.relation.before)
            w.type = ltype["conjunction"]
            w.transcription = self.relation.before_transcription
            bl += [w]


        am = self.relation.among != None
        for b in self.blocks[:-1]:
            bl += [b]
            if am:
                w = Token(self.relation.among)
                w.type = ltype["conjunction"]
                w.transcription = self.relation.among_transcription
                bl += [w]
        bl += [self.blocks[-1]]

        if self.relation.after != None:
            w = Token(self.relation.after)
            w.type = ltype["conjunction"]
            w.transcription = self.relation.after_transcription
            bl += [w]

        return bl

    cblocks = property(get_cblocks)
    

    def is_proper(self, eqto):
        pass


class ConjuctionStructure:
    before = None
    among = None
    after = None

    with_comma = None
    connect = None

    function_number = None
    order = None
    max_items = None

    por = None

    conj_type = None

    def __init__(self):
        self.with_comma = False
        self.connect = False
        self.por = []
#    def __init__(self, before, among, after):
#        self.before = before
#        self.among = among
#        self.after = after

    def __eq__(self, other):
#        return not self and not other or \
#            self and other and \
#            self.before == other.before and \
#            self.among == other.among and \
#            self.after == other.after and \
#            self.with_comma == other.with_comma and \
#            self.connect == other.connect and \
#            self.function_number == other.function_number and \
#            self.order == other.order #and \
#            # self.por == other.por #if i want to use (actiolly there's no obvious need in it) I must choose another way to compare them!!!
        return not self and not other or \
            self and other and \
            (self.before == other.before and \
            self.among == other.among and \
            self.after == other.after and \
            self.with_comma == other.with_comma and \
            self.connect == other.connect and \
            self.function_number == other.function_number and \
            self.order == other.order or \
            #self.conj_type == order.conj_type and \
            #self.max_items == order.max_items or \
            self.before == other.before == None and \
            self.among and other.among and \
            self.after == other.after == None and \
            self.connect == other.connect and \
            self.function_number == other.function_number and \
            self.order == other.order) #and \
            #self.conj_type == order.conj_type and \
            #self.max_items == order.max_items)
    def __ne__(self, other):
        return not (self == other)

    def get_conj_str(self):
        if self.before:
            if self.among:
                if self.after:
                    return conj_str["before-among-after"]
                else:
                    return conj_str["before-among"]
            elif self.after:
                return conj_str["before-among"]
            else:
                return conj_str["before"]
        elif self.among:
            if self.after:
                return conj_str["after"]
            else:
                return conj_str["among-after"]
        elif self.after:
            return conj_str["after"]
        else:
            return conj_str["nothing"]

    conj_str = property(get_conj_str)

#class Transcription:
#    #the first 3 parameters are boolean
#    stressed = None
#    before_a_vowel = None
#    after_a_vowel = None
#    transcription = None

#TODO: Add a Lang property.

class Token(LingUnit):
    fixed = None

    _is_ghost = None #is empty?
    _text = None

    #Phonetic transcription in International Phonetic Alphabet
    def get_transcription(self):
        return self.attr(concept["transcription"])

    def set_transcription(self, transcription):
        return self.attr(concept["transcription"], transcription)

    transcription = property(get_transcription, set_transcription)

    def get_ghost(self):
        return self._is_ghost

    def set_ghost(self, value):
        self._is_ghost = value

    def get_meaning(self):
        return self.attr(concept["lemma"])

    def set_meaning(self, meaning):
        return self.attr(concept["lemma"], meaning)

    meaning = property(get_meaning, set_meaning)

    def numerate(self, num):
        if self.type in modificators: return num#0
        self.attr(concept["order-number"], num)
        return num + 1

    #TODO: TAKE A LOOK AT renumerate1
#    def renumerate1(self, num):
#        if self.type in modificators: return num, 0#0, 0
#        if self.attr(concept["order_number"]) == None:
#            res = 0
#        else:
#            res = abs(self.attr(concept["order_number"]) - num)
#        self.attr(concept["order_number"], num)
#        return num + 1, res

    def renumerate(self, num):
        if self.type in modificators: return num, 0#0, 0
        if num == None:
            if self.attr(concept["order_number"]) == None:
                return None, 0
            else:
                return self.attr(concept["order_number"]) + 1, 0
        if self.attr(concept["order_number"]) == None:
            res = 0
        else:
            res = abs(self.attr(concept["order_number"]) - num)
        return num + 1, res


    def descr(self):
        return "(" + str(self.text) + "[" + str(self.meaning) + "] " + str(self._attrs)
        #return "(" + str(str(self.text).encode("iso-8859-1")) + "[" + str(self.meaning) + "] " + str(self._attrs)
#    def __eq__(self, obj):
#        #print("zxx")
#        if obj is None:
#            return False
#        if not (self.type == obj.type and self.meaning == obj.meaning):
#            #print "zxx"
#            return False
#        for key in self._attrs.keys():
#            #if key == concept["TAGS: continue ####
#            if self._attrs.get(key, None) != obj._attrs.get(key, None):
#                #print "zxx"
#                return False
#        for key in obj._attrs.keys():
#            #if key == concept["TAGS: continue #####
#            if self._attrs.get(key, None) != obj._attrs.get(key, None):
#                #print "zxx"
#                return False
#        #print "zxx"
#        return True
#        #return False
#        #raise NotImplementedError


    def __ne__(self, obj):
        return not self.__eq__(obj)

    def fixed_with(self, name):
        return name in self.fixed

    def set_type(self, value):
        if value > LAST_TERMINAL:
            raise ArgumentError("in Word.type")

    def __init__(self, type = None, text = None, start = None, end = None):
        self.por = []
        self.text = text

        #######
        #self._attach = []
        self.fixed = []
        #######
        LingUnit.__init__(self, type, start, end)

    def __str__(self):
        if self.text == None: return ""
        s = ""
        for t in self.text:
            s += t + " "
        if self.attr(concept["noun-type"]) == noun_type["proper"]:
            s = s[0].upper() + s[1:]
        return s[:-1]#.decode("utf8")

    def set_text(self, value):
        self._text = value
#        _text = lower(value)
#        if Lang.is_punctuation(value):
#            self.type = SYNTACTIC_CATEGORY_PUNCTUATION
#            return
#        if Lang.modifiers.contains(_text):
#            pass
    def get_text(self):
        return self._text
    def del_text(self):
        del self._text
    text = property(get_text, set_text, del_text)



    def get_ltext(self):
        return self.text[-1]

    def set_ltext(self, value):
        self.text[-1] = value

    def del_ltext(self):
        del self.text[-1]

    ltext = property(get_ltext, set_ltext, del_ltext)

    