import numpy as np

from address_segmentation.feature import getFeature
from config import models, email_regex, url_regex


def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def clasify(clfs, text):
    probName = calANNProba(clfs['name'], text, 'name')

    probAddress = calANNProba(clfs['address'], text, 'address')

    probPhone = calANNProba(clfs['phone'], text, 'phone')

    proba = [
        probName[0] * probAddress[1] * probPhone[1],
        probName[1] * probAddress[0] * probPhone[1],
        probName[1] * probAddress[1] * probPhone[0],
        probName[1] * probAddress[1] * probPhone[1]
    ]

    _ = np.asarray(proba) / np.sum(proba)
    return max(range(len(_)), key=_.__getitem__), _

def checkCandidate(text, lc, other):
    score = {}
    for key in lc:
        score[key] = calScore(text, key)
    mxvalue = max(score.values())
    if (mxvalue > 0.5):
        return (list(score.keys())[list(score.values()).index(mxvalue)], mxvalue)
    return (other, 0)

def fixMisunderstood(text):
    text = text.replace('o', '0')
    text = text.replace('d', '0')
    text = text.replace('q', '0')
    return text

def calScore(text, ttype):
    if (ttype in ['name', 'address', 'phone']):
        if (ttype == 'phone'):
            text = fixMisunderstood(text)
        return calANNProba(models[ttype], text, ttype)[0]
    elif (ttype == 'fax'):
        text = fixMisunderstood(text)
        return calANNProba(models['phone'], text, 'phone')[0]
    elif (ttype == 'email'):
        return 1 if (len(email_regex.findall(text)) > 0) else 0
    elif (ttype == 'url'):
        return 1 if (len(url_regex.findall(text)) > 0) else 0
    return 0

def calANNProba(clf, text, ttype):
    ft = getFeature([text], ttype)
    layer0, layer1 = clf['layer_0'], clf['layer_1']
    a = sigmoid(ft[0].dot(layer0['w']) + layer0['b'])
    return softmax(a.dot(layer1['w']) + layer1['b'])