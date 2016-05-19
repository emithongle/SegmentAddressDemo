from address_segmentation.feature import getFeature
import numpy as np
import math

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def clasify(clfs, text):
    def _f(clf, text, ttype):
        return clf.predict_proba(getFeature([text], ttype))

    def _g(clf, text, ttype):
        ft = getFeature([text], ttype)
        layer0, layer1 = clf['layer_0'], clf['layer_1']
        a = sigmoid(ft[0].dot(layer0['w']) + layer0['b'])
        return softmax(a.dot(layer1['w']) + layer1['b'])

    # probName = _f(clfs['name'], text, 'name')[0]
    probName = _g(clfs['name'], text, 'name')

    # probAddress = _f(clfs['address'], text, 'address')[0]
    probAddress = _g(clfs['address'], text, 'address')

    # probPhone = _f(clfs['phone'], text, 'phone')[0]
    probPhone = _g(clfs['phone'], text, 'phone')

    proba = [
        probName[0] * probAddress[1] * probPhone[1],
        probName[1] * probAddress[0] * probPhone[1],
        probName[1] * probAddress[1] * probPhone[0],
        probName[1] * probAddress[1] * probPhone[1]
    ]

    # _ = np.exp(proba) / np.sum(np.exp(proba))
    _ = np.asarray(proba) / np.sum(proba)
    return max(range(len(_)), key=_.__getitem__), _