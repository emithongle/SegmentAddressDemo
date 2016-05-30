from address_segmentation.segment import segmentText, preprocessPuncText, findPoses, removeKeyword, combinationTerm
from address_segmentation.model import clasify, checkCandidate
from address_segmentation.config import models, term_regex, email_regex, url_regex, string
from math import log
import copy

def segment_api_v1_0(text):

    templateList = segmentText(text)

    # bestSegment = {}
    # bestScore = - float('inf')
    results = []
    m = {0: 'name', 1: 'address', 2: 'phone'}

    for j, tm in enumerate(templateList):
        label_0, score_0 = clasify(models, tm[0])
        label_1, score_1 = clasify(models, tm[1])
        label_2, score_2 = clasify(models, tm[2])

        totalScore = log(score_0.max()) + log(score_1.max()) + log(score_2.max()) + log(tm[3])
        if (sorted([label_0, label_1, label_2]) == list(range(3))):
            # if (bestScore < totalScore):
            #     bestScore = totalScore
            results.append({ m[label_0]: tm[0], m[label_1]: tm[1], m[label_2]: tm[2] , 'score': totalScore})

    results = sorted(results, key=lambda x: x['score'], reverse=True)

    return results[:3]


def segment_api_v1_1(text):

    preAddr = preprocessPuncText(text)

    addrTermTuples = findPoses(term_regex['address'].finditer(preAddr))
    companyTermTuples = findPoses(term_regex['company'].finditer(preAddr))
    titleTermTuples = findPoses(term_regex['name'].finditer(preAddr))
    phoneTermTuples = findPoses(term_regex['phone'].finditer(preAddr))
    faxTermTuples = findPoses(term_regex['fax'].finditer(preAddr))
    emailTermTuples = findPoses(term_regex['email'].finditer(preAddr))
    urlTermTuples = findPoses(term_regex['url'].finditer(preAddr))

    # emailTuples = findPoses(email_regex.finditer(text))
    # urlTuples = findPoses(url_regex.finditer(text))

    preAddr = removeKeyword(preAddr, addrTermTuples)
    preAddr = removeKeyword(preAddr, companyTermTuples)
    preAddr = removeKeyword(preAddr, titleTermTuples)
    preAddr = removeKeyword(preAddr, phoneTermTuples)
    preAddr = removeKeyword(preAddr, faxTermTuples)
    preAddr = removeKeyword(preAddr, emailTermTuples)
    preAddr = removeKeyword(preAddr, urlTermTuples)

    for i, c in enumerate(preAddr):
        if (c == ' '):
            if (text[i] in string.punctuation+string.whitespace):
                preAddr = preAddr[:i] + text[i] + preAddr[i+1:]

    labels = ['name', 'address', 'phone', 'email', 'url']
    otherLabel = 'unknown'

    ic = -1
    _ = checkCandidate(preAddr, labels, otherLabel)

    candidates = {preAddr: (0, _[1], _[0])}
    candidateList = [preAddr]

    def addText(text, pos):
        rs = checkCandidate(text, labels, otherLabel)
        return (pos, rs[1], rs[0])

    while (ic + 1 < len(candidateList)):
        ic += 1
        segs = combinationTerm(candidateList[ic])
        for iseg in segs:
            if (iseg[0] not in candidates):
                candidateList.append(iseg[0])
                candidates[iseg[0]] = addText(iseg[0], candidates[candidateList[ic]][0])
            if (iseg[1] not in candidates):
                candidateList.append(iseg[1])
                candidates[iseg[1]] = addText(iseg[1], candidates[candidateList[ic]][0] + len(iseg[0]))

    skiplist = [[] for i in range(len(text))]
    for ttext, tvalue in candidates.items():
        if (tvalue[2] != otherLabel):
            skiplist[tvalue[0]].append([ttext, tvalue[1], tvalue[2]])


    _results = []
    def findResults(text, n, i, l, lt):
        if (i >= len(text)):
            _results.append({'solution': copy.deepcopy(l), 'score': sum([_[1] for _ in l])})
        elif (n < 7):
            for tt in skiplist[i]:
                if (tt[2] not in lt):
                    if (tt[1] >= 0.01):
                        lt.append(tt[2])
                        l.append(tt)
                        findResults(text, n+1, i+len(tt[0]), l, lt)
                        del lt[-1]
                        del l[-1]

    findResults(text, 1, 0, [], [])

    _results = sorted(_results, key=lambda x: x['score'], reverse=True)

    results = []
    for _ in _results[:3]:
        tp = {ilabel: '' for ilabel in labels}
        tp['score'] = _['score']
        for i in _['solution']:
            tp[i[2]] = i[0]
        results.append(tp)

    return results