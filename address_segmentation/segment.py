from address_segmentation.config import *
import itertools as it

def segmentText(text):
    text = text.strip(' \n,.')
    # text = text.strip(''.join(split_characters.keys()))

    # ========= 1 ========================

    terms = []
    _ = 0
    for c in range(1, text.__len__()):
        if (text[c] in split_characters):
            # if (text[c] not in ' /\\+('):
                terms.append(text[_:c+1])
                _ = c + 1
    terms.append(text[_:c + 1])

    _ = []
    for term in terms:
        # print(term)
        if (len(term) > 0):
            if (_.__len__() == 0):
                _.append(term)
            elif (len(term) == 1 and term in split_characters.keys()):
                if (split_characters[_[-1][-1]] < split_characters[term[-1]]):
                    _[-1] += term
                else:
                    _.append(term)
            elif (_[-1].strip(''.join(split_characters.keys())) == ''):
                _[-1] += term
            else:
                _.append(term)

    terms = _

    ls = []
    for cb in list(it.combinations(range(len(terms) - 1), 2)):
        term1 = ''.join(terms[:cb[0] + 1])
        term2 = ''.join(terms[cb[0] + 1:cb[1] + 1])
        term3 = ''.join(terms[cb[1] + 1:])
        _f = lambda x: 1 if len(x) == 0 else 1 if x[-1] not in split_characters else split_characters[x[-1]]
        score = _f(term1) * _f(term2) * _f(term3)
        ls.append([term1, term2, term3, score])

    return ls