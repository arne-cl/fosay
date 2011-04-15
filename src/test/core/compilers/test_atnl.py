__author__="zoltan kochan"
__date__ ="$18 бер 2011 0:35:07$"
import unittest
import core.compilers.atnl as atnl
import core.constants as const
from core.constants import concept, gender, number

class AtnlTestCase(unittest.TestCase):
    def setUp(self):
        self.ptc = False
        #self.foo = Test_atnl()
    

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_atnl(self):
        self.assertIsNotNone(atnl.parse("np :- \n $N", self.ptc))
        self.assertIsNotNone(atnl.parse("np :- \n $N<number, $case->gender>", self.ptc))
        self.assertIsNotNone(atnl.parse("np :- \n $N<number, case->gender>{gender: feminine}", self.ptc))
        
    def test_atnl_errors(self):
        self.assertIsNone(atnl.parse("np :- \n $N<number, $caste->gender>", self.ptc))
        self.assertIsNone(atnl.parse("np :- \n $N<number, case->gender>{gender: fkeminine}", self.ptc))
        self.assertIsNone(atnl.parse("np :- \n $N<number, case->gender>{geonder: feminine}", self.ptc))
        self.assertIsNone(atnl.parse("np :- \n $Nbb<number, case->gender>{geonder: feminine}", self.ptc))
        self.assertIsNone(atnl.parse("npb :- \n $N<number, case->gender>{gender: feminine}", self.ptc))
        self.assertIsNone(atnl.parse("\nn--p :- \n $N<8number, case->gender>{gender: feminine}", self.ptc))
        self.assertIsNone(atnl.parse("np :- \n $N<num---ber, case->gender>{gender: feminine}", self.ptc))
        self.assertIsNone(atnl.parse('np :- \n $N<number, case->gender>{gender: ".uioou}', self.ptc))

    def test_div_to_op(self):
        tests = [
            (
            # alpha
            # [bravo]
            {
                1: [('alpha', None, 0.0, 2)],
                2: [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
            },
            (
                [
                   [('alpha', None, 0.0, 2)]
                ]
                ,
                [
                   [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
                ]
            )
            ),
            (
            # [alpha]
            # [bravo]
            {
                1: [('alpha', None, 0.0, 2),               ('JMP', None, 0.0, 2)],
                2: [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
            },
            (
                []
                ,
                [
                   [('alpha', None, 0.0, 2),               ('JMP', None, 0.0, 2)],
                   [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
                ]
            )
            ),
            (
            # alpha
            # bravo
            {
                1: [('alpha', None, 0.0, 2)],
                2: [('bravo', None, 0.0, const.STATE_END)]
            },
            (
                [
                   [('alpha', None, 0.0, 2)],
                   [('bravo', None, 0.0, const.STATE_END)]
                ]
                ,
                []
            )
            ),
            (
            # alpha bravo
            {
                1: [('alpha', None, 0.0, const.STATE_END), ('bravo', None, 0.0, const.STATE_END)]
            },
            (
                [
                   [('alpha', None, 0.0, const.STATE_END), ('bravo', None, 0.0, const.STATE_END)]
                ]
                ,
                []
            )
            ),
        ]
        
        for par, target in tests:
            self.assertEqual((atnl.div_to_op(par)), target)

    def test_concat(self):
        tests = [
            (
                (
                {
                    1: [('alpha', None, 0.0, const.STATE_END)]
                },
                        ('delta', None, 0.0, const.STATE_END)
                ),
                {
                    1: [('alpha', None, 0.0, 2)],
                    2: [('delta', None, 0.0, const.STATE_END)]
                }
            ),
            (
                (
                {
                    1: [('alpha',   None, 0.0, 6)],
                    6: [('india',   None, 0.0, const.STATE_END)],
                },
                       [('foxtrot', None, 0.0, const.STATE_END)]
                ),
                {
                    1: [('alpha',   None, 0.0, 6)],
                    6: [('india',   None, 0.0, 7)],
                    7: [('foxtrot', None, 0.0, const.STATE_END)],
                }
            ),
            (
                (
                {
                    1: [('alpha',   None, 0.0, 2)],
                    2: [('india',   None, 0.0, const.STATE_END)],
                },
                {
                    1: [('juliet',  None, 0.0, 2), ('JMP', None, 0.0, 3)],
                    2: [('foxtrot', None, 0.0, 3), ('JMP', None, 0.0, 3)],
                    3: [('kilo',    None, 0.0, const.STATE_END)],
                }
                ),
                {
                    1: [('alpha',   None, 0.0, 2)],
                    2: [('india',   None, 0.0, 3)],
                    3: [('juliet',  None, 0.0, 4), ('JMP', None, 0.0, 5)],
                    4: [('foxtrot', None, 0.0, 5), ('JMP', None, 0.0, 5)],
                    5: [('kilo',    None, 0.0, const.STATE_END)],
                }
            ),
        ]
        
        for par, target in tests:
            self.assertEqual((atnl.concat(par[0], par[1])), target)

    def test_add_priorities(self):
        tests = [
            (
            (
            {
                'tango':
                {
                    1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                    2: [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
                }
            },
            {
                'tango': [(0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
            }
            ),
            {
                'tango':
                {
                    1: [('alpha', None, 0.87, 2), ('uniform', None, 0.34, const.STATE_END),],
                    2: [('bravo', None, 0.87, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
                }
            }
            ),
            (
            (
            {
                'tango':
                {
                    1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                    2: [('bravo', None, 0.0, const.STATE_END), ('bravo', None, 0.0, 3), ('JMP', None, 0.0, const.STATE_END)],
                    3: [('delta', None, 0.0, const.STATE_END)]
                }
            },
            {
                'tango': [(0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
            }
            ),
            {
                'tango':
                {
                    1: [('alpha', None, 0.87, 2), ('uniform', None, 0.34, const.STATE_END),],
                    2: [('bravo', None, 0.87, const.STATE_END), ('bravo', None, 0.0, 3), ('JMP', None, 0.0, const.STATE_END)],
                    3: [('delta', None, 0.0, const.STATE_END)]
                }
            }
            ),
            (
            (
            {
                'tango':
                {
                    1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                    2: [('bravo', None, 0.0, const.STATE_END), ('JMP', None, 0.0, const.STATE_END)]
                }
            },
            {
                'tango': [(0.98, ['alpha', 'JMP']), (0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
            }
            ),
            {
                'tango':
                {
                    1: [('alpha', None, 0.98, 2), ('uniform', None, 0.34, const.STATE_END),],
                    2: [('bravo', None, 0.87, const.STATE_END), ('JMP', None, 0.98, const.STATE_END)]
                }
            }
            ),
        ]

        for par, target in tests:
            atnl.add_priorities(par[0], par[1])
            self.assertEqual(par[0], target)
    def test_optional_state(self):
        s = "[obj]"