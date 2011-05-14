import unittest
import yaml
import os
import sys
from functools import reduce
from core.lang.translate import translate

from core.models.lang import Language
lang = {
    "eng": Language("eng"),
    "hun": Language("hun"),
    "ukr": Language("ukr")
}

#s = ukr.synset("nixli")
#print([str(x) for x in s])

class TranslateTestCase(unittest.TestCase):
    def setUp(self):
        currentdir = str(os.path.dirname(sys.argv[0]))
        self.currentdir = reduce(os.path.join, [currentdir, "test", "core", "lang", "test_translate_data"])
    
    def lang_test(self, source_lang, target_lang):
        stream = open(os.path.join(self.currentdir, '%s_to_%s.yaml'%(source_lang, target_lang)) , 'r')
        tmp = yaml.load(stream)
        stream.close()
        
        first = "ip"
        for item in tmp:
            text, proper = item[source_lang], item[target_lang]
            translations = translate(text, first, lang[source_lang], [lang[target_lang]])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)
    
    def test_translate_ukr_to_eng(self):
        self.lang_test("ukr", "eng")

    def test_translate_eng_to_ukr(self):
        self.lang_test("eng", "ukr")

    def test_translate_hun_to_ukr(self):
        self.lang_test("hun", "ukr")

    def test_translate_ukr_to_hun(self):
        self.lang_test("ukr", "hun")

    def test_translate_hun_to_eng(self):
        self.lang_test("hun", "eng")

    def test_translate_eng_to_hun(self):
        self.lang_test("eng", "hun")