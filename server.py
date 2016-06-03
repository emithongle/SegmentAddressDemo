import tornado.ioloop
import tornado.web
from address_segmentation.segment_api import segment_api_v1_0, segment_api_v1_1
import json
from logs.loger import saveLog, saveWebLog
from config import rm_preprocessed_punctuation

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Main.GET')

    def post(self):
        self.write('Main.POST')

class MainServiceHandler(MainHandler):
    def get(self):
        text = self.get_argument('addText', False)

        uploadTime = self.get_argument('uploadTime', False)
        # ocrTime = self.get_argument('ocrTime', False)
        segmentTime = self.get_argument('segmentTime', False)
        ocrText = self.get_argument('ocrText', False)
        imageURL = self.get_argument('imageURL', False)

        idResult = self.get_argument('idResult', False)

        name = self.get_argument('name', '')
        address = self.get_argument('address', '')
        phone = self.get_argument('phone', '')

        if (text):
            self.write(json.dumps(segment_api_v1_1(text), ensure_ascii=False))
        elif (uploadTime and segmentTime and ocrText and imageURL):
            log = {'uploadTime': uploadTime, 
                         'segmentTime': segmentTime, 'ocrText': ocrText, 'imageURL': imageURL, 'idResult': idResult,
                         'name': name, 'address': address, 'phone': phone}
            if (saveLog(log)):
                self.write('Okay!')

class ORCText(object):
    orcText = ''
    save = False

class MainWebHandler(MainHandler):

    def post(self):
        idCorrect = self.get_argument('correct', '')

        f = lambda x, y: x.strip(rm_preprocessed_punctuation) != y.strip(rm_preprocessed_punctuation)

        if (f(ORCText.orcText, 'Please input address...') and f(ORCText.orcText, '')):
            if (ORCText.save):
                saveWebLog({'ocrText': ORCText.orcText, 'idResult': idCorrect })

        ORCText.orcText = self.get_argument('orcText', None)
        if (f(ORCText.orcText, 'Please input address...') and f(ORCText.orcText, '')):
            results = segment_api_v1_1(ORCText.orcText)
            self.render('index.html', results=results, orcText=ORCText.orcText)
            if (len(results) == 0):
                saveWebLog({'ocrText': ORCText.orcText, 'idResult': '' })
                ORCText.save = False
            else:
                ORCText.save = True
        else:
            self.render('index.html', results=[], orcText='')

    def get(self):
        self.render('index.html', results=[], orcText='')


def make_app():
    return tornado.web.Application([
        (r"/", MainWebHandler),
        (r"/sv", MainServiceHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
