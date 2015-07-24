# Cascading Word Sheets #

---

**Cascading Word Sheets** (**CWS**) is a language used to describe the dictionary of a natural or constructed language.

Every word has a set of attributes, like: number, gender, case, form, person, time, etc. A dictionary is a place where this information can be stored. CWS is an instrument to represent this info.

# Syntax #

---

CWS looks like CSS:
```
"brother"[brəðər]
{
    lemma: "bruna";
    stem: "bruna.brother";
    real-number: singular;
    type: noun;
    number: singular;
    gender: masculine;
    persone: third;
    noun-type: common;
    case: nominative;
}
```
I guess only three attributes need explanation here: lemma, stem and real-number.
  * lemma is used to unambiguously define the word's meaning. To do so we need to anchor the word to a Lojban word which is always unambiguous.
  * stem is used to tie different forms of one word in the language. E.g. _"brother"_, _"brothers"_ and _"brother's"_ all will have the same stem - "bruna.brother"
  * real-number is used to define the number de facto of the word
Yet two attributes aren't required in the example above: lemma and real-number. If we do not specify the lemma then it's taken from the stem (it's part before the period). If we do not specify real-number then it's value will be equal to it's number.

But if we'll write every word in the dictionary with so many attributes it will be too cumbersome. That's why bases were invented. A base is not a part of the dictionary but a tool to generate the dictionary.
```
simple-noun
{
    type: noun;
    number: singular;
    gender: masculine;
    persone: third;
    noun-type: common;
    case: nominative;
}
."brother"[brəðər] :: simple-noun { stem: "bruna.brother" }
."father"[fɑðər]   :: simple-noun { stem: "patfu.father"  }
."son"[sən]        :: simple-noun { stem: "bersa.son"     }
```
In this example 'simple-noun' is a base which extends "brother", "father" and "son" with the lacking attributes.