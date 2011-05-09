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
        tests = [
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N;
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, $case->gender>;
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, case->gender>{gender: feminine};
            """,
        ]
        for txt in tests:
            self.assertIsNotNone(atnl.parse(txt, self.ptc))
        
    def test_atnl_errors(self):
        tests = [
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, $caste->gender>;
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, case->gender>{gender: fkeminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, case->gender>{geonder: feminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $Nbb<number, case->gender>{geonder: feminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            npb :-
                $N<number, case->gender>{gender: feminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            n--p :-
                $N<8number, case->gender>{gender: feminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<num---ber, case->gender>{gender: feminine};
            """,
            """
            np is noun-phrase;
            N is noun;
            np :-
                $N<number, case->gender>{gender: ".uioou};
            """,
        ]
        for txt in tests:
            self.assertIsNone(atnl.parse(txt, self.ptc))

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
        epsilon = const.type['epsilon']
        tests = [
            (
                (
                    { #tango :- alpha [bravo] | uniform;
                        'tango':
                        {
                            1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                            2: [('bravo', None, 0.0, const.STATE_END), (epsilon, None, 0.0, const.STATE_END)]
                        }
                    },
                    { #tango := 0.87: alpha bravo | 0.34: uniform
                        'tango': [(0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('alpha', None, 0.87, 2), ('uniform', None, 0.34, const.STATE_END),],
                        2: [('bravo', None, 0.87, const.STATE_END), (epsilon, None, 0.0, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                            2: [('bravo', None, 0.0, const.STATE_END), ('bravo', None, 0.0, 3), (epsilon, None, 0.0, const.STATE_END)],
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
                        2: [('bravo', None, 0.87, const.STATE_END), ('bravo', None, 0.0, 3), (epsilon, None, 0.0, const.STATE_END)],
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
                            2: [('bravo', None, 0.0, const.STATE_END), (epsilon, None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.98, ['alpha', epsilon]), (0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('alpha', None, 0.98, 2), ('uniform', None, 0.34, const.STATE_END),],
                        2: [('bravo', None, 0.87, const.STATE_END), (epsilon, None, 0.98, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [('alpha', None, 0.0, 2), ('uniform', None, 0.0, const.STATE_END),],
                            2: [('bravo', None, 0.0, const.STATE_END), (epsilon, None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.98, ['alpha']), (0.87, ['alpha', 'bravo']), (0.34, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('alpha', None, 0.98, 2), ('uniform', None, 0.34, const.STATE_END),],
                        2: [('bravo', None, 0.87, const.STATE_END), (epsilon, None, 0.98, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [(epsilon, None, 0.0, 2), ('uniform', None, 0.0, 2)],
                            2: [('alpha', None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.98, ['alpha']), (0.98, ['uniform', 'alpha'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [(epsilon, None, 0.98, 2), ('uniform', None, 0.98, 2),],
                        2: [('alpha', None, 0.98, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [('uniform', None, 0.0, 2)],
                            2: [(epsilon, None, 0.0, 3)],
                            3: [(epsilon, None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.56, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('uniform', None, 0.56, 2)],
                        2: [(epsilon, None, 0.56, 3)],
                        3: [(epsilon, None, 0.56, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [('uniform', None, 0.0, 2)],
                            2: [(epsilon, None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.56, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('uniform', None, 0.56, 2)],
                        2: [(epsilon, None, 0.56, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [(epsilon, None, 0.0, const.STATE_END)],
                        }
                    },
                    {
                        'tango': [(0.56, ['uniform'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [(epsilon, None, 0.0, const.STATE_END)]
                    }
                }
            ),
            (
                (
                    {
                        'tango':
                        {
                            1: [('uniform', None, 0.0, 2)],
                            2: [(epsilon, None, 0.0, 3)],
                            3: [('x-ray', None, 0.0, const.STATE_END)]
                        }
                    },
                    {
                        'tango': [(0.56, ['uniform', 'x-ray'])]
                    }
                ),
                {
                    'tango':
                    {
                        1: [('uniform', None, 0.56, 2)],
                        2: [(epsilon, None, 0.56, 3)],
                        3: [('x-ray', None, 0.56, const.STATE_END)]
                    }
                }
            ),
        ]

        for par, target in tests:
            atnl.add_priorities(par[0], par[1])
            self.assertEqual(par[0], target)
    def test_optional_state(self):
        s = "[obj]"