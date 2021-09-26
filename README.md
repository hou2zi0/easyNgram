# easyNgram

## How to use

### Load the required libraries in your Notebook

```python
import pandas as pd
import numpy as np
import spacy
import nltk
import re
```

### Load the easyNgram code in your Notebook

Just put the code within `easyNgram.py` in your Notebook or use the `basic_usage_notebook.ipynb` file.

### Load the Spacy Language Class


```python
German = spacy.load('de_core_news_sm')
English = spacy.load('en_core_web_sm')
```

### Load the text


```python
# The Phoenix on the Sword. (2012, November 9). In Wikisource . Retrieved 15:17, September 26, 2021, from https://en.wikisource.org/w/index.php?title=The_Phoenix_on_the_Sword&oldid=4132475
text = """"Know, oh prince, that between the years when the oceans drank Atlantis and the gleaming cities, and the years of the rise of the Sons of Aryas, there was an Age undreamed of, when shining kingdoms lay spread across the world like blue mantles beneath the stars — Nemedia, Ophir, Brythunia, Hyperborea, Zamora with its dark-haired women and towers of spider-haunted mystery, Zingara with its chivalry, Koth that bordered on the pastoral lands of Shem, Stygia with its shadow-guarded tombs, Hyrkania whose riders wore steel and silk and gold. But the proudest kingdom of the world was Aquilonia, reigning supreme in the dreaming west. Hither came Conan, the Cimmerian, black-haired, sullen-eyed, sword in hand, a thief, a reaver, a slayer, with gigantic melancholies and gigantic mirth, to tread the jeweled thrones of the Earth under his sandalled feet."

— The Nemedian Chronicles.

Over shadowy spires and gleaming towers lay the ghostly darkness and silence that runs before dawn. Into a dim alley, one of a veritable labyrinth of mysterious winding ways, four masked figures came hurriedly from a door which a dusky hand furtively opened. They spoke not but went swiftly into the gloom, …""".replace('\n', ' ').replace('  ', ' ').strip()
```

### Process the text with the language class


```python
spacyDocument = English(text)
```

### Use the spaCy document for your queries

#### Show nGrams

`n=2` sets the length of the ngram to two.
The function returns a dictionary object taht may be used further.


```python
wordNgram(spacyDocument, n=2)
```

    . " => 28
    , and => 18
    of the => 17
    in the => 13
    " " => 13
    , " => 13
    the king => 7
    , a => 6
    from the => 6
    ? " => 6
    …

    {'our positions': 1,
     'north to': 1,
     'denounces Conan': 1,
     'or beyond': 1,
     'snarl .': 1,
     ', hiding': 2,
     'I was': 2,
     'whom Conan': 1,
     'that Ascalante': 1,
     ...}



## Specific co-occurrences

When you want to search for specific co-occurrences, just provide an tuple as argument on position two or as named argument `word`, that details the pivot for the co-occurrence. 

```python
(
    'Conan',
    1
)
```

The word whose collocation is being searched for (word, position, mode). `mode` can be 'orth' (standard), 'lemma', 'FG' (fine-grained POS), 'CG' (search term-grained POS).

The available POS tags for coarse grained tagging are shared among languages: https://universaldependencies.org/docs/u/pos/

The available POS tags for fine grained tagging differ among languages. You'll have to look it up in the spaCy model's documentation: https://spacy.io/models/de


```python
wordNgram(spacyDocument, word=('Conan',1), n=2)
```

    Conan killed => 1
    Conan a => 1
    Conan 's => 1
    Conan laughs => 1
    Conan as => 1
    Conan in => 1
    Conan ? => 1
    Conan will => 1
    Conan , => 1
    Conan makes => 1


```python
wordNgram(spacyDocument, ('PROPN', 2, 'CG'), n=4, boilDown=True)
```

    of aryas , there => 1
    black legion . through => 1
    , brythunia , hyperborea => 1
    king conan 's right­hand => 1
    , gromel 's black => 1
    by mitra , i => 1
    see thoth - amon => 1
    ? volmana , the => 1
    …


You may use regex patterns on  the string position:


```python
wordNgram(spacyDocument, ('ma[kd]e[s]{0,1}',2), n=3, boilDown=True)
```

    wealth made that => 1
    volmana made it => 1
    conan makes a => 1


## Adding further constraints

Whether another word with a specific position in the ngram should serve as a constraint of the result set, e.g. (searchphrase, position, mode) constraint=("^must$",2) => "must" should appear as the second word in the gram If a constraint is not to be included in the result set, the search word must be prefigured with "~". As with word, 'orth' (default), 'lemma', 'FG' (fine grained POS), 'CG' (coarse grained POS) can be specified as the mode.


```python
# Forces a Proper Noun on position one and an Auxiliary Verb on position 2: 
wordNgram(spacyDocument, ('PROPN', 1, 'CG'), n=3, constraint=('AUX', 2, 'CG'), boilDown=True)
```

    ascalante is in => 1
    rinaldo has no => 1
    rinaldo is a => 1


```python
# Forces a Proper Noun on position one and NO Punctuation (`~PUNCT`) on position 3: 
wordNgram(spacyDocument, ('PROPN', 1, 'CG'), n=3, constraint=('~PUNCT', 3, 'CG'), boilDown=True)
```

    thoth - amon => 2
    gromel i 've => 1
    trocero of poitain => 1
    stygia with its => 1
    rinaldo is a => 1
    poitain , seneschal => 1
    …


```python
wordNgram(spacyDocument, ('PROPN', 1, 'CG'), n=3, constraint=[('~PUNCT', 2, 'CG'), ('~PUNCT', 3, 'CG')], boilDown=True)
```

    aquilonian started up => 1
    gromel i 've => 1
    ascalante turned again => 1
    trocero of poitain => 1
    age undreamed of => 1
    hyrkania whose riders => 1
    sons of aryas => 1
    gromel 's black => 1
    dion thinks that => 1
    stygia with its => 1
    …

```python
wordNgram(spacyDocument, ('ADJ', 3, 'CG'), n=3, constraint=('AUX', 2, 'CG'), boilDown=True)
```

    and are likely => 1
    it was easy => 1
    he was bidden => 1
    will be sufficient => 1


Using regex patternms allows to chain POS tags together in a query.


```python
wordNgram(spacyDocument, ('(PROPN|NOUN|PRON)', 3, 'CG'), n=3, constraint=('AUX', 2, 'CG'), boilDown=True)
```

    who are they => 1
    to do him => 1
    why does he => 1
    i have work => 1
    world was aquilonia => 1
    " had i => 1




```python
wordNgram(spacyDocument, ('(PROPN|NOUN|PRON)', 1, 'CG'), n=2, constraint=('VERB', 2, 'CG'), boilDown=True)
```

    you know => 2
    i will => 2
    we send => 1
    stygian shrugged => 1
    time comes => 1
    you dare => 1
    dreams stir => 1
    …
