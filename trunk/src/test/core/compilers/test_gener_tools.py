__author__="zoltan kochan"
__date__ ="$27 бер 2011 4:07:25$"
import unittest

import core.compilers.gener_tools as gtools
from core.compilers.gener_tools import add_to_blocks, add_to_left

import core.constants as const
from core.constants import concept, number, gender, case

class GenerToolsTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Test_gener_tools()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_unite(self):
        tests = [
            (
            (
                {
                    1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END)],
                    2: [('YANKEE', None, 0.0, const.STATE_END)],
                    const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
                },
                {
                    1: [('SIERRA', None, 0.0, 2)],
                    2: [('WHISKY', None, 0.0, const.STATE_END)],
                }
            ),
            {
                1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END), ('SIERRA', None, 0.0, 3)],
                2: [('YANKEE', None, 0.0, const.STATE_END)],
                3: [('WHISKY', None, 0.0, const.STATE_END)],
                const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
            }
            ),
            (
            (
                {
                    1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END)],
                    2: [('YANKEE', None, 0.0, const.STATE_END)],
                },
                {
                    1: [('SIERRA', None, 0.0, 2)],
                    2: [('WHISKY', None, 0.0, const.STATE_END)],
                    const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
                }
            ),
            {
                1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END), ('SIERRA', None, 0.0, 3)],
                2: [('YANKEE', None, 0.0, const.STATE_END)],
                3: [('WHISKY', None, 0.0, const.STATE_END)],
                const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
            }
            ),
        ]
        for par, target in tests:
            actual = gtools.unite(par[0], par[1])
            self.assertDictEqual(actual, target)

        self.assertRaises(Exception, gtools.unite, ((
            (
                {
                    1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END)],
                    2: [('YANKEE', None, 0.0, const.STATE_END)],
                },
                {
                    1: [('SIERRA', None, 0.0, 2)],
                    2: [('WHISKY', None, 0.0, const.STATE_END)],
                    const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
                }
            ),
            {
                1: [('KILO', None, 0.0, 2), ('ECHO', None, 0.0, const.STATE_END), ('SIERRA', None, 0.0, 3)],
                2: [('YANKEE', None, 0.0, const.STATE_END)],
                3: [('WHISKY', None, 0.0, const.STATE_END)],
                const.STATE_CONJ_A1: [('QUEBEC', None, 0.0, const.STATE_END)]
            }
            )))


    def test_compr(self): #functions should be equal too!!!!
        fa1 = dict(
            f = add_to_blocks,
            up = [(concept['number'], number['singular']), (concept['gender'], gender['feminine'])],
            down = [(concept['case'], case['elative'])],
            attach = [concept['tense'], concept['gender']],
            fixed = [concept['difinity'], concept['real-number']])
        fa2 = dict(
            f = add_to_blocks,
            up = [(concept['gender'], gender['feminine']), (concept['number'], number['singular'])],
            down = [(concept['case'], case['elative'])],
            attach = [concept['gender'], concept['tense']],
            fixed = [concept['real-number'], concept['difinity']])

        fb = dict(
            f = add_to_left,
            up = [(concept['gender'], gender['masculine'])],
            down = [(concept['case'], case['nominative'])],
            fixed = [concept['persone'], concept['tense']])

        tests = [
            (
                {
                    1: [('GOLF', None, 0.0, 3), ('GOLF', None, 0.0, 2)],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                    3: [('LIMA', None, 0.0, const.STATE_END)],
                },
                {
                    1: [('GOLF', None, 0.0, 2),],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                }
            ),
            (
                {
                    1: [('GOLF', None, 0.0, 2), ('CHARLIE', None, 0.0, 3), ('GOLF', None, 0.0, 3)],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                    3: [('LIMA', None, 0.0, const.STATE_END)],
                },
                {
                    1: [('GOLF', None, 0.0, 2), ('CHARLIE', None, 0.0, 3),],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                    3: [('LIMA', None, 0.0, const.STATE_END)],
                }
            ),
            (
                {
                    1: [('GOLF', None, 0.0, 2), ('CHARLIE', None, 0.0, 3), ('GOLF', None, 0.0, 3)],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                    3: [('LIMA', None, 0.0, const.STATE_END)],
                },
                {
                    1: [('GOLF', None, 0.0, 2), ('CHARLIE', None, 0.0, 3),],
                    2: [('LIMA', None, 0.0, const.STATE_END)],
                    3: [('LIMA', None, 0.0, const.STATE_END)],
                }
            ),
            (
                {
                    1: [('GOLF', None, 0.3, 2), ('GOLF', None, 0.6, const.STATE_END)],
                    2: [('LIMA', None, 0.9, const.STATE_END)],
                },
                {
                    1: [('GOLF', None, 0.3, 2), ('GOLF', None, 0.6, const.STATE_END)],
                    2: [('LIMA', None, 0.9, const.STATE_END)],
                }
            ),
            (
                {
                    1: [('GOLF', fa1, 0.0, 3), ('GOLF', fa2, 0.0, 2)],
                    2: [('LIMA', fa1, 0.0, const.STATE_END)],
                    3: [('LIMA', fb, 0.0, const.STATE_END)],
                },
                {
                    1: [('GOLF', fa2, 0.0, 2),],
                    2: [('LIMA', fa1, 0.0, const.STATE_END), ('LIMA', fb, 0.0, const.STATE_END)],
                }
            ),
            (
                {
                    1: [('WHISKY', None, 0.23, const.STATE_END)],
                    2: [('PAPA', None, 0.0, 2)],
                },
                {
                    1: [('WHISKY', None, 0.23, const.STATE_END)]
                }
            ),
            (
                {
                    1: [('WHISKY', None, 0.23, const.STATE_END)],
                    2: [('PAPA', None, 0.0, 3)],
                    3: [('X-RAY', None, 0.0, 2)]
                },
                {
                    1: [('WHISKY', None, 0.23, const.STATE_END)]
                }
            ),
#            (
#                {
#                    -4: [('HOTEL', None, 0.0, -3)],
#                    -3: [('VICTOR', None, 0.0, -4), ('VICTOR', None, 0.0, const.STATE_END)],
#                    -2: [('HOTEL', None, 0.0, -1)],
#                    -1: [('VICTOR', None, 0.0, -2), ('VICTOR', None, 0.0, const.STATE_END)],
#                    1: [('GOLF', fa1, 0.0, -2), ('GOLF', fa2, 0.0, -4)],
#                },
#                {
#                    -2: [('HOTEL', None, 0.0, -1)],
#                    -1: [('VICTOR', None, 0.0, -2), ('VICTOR', None, 0.0, const.STATE_END)],
#                    1: [('GOLF', fa2, 0.0, 2),],
#                }
#            ),
        ]
        for par, target in tests:
            actual = gtools.compr(par, True)
            #print(actual)
            self.assertEqual(actual, target)

if __name__ == '__main__':
    unittest.main()

