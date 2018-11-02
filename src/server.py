""" server's backbone """
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlunparse
import requests
from .interceptors import intercept


SCHEME = 'https'
HOST = 'habr.com'

class Handler(BaseHTTPRequestHandler):
    """ client requests handler """
    # pylint: disable=invalid-name
    def do_GET(self):
        """ handler for GET requests """
        self.send_response(200)
        # six items in iterable for urlunparse(): scheme://netloc/path;parameters?query#fragment
        url = urlunparse([SCHEME, HOST, self.path, '', '', ''])
        resp = requests.get(url, headers=self.headers)
        intercept(resp)
        list(map(lambda x: self.send_header(x[0], x[1]), dict(resp.headers).items()))
        self.end_headers()
        self.wfile.write(resp.content)


def get_server(port):
    """ serve_forever() should be called outside, by runners """
    server = HTTPServer(('', port), Handler)
    return server
