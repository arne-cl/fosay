__author__="zoltan kochan"
__date__ ="$5 бер 2011 21:28:42$"

import unittest
from core.models.lang import Language
from core.constants import concept

def equal(a, b):
    if str(a) != str(b):
        return False
    for attribute in a._attrs.keys(): #+b._attrs.keys()
        if attribute != concept["tags"] and \
           a.attr(attribute) != b.attr(attribute):
            return False
    return True

class LanguageTestCase(unittest.TestCase):
    def tdict(self, lang_name):
        lan = Language(lang_name)
        for i in range(len(lan.words)):
            for j in range(i + 1, len(lan.words)):
                self.assertFalse(equal(lan.words[i], lan.words[j]),
                    "Duplication:\n%s\nand\n%s"%(lan.words[i].descr(), lan.words[j].descr()))

    def test_ukr_dict(self):
        '''Test Ukrainian dictionary for duplications.'''
        self.tdict("ukr")

    def test_hun_dict(self):
        '''Test Hungarian dictionary for duplications.'''
        self.tdict("hun")

    def test_eng_dict(self):
        '''Test English dictionary for duplications.'''
        self.tdict("eng")

    
    def test_divide_into_words(self):
        eng = Language("eng")
        examples = [
            ('alpha, bravo, charlie delta', ["alpha", ", ", "bravo", ", ", "charlie", "delta"]),
            ('alpha, ', ["alpha", ", "]),
            (', alpha', [", ", "alpha"]),
            ('alpha.', ["alpha", ". "]),
            ('alpha. ', ["alpha", ". "]),
            (' alpha ', ["alpha"]),
        ]
        for s, expected in examples:
            actual = eng.divide_into_words(s)
            self.assertListEqual(actual, expected)