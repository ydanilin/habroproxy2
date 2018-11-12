""" server's backbone """
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlunparse
import requests
from .interceptors import intercept
from .utils import get_time


def strip_headers_to_client(headers):
    """
        Removes the following headers from Response class (MUTATES):
        'Content-Encoding': Python Requests library provides content already ungzipped
        'Transfer-Encoding': Response will not be understood by client if 'chunked' is set
    """
    if headers.get('Content-Encoding'):
        headers.pop('Content-Encoding')
    if headers.get('Transfer-Encoding'):
        headers.pop('Transfer-Encoding')


class Handler(BaseHTTPRequestHandler):
    """ client requests handler """
    # pylint: disable=invalid-name
    def do_GET(self):
        """ handler for GET requests """
        self.protocol_version = self.request_version
        # pylint: disable=attribute-defined-outside-init
        self.close_connection = False if self.headers.get('Connection') == 'keep-alive' else True

        print(f'Got request for {self.requestline} at {get_time()}')
        url, headers = self.server.modify_request_to_remote(self.path, self.headers)
        resp = requests.get(url, headers=headers)
        strip_headers_to_client(resp.headers)
        content_type = resp.headers.get('Content-Type')
        if content_type and 'text/html' in content_type:
            content_for_client = intercept(resp)
            content_for_client = content_for_client.replace(
                b'https://habr.com', b'http://127.0.0.1:8080'
            )
        else:
            content_for_client = resp.content

        self.send_response(resp.status_code)
        list(map(lambda x: self.send_header(x[0], x[1]), dict(resp.headers).items()))
        if not resp.headers.get('Content-Length'):
            self.send_header('Content-Length', len(content_for_client))
        self.end_headers()
        try:
            amt = self.wfile.write(content_for_client)
            print((f'Response {resp.status_code}, written {amt} bytes'
                   f'for {self.requestline} at {get_time()}\n'))
        except BrokenPipeError:
            print(f'Connection for {self.requestline} suddenly closed by client')


class HabroServer(ThreadingMixIn, HTTPServer):
    """ Just to inherit from ThreadingMixIn """
    def __init__(self, address, request_handler):
        super(HabroServer, self).__init__(address, request_handler)
        self.scheme = 'https'
        self.host = 'habr.com'

    def modify_request_to_remote(self, path, headers):
        """
            path = request handler.path
            headers = request handler.headers
            Returns url and headers dict suitable for remote
        """
        # six items in iterable for urlunparse() are: scheme://netloc/path;parameters?query#fragment
        url = urlunparse([self.scheme, self.host, path, '', '', ''])
        host_hd = headers.get('Host')
        if host_hd and ('127.0' in host_hd or 'localhost' in host_hd):
            headers.replace_header('Host', self.host)
        ref_hd = headers.get('Referer')
        if ref_hd and ('127.0' in ref_hd or 'localhost' in ref_hd):
            headers.replace_header('Referer', url)
        orig_hd = headers.get('Origin')
        if orig_hd and ('127.0' in orig_hd or 'localhost' in orig_hd):
            headers.replace_header('Origin', urlunparse([self.scheme, self.host, '', '', '', '']))
        return url, dict(headers.items())


def get_server(port):
    """ serve_forever() should be called outside, by runners """
    # server = HTTPServer(('', port), Handler)
    server = HabroServer(('', port), Handler)
    return server
