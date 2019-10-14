# -*- coding: utf-8 -*-
"""
csrweb.wsgi
~~~~~~~~~~

wsgi script.

"""

import sys


# Ensure the main project directory is on the path
sys.path.insert(0, '/var/www/apps/csrweb')

from csrweb import app as application
