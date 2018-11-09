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
        # six items in iterable for urlunparse(): scheme://netloc/path;parameters?query#fragment
        url = urlunparse([SCHEME, HOST, self.path, '', '', ''])
        host_hd = self.headers.get('Host')
        if host_hd and ('127.0' in host_hd or 'localhost' in host_hd):
            self.headers.replace_header('Host', HOST)
        ref_hd = self.headers.get('Referer')
        if ref_hd and ('127.0' in ref_hd or 'localhost' in ref_hd):
            self.headers.replace_header('Referer', url)
        orig_hd = self.headers.get('Origin')
        if orig_hd and ('127.0' in orig_hd or 'localhost' in orig_hd):
            self.headers.replace_header('Origin', urlunparse([SCHEME, HOST, '', '', '', '']))

        resp = requests.get(url, headers=dict(self.headers.items()))
        # resp = requests.get(url)
        if resp.headers.get('Content-Encoding'):
            resp.headers.pop('Content-Encoding')
        if resp.headers.get('Transfer-Encoding'):
            resp.headers.pop('Transfer-Encoding')
        content_type = resp.headers.get('Content-Type')
        if content_type and 'text/html' in content_type:
            content_for_client = intercept(resp)
        else:
            content_for_client = resp.content
        self.protocol_version = self.request_version
        if self.headers.get('Connection') == 'keep-alive':
            self.close_connection = False
        else:
            self.close_connection = True
        self.send_response(200)
        list(map(lambda x: self.send_header(x[0], x[1]), dict(resp.headers).items()))
        self.send_header('Content-Length', len(content_for_client))
        self.end_headers()
        amt = self.wfile.write(content_for_client)
        print('Written bytes: ', amt)
        if self.close_connection:
            print('connection closed')
            self.connection.close()


def get_server(port):
    """ serve_forever() should be called outside, by runners """
    server = HTTPServer(('', port), Handler)
    return server
