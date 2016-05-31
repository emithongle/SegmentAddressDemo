import tornado.ioloop
import tornado.web
from address_segmentation.segment_api import segment_api_v1_0, segment_api_v1_1
import json
from logs.loger import saveLog

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        text = self.get_argument('addText', False)

        uploadTime = self.get_argument('uploadTime', False)
        ocrTime = self.get_argument('ocrTime', False)
        segmentTime = self.get_argument('segmentTime', False)
        ocrText = self.get_argument('ocrText', False)
        imageURL = self.get_argument('imageURL', False)

        if (text):
            self.write(json.dumps(segment_api_v1_1(text), ensure_ascii=False))
        elif (uploadTime and ocrTime and segmentTime and ocrText and imageURL):
            log = {'uploadTime': uploadTime, 'ocrTime': ocrTime,
                         'segmentTime': segmentTime, 'ocrText': ocrText, 'imageURL': imageURL}
            if (saveLog(log)):
                self.write('Okay!')



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()