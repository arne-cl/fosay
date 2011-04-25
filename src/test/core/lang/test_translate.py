import unittest
from core.lang.translate import translate

from core.models.lang import Language
eng = Language("eng")
hun = Language("hun")
ukr = Language("ukr")

#s = ukr.synset("nixli")
#print([str(x) for x in s])

class TranslateTestCase(unittest.TestCase):
    ukr_to_eng = [
    (
        "Всі хлопці бачили багатьох дівчат.",
        [
            'Every boy saw many girls.',
            'All the boys saw many girls.',
            'Every boy has been seeing many girls.',
            'All the boys have been seeing many girls.',
        ]
    ),
    (
        "Декілька хлопців бачили дівчат.",
        [
            "A few boys saw girls.",
            'A few boys have been seeing girls.'
        ]
    ),
    (
        "Кожен хлопець бачив багатьох гарних і розумних дівчат.",
        [
            "Each boy saw many beautiful and smart girls.",
            "Each boy has been seeing many beautiful and smart girls.",
        ]
    ),
    (
        "Хлопець бачитиме дівчат і жінок.",
        [
            "A boy will see girls and women."
        ]
    ),
    (
        "Я бачив тебе.",
        [
            "I saw you.",
            "I have been seeing you."
        ]
    ),
    ]

    def test_translate_ukr_to_eng(self):
        first = "ip"
        source_lang = ukr
        target_lang = eng
        for text, proper in self.ukr_to_eng:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)

    eng_to_ukr = [
    (
        "The woman's house saw a boy.",
        [
            "Будинок жінки бачив хлопця.",
        ],
    ),
    (
        "I see you.",
        [
            "Я бачу вас."
        ]
    ),
    (
        "Today the boy will see the house of the woman.",
        [
            "Сьогодні хлопець бачитиме будинок жінки.",
        ],
    ),
    ]

    def test_translate_eng_to_ukr(self):
        first = "ip"
        source_lang = eng
        target_lang = ukr
        for text, proper in self.eng_to_ukr:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)

    hun_to_ukr = [
    (
        "Néhány fiú látott sok szép lányt.",
        [
            "Декілька хлопців бачили багатьох гарних дівчат."
        ]
    ),
    (
        "A fiú látta egy okos nőnek a szép házát.",
        [
            "Хлопець бачив гарний будинок розумної жінки."
        ]
    )
    ]

    def test_translate_hun_to_ukr(self):
        first = "ip"
        source_lang = hun
        target_lang = ukr
        for text, proper in self.hun_to_ukr:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)

    ukr_to_hun = [
    (
        "Всі хлопці бачили багатьох дівчат.",
        [
            'Az összes fiú látott sok lányt.'
        ]
    ),
    (
        "Декілька хлопців бачили дівчат.",
        [
            "Néhány fiú látott lányokat."
        ]
    ),
    (
        "Хлопець бачитиме дівчат і жінок.",
        [
            "Egy fiú látni fog lányokat s nőket.",
            "Egy fiú látni fog lányokat és nőket.",
            "Egy fiú látni fog lányokat meg nőket.",
        ]
    ),
    (
        "Бачу тебе.",
        [
            "Látlak.",
            "Látlak.",
            "Látlak.",
        ]
    ),
    ]

    def test_translate_ukr_to_hun(self):
        first = "ip"
        source_lang = ukr
        target_lang = hun
        for text, proper in self.ukr_to_hun:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)

    hun_to_eng = [
    (
        "Néhány fiú látott sok szép lányt.",
        [
            "A few boys saw many beautiful girls.",
            "A few boys have been seeing many beautiful girls.",
        ]
    ),
    (
        "A fiú látta egy okos nőnek a szép házát.",
        [
            "The boy saw a smart woman's beautiful house.",
            "The boy has been seeing a smart woman's beautiful house."
        ]
    ),
    (
        "Egy lány vett egy házat Londonban.",
        [
            "A girl bought a house in London.",
            "A girl has been buying a house in London."
        ]
    ),
    ]

    def test_translate_hun_to_eng(self):
        first = "ip"
        source_lang = hun
        target_lang = eng
        for text, proper in self.hun_to_eng:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)

    eng_to_hun = [
    (
        "The woman's house saw a boy.",
        [
            "A nő háza látott egy fiút.",
        ]
    ),
    (
        "Zoltan Kochan saw a house.",
        [
            "Kocsán Zoltán látott egy házat.",
        ]
    ),
    ]

    def test_translate_eng_to_hun(self):
        first = "ip"
        source_lang = eng
        target_lang = hun
        for text, proper in self.eng_to_hun:
            translations = translate(text, first, source_lang, [target_lang])
            #self.assertSameElements(translations[0], proper)
            self.assertSameElements(translations[0], proper)