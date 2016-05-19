import tornado.ioloop
import tornado.web
from address_segmentation.segment_api import segment_api
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        text = self.get_argument('addText', True)
        self.write(json.dumps(segment_api(text), ensure_ascii=False))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()