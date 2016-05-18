import tornado.ioloop
import tornado.web
from address_segmentation.segment_api import segment_api

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, " + self.get_argument('name', True))
        text = self.get_argument('addText', True)

        self.write('<h1>' + 'Results' + '</h1>')

        self.write('<table style = "width:100%" >')
        self.write('<tr>')
        self.write('<th>#</th>')
        self.write('<th>Name</th>')
        self.write('<th>Address</th>')
        self.write('<th>Phone</th>')
        self.write('<th>Score</th>')
        self.write('</tr>')

        for i, template in enumerate(segment_api(text)):
            self.write('<tr>')
            self.write('<td>' + str(i) + '</td>')
            self.write('<td>' + template['name'] + '</td>')
            self.write('<td>' + template['address'] + '</td>')
            self.write('<td>' + template['phone'] + '</td>')
            self.write('<td>' + str(template['score']) + '</td>')
            self.write('</tr>')

        self.write('</table>')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()