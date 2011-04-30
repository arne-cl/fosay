__author__="zoltan kochan"
__date__ ="$12 квіт 2011 1:25:23$"
import unittest
import core.compilers.cws as cws

class CwsTestCase(unittest.TestCase):
    def setUp(self):
        self.ptc = False

    def test_cws(self):
        tests = [
            '''
            "alpha"
            {
                number: singular;
                gender: masculine feminine;
            }
            ''',
            '''
            betta
            {
                case: accusative nominative;
            }
            "echo"[exo] "delta" :: betta
            {
                real-number: dual;
            }
            ''',
            '''
            "dog"[dog]
            {
                tags: slang ukrainian, russian;
                type: noun;
            }
            '''
        ]

        for test in tests:
            self.assertIsNotNone(cws.parse(test, self.ptc))

    def test_cws_errors(self):
        tests = [
            '''
            "alpha""
            {
                number: singular;
                gender: masculine feminine;
            }
            ''',
            '''
            betta
            {
                case: accusative nominative;
            }
            "echo"[exo] "delta" :: bett-a
            {
                real-number: dual;
            }
            ''',
#            '''
#            betta
#            {
#                ca-se: accusative nominative;
#            }
#            "echo"[exo] "delta" :: betta
#            {
#                real-number: dual;
#            }
#            ''',
            '''
            "dog"[dog]
            {
                tags: slang ukrainian, russian;
                type: nounl;
            }
            '''
        ]

        for test in tests:
            self.assertIsNone(cws.parse(test, self.ptc))