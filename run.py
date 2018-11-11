#!/usr/bin/env python
""" may serve as bin runner in linux """
import sys
from src import get_server


if __name__ == "__main__":
    PORT = 8080
    print(f'Habroproxy server started at port {PORT}')
    try:
        with get_server(PORT) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        sys.exit()