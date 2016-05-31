__author__ = 'ThongLe'

from time import strftime, localtime
from address_segmentation.segment_api import segment_api_v1_1
from config import folders, files
from db.store import loadXLSX, saveXLSX

def saveLog(log, filePath=folders['log'] + '/' + files['log']['log']):
    try:
        data = loadXLSX(filePath)

        data.append([
            strftime("%a, %d %b %Y %H:%M:%S", localtime()),
            log['uploadTime'],
            log['ocrTime'],
            log['segmentTime'],
            log['imageURL'],
            log['ocrText'],
            str(segment_api_v1_1(log['ocrText'])),
        ])

        saveXLSX({'log-result': data}, filePath)

    except ValueError:
        return False
    return True

# uploadTime=1&
# ocrTime=2&
# segmentTime=3&
# imageID=imageid&
# ocrText=xyz

