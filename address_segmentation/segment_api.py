from address_segmentation.segment import segmentText
from address_segmentation.model import clasify
from address_segmentation.config import models
from math import log

def segment_api(text):

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