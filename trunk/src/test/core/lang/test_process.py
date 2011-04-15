import unittest
from core.constants import *
from core.models.lang import Language
#from core.lang.atn.jbo import atn
from core.lang.process import lang_to_case_frame

class LangToCaseFrameTestCase(unittest.TestCase):
    def setUp(self):
        self.ilang = Language("jbo")

    def test_lang_to_case_frame(self):
        st = self.ilang.init_sentence("melbi nanla", "np")
        cf = lang_to_case_frame(st[-1])
        print(cf)
        tcf = \
            {
                concept['noun-phrase']:
                    {
                        concept['noun']:
                            {
                                concept['meaning']: 'nanla',
                                concept['noun-type']: noun_type['common'],
                                concept['form']: None,
                                concept['order-number']: None,
                                concept['real-number']: None,
                                concept['tags']: None
                            },
                        concept['epithet']:
                            {
                                concept['adjective']:
                                    {
                                        concept['meaning']: 'melbi',
                                        concept['order-number']: None
                                    }
                            },
                        concept['difinity']: difinity['difinite'], #######UNDIFINITE!!!!
                        concept['quantity']: None,
                        concept['quantity-number']: None,
                        concept['persone']: persone['third']
                    }
            }
        self.assertDictEqual(cf, tcf)
#        AdjToken = Token(TERMINAL_ADJECTIVE)
#        NounToken = Token(TERMINAL_NOUN)
#        AdjPhrase = FlowerLingUnit(NONTERMINAL_EPITHET, 0, 0)
#        NounPhrase = FlowerLingUnit(NONTERMINAL_NOUN_PHRASE, 0, 0)
#
#        AdjPhrase.blocks = [AdjToken]
#        NounPhrase.left = [AdjPhrase]
#        NounPhrase.blocks = [NounToken]