""" server's backbone """
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    """ client requests handler """
    # pylint: disable=invalid-name
    def do_GET(self):
        """ handler for GET requests """
        print(self.requestline)


def get_server(port):
    """ serve_forever() should be called outside, by runners """
    server = HTTPServer(('', port), Handler)
    return server
