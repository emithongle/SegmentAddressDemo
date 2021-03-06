__author__ = 'ThongLe'

from time import strftime, localtime
from address_segmentation.segment_api import segment_api_v1_1
from config import folders, files
from db.store import loadXLSX, saveXLSX
from datetime import datetime 

def saveLog(log, filePath=folders['log'] + '/' + files['log']['log']):
    try:
        data = loadXLSX(filePath)

        startTime = datetime.now()
        apiResults = str(segment_api_v1_1(log['ocrText']))
        endTime = datetime.now()

        realSegmentTime = (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000

        data.append([
            strftime("%a, %d %b %Y %H:%M:%S", localtime()),
            log['uploadTime'],
            '',
            log['segmentTime'],
            realSegmentTime,
            log['imageURL'],
            log['ocrText'],
            log['idResult'],
            apiResults,
            log['name'],
            log['address'],
            log['phone']
        ])

        saveXLSX({'log-result': data}, filePath)

    except ValueError:
        return False
    return True

def saveWebLog(log, filePath=folders['log'] + '/' + files['log']['wlog']):
    # Time	UploadTime	OCRTime	SegmentTime	ImageURL	OCRResult	idResult	SegmentResult	ChosenName	ChosenAddress	ChosenPhone

    try:
        data = loadXLSX(filePath)

        startTime = datetime.now()
        apiResults = str(segment_api_v1_1(log['ocrText']))
        endTime = datetime.now()

        realSegmentTime = (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000

        data.append([
            strftime("%a, %d %b %Y %H:%M:%S", localtime()),
            '',
            '',
            '',
            realSegmentTime,
            '',
            log['ocrText'],
            log['idResult'],
            apiResults,
            '',
            '',
            ''
        ])

        saveXLSX({'log-result': data}, filePath)

    except ValueError:
        return False
    return True

