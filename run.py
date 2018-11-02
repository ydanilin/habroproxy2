#!/usr/bin/env python
""" may serve as bin runner in linux """
import sys
from src import get_server


if __name__ == "__main__":
    PORT = 8080
    print(f'Habroproxy server started at port {PORT}')
    try:
        get_server(PORT).serve_forever()
    except KeyboardInterrupt:
        sys.exit()
