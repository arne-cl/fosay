# Augmented Transition Network Language #

---

**Augmented Transition Network Language** (**ATNL**) is a language used to describe the grammar of a natural or constructed language.


## Syntax ##

---

An ATN consists of a set of rules which makes the language grammar. E.g. the simplest English noun-phrase consist of an article and a noun: _"the house"_, _"an apple"_, _"the girls"_, etc. This is how this rule is described in ATNL:
```
np :-
    ART
    $N;
```
Above,
  * np is the rule's name
  * ART and N are the names of terminals (word types)
  * $ shows which word is the main in the phrase (rule)
But it's the simplest kind of noun-phrase. There are also noun-phrases with epithets: _"the big house"_, _"a red apple"_, _"the beautiful girls"_, etc. In this case we should describe a new rule for adjective-phrases and change the noun-phrase rule:
```
ap :-
    $ADJ;
np :-
    ART
    [ap]
    $N;
```
`[...`] shows the part of the rule which is optional.

OK, as you can see, the rules for English noun-phrases are really simple because they are context-free. But how do we handle a context-sensitive noun-phrase? E.g. a Spanish noun-phrase is always context-sensitive because the article, adjective and noun should have the same number and gender: _"las grandes casas"_, _"una manzana roja"_, _"las hermosas chicas"_, etc. But the rule above will produce also invalid phrases like: _"las grande casa"_, _"la hermosa chicas"_, _"una manzana rojo"_ etc. To exclude such results the ATN should be as follows:
```
ap :-
    $ADJ<$number; $gender>;
np :-
    ART<number; gender>
    [ap<number; gender>]
    $N<$number; $gender>;
```
Here `<number; gender> shows that the number and gender of the terminal/nonterminal should be the same as it's parent's(rule's). `$number shows that if there are more than one elements which have influence to the number of the rule then the current element's number will be assigned as the rule's number and the others will be compared to it.