import tornado.escape
import tornado.ioloop
import tornado.web
import jwt
import datetime
from auth import jwtauth
SECRET = 'my_secret_key'


@jwtauth
class HelloHandler(tornado.web.RequestHandler):

    def get(self):
        # Contains user found in previous auth
        if self.request.headers.get('auth'):
            self.write('ok')


class AuthHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.encoded = jwt.encode({
            'some': 'payload',
            'a': {2: True},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=22)},
            SECRET,
            algorithm='HS256'
        )

    def get(self):
        response = {'token': self.encoded}
        self.write(response)


application = tornado.web.Application([
    (r"/auth", AuthHandler),
    (r"/", HelloHandler)
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
