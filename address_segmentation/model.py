from address_segmentation.feature import getFeature
import numpy as np
from address_segmentation.config import models, email_regex, url_regex

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def clasify(clfs, text):
    # probName = _f(clfs['name'], text, 'name')[0]
    probName = calANNProba(clfs['name'], text, 'name')

    # probAddress = _f(clfs['address'], text, 'address')[0]
    probAddress = calANNProba(clfs['address'], text, 'address')

    # probPhone = _f(clfs['phone'], text, 'phone')[0]
    probPhone = calANNProba(clfs['phone'], text, 'phone')

    proba = [
        probName[0] * probAddress[1] * probPhone[1],
        probName[1] * probAddress[0] * probPhone[1],
        probName[1] * probAddress[1] * probPhone[0],
        probName[1] * probAddress[1] * probPhone[1]
    ]

    # _ = np.exp(proba) / np.sum(np.exp(proba))
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

def calScore(text, ttype):
    if (ttype in ['name', 'address', 'phone']):
        return calANNProba(models[ttype], text, ttype)[0]
    elif (ttype == 'fax'):
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