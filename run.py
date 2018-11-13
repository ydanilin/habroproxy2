#!/usr/bin/env python
""" may serve as bin runner in linux """
import sys
from src import get_server


if __name__ == "__main__":
    BIND_HOST = '127.18.0.1'
    # BIND_HOST = 'localhost'
    PORT = 8080
    try:
        with get_server(BIND_HOST, PORT) as server:
            print((f'Habroproxy server started at'
                   f' {server.bind_host}:{server.bind_port}'))
            server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        sys.exit()
