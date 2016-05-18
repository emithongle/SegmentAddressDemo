from address_segmentation.feature import getFeature
import numpy as np

def clasify(clfs, text):
    def _f(clf, text, ttype):
        return clf.predict_proba(getFeature([text], ttype))

    probName = _f(clfs['name'], text, 'name')[0]
    probAddress = _f(clfs['address'], text, 'address')[0]
    probPhone = _f(clfs['phone'], text, 'phone')[0]

    proba = [
        probName[0] * probAddress[1] * probPhone[1],
        probName[1] * probAddress[0] * probPhone[1],
        probName[1] * probAddress[1] * probPhone[0],
        probName[1] * probAddress[1] * probPhone[1]
    ]

    # _ = np.exp(proba) / np.sum(np.exp(proba))
    _ = np.asarray(proba) / np.sum(proba)
    return max(range(len(_)), key=_.__getitem__), _