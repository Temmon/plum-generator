import json
import logging
import uuid
from wsgiref import simple_server

import falcon
from api import api_server

class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')

# Configure your WSGI server to load "things.app" (app is a WSGI callable)
app = falcon.API(middleware=[
#    AuthMiddleware(),
    #RequireJSON(),
])

api_server.load_api(app)

def run_dev():
    print("Starting at http://127.0.0.1:8000/")
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()

if __name__ == '__main__':
    run_dev()
