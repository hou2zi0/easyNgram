# Helper functions for wordNgram
# Code Styles nachschauen
import re
import nltk

# Helper functions for wordNgram
def boolArray(test_array):
    if False in test_array:
        return False
    else:
        return True
    
def resolve(gram,constraint,resolvedConstraints):
    try: 
        constraint_mode = constraint[2]
    except:
        constraint_mode = "orth"
        
    if constraint_mode.lower() == "orth":
        if constraint[0].startswith("~"):
            resolvedConstraints.append(not bool(re.search(r'{}'.format(constraint[0][1:]),gram['Orth'][constraint[1]-1])))
        else:
            resolvedConstraints.append(bool(re.search(r'{}'.format(constraint[0]),gram['Orth'][constraint[1]-1])))
    elif constraint_mode.lower() == "lemma":
        if constraint[0].startswith("~"):
            resolvedConstraints.append(not bool(re.search(r'{}'.format(constraint[0][1:]),gram['Lemmata'][constraint[1]-1])))
        else:
            resolvedConstraints.append(bool(re.search(r'{}'.format(constraint[0]),gram['Lemmata'][constraint[1]-1])))
    elif constraint_mode.lower() == "fg":
        if constraint[0].startswith("~"):
            resolvedConstraints.append(not bool(re.search(r'{}'.format(constraint[0][1:]),gram['FG_POS'][constraint[1]-1])))
        else:
            resolvedConstraints.append(bool(re.search(r'{}'.format(constraint[0]),gram['FG_POS'][constraint[1]-1])))
    elif constraint_mode.lower() == "cg":
        if constraint[0].startswith("~"):
            resolvedConstraints.append(not bool(re.search(r'{}'.format(constraint[0][1:]),gram['CG_POS'][constraint[1]-1])))
        else:
            resolvedConstraints.append(bool(re.search(r'{}'.format(constraint[0]),gram['CG_POS'][constraint[1]-1])))

def resolveConstraints(gram, constraints):
    resolvedConstraints = []
    if isinstance(constraints,(list,)):
        for constraint in constraints:
            resolve(gram,constraint,resolvedConstraints)
    elif isinstance(constraints,(tuple,)):  
        constraint = constraints
        resolve(gram,constraint,resolvedConstraints)
    else:
        print("Input error.")
        
    return resolvedConstraints


# ngram function
# WICHTIG: word und constraint nehmen jetzt RegExe entgegen, d.h. soll nach einem einzigen Wort gesucht werden 
# muss der RegEx gegebenenfalls mit Zeilenanfang "^" und Zeilenende "$" angegeben werden um eine "Fuzzy Search" auszuschließen
def wordNgram(text, # Erwartet eine Liste von Strings.
              word=False, # Das Wort nach dessen Kollokation gesucht wird, (word, position, mode). Mode may be
                          # 'orth' (default), 'lemma', 'FG' (fine grained POS), 'CG' (searchphrase grained POS).
              n=2, # Gibt die Anzahl der Grame an; 2 = Bigram, 3 = Trigram, etc.
              threshold=0, # Unter welcher Häufigkeit Gramme nicht mehr angezeigt werden soll
              constraint=False, # Ob ein anderes Wort mit spezifischer Position im Gram als 
                                # Constraint der Ergebnismenge dienen soll, e.g. (searchphrase, position, mode)
                                # constraint=("^muss$",2) => "muss" soll als zweites Wort im Gram auftauchen
                                # soll ein Constraint nicht mit in die Ergebnismenge aufgenommen werden, muss
                                # das Suchwort mit "~" präfigiert werden. Als Mode kann wie bei word 
                                # 'orth' (default), 'lemma', 'FG' (fine grained POS), 'CG' (coarse grained POS) angegeben
                                # werden.
              source="spacy",   # Source mode of text. By default a spacy token document is expected.
              boilDown=False # True converts all found ngrams to lower case. Thus the frequencies of ngrams 
                             # only distinguishable by case are summed up.
             ):
    ngrams_ = nltk.ngrams(text, n)
    
    ngram_list = []
    ngram_frequ = {}
    
    for grams in list(ngrams_):
        gram = {
            "Orth" : False,
            "FG_POS" : False,
            "CG_POS" : False,
            "Lemmata" : False
        }
        
        if source.strip().lower() == "spacy":
            gram["Orth"] = [token.orth_.strip() for token in grams]
            gram["FG_POS"] = [token.tag_.strip() for token in grams]
            gram["CG_POS"] = [token.pos_.strip() for token in grams]
            gram["Lemmata"] = [token.lemma_.strip() for token in grams]
        else:
            gram["Orth"] = [token.strip() for token in grams]
            
        gram_str = " ".join(gram['Orth'])
        
        if word != False:
            if isinstance(word[1],(int,)) == True and bool(constraint) == True:
                if boolArray(resolveConstraints(gram, word)) and boolArray(resolveConstraints(gram, constraint)):
                    ngram_list.append(gram_str)     
            elif isinstance(word[1],(int,)) == True:
                if boolArray(resolveConstraints(gram, word)):
                    ngram_list.append(gram_str)
            else:
                if True in [bool(re.search(r'{}'.format(word),i)) for i in gram['Orth'] ]:
                    ngram_list.append(gram_str)
        else:
            ngram_list.append(gram_str)
            
    if boilDown == True:
        ngram_list = [ ngram.lower() for ngram in ngram_list ]
        
    for ngram in set(ngram_list):
        count = ngram_list.count(ngram)
        if count > threshold:
            ngram_frequ[ngram] = count

    for entry in sorted(ngram_frequ, key=ngram_frequ.get, reverse=True):
        print("{} => {}".format(entry,ngram_frequ[entry]))
        
    return ngram_frequ
