from spellCorrecter import WORDS, P
from collections import Counter

def correction(word): 
    "Most probable spelling correction for word."
    cand = candidates(word)
    if not candidates(word):
         return word
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known(edits1(word)) or known(edits2(word)) )
#known([word]) or or [word]

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def translate(sentance):
    original = sentance.split(' ')
    newsent = ""
    for orig in original:
         newsent += (" " +  correction (orig.lower()))
    return newsent
 #('people like to carry weight')
#print translate('horses love chicken')

