# -*- coding: utf-8 -*-

import os
import pickle
from server import app

if __name__ == '__main__':
    print('Flask starting server...')
    app.run(
        host='localhost',
        port=5000,
        debug=True
    )
