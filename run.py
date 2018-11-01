#!/usr/bin/env python
""" may serve as bin runner in linux """
from src import get_server


if __name__ == "__main__":
    get_server(8080).serve_forever()
