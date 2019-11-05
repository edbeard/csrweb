# -*- coding: utf-8 -*-
"""
csrweb.api.representations
~~~~~~~~~~~~~~~~~~~~~~~~~~

API response formats.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
from io import BytesIO
import logging

import dicttoxml
import pandas as pd
from flask import make_response, abort
import json

from . import api


log = logging.getLogger(__name__)


@api.representation('application/json')
def output_json(data, code, headers):

    all_results = []
    print('The data is: %s' % data)
    print('The data result is : %s' % data['result'])
    for result in data['result']:
        print(result)
        labels = [{'value': label['value']} for label in result['labels']]
        all_results.append({'labels': labels, 'smiles': result['smiles'], 'name': result['name']})

    resp = make_response(json.dumps(data, indent=4, sort_keys=True), code)
    resp.headers.extend(headers)
    return resp


@api.representation('application/xml')
def output_xml(data, code, headers):

    # all_results = []
    # for result in data['result']:
    #     labels = [{'label': label}]
    #
    #     # labels = [{'label': label.value} for label in result.labels]
    #     # all_results.append({'labels': labels, 'smile': result.smiles})
    #
    # data['result'] = all_results
    # print('The result is %s ' % data['result'])

    resp = make_response(dicttoxml.dicttoxml(data, attr_type=False, custom_root='job'), code)
    resp.headers.extend(headers)
    return resp
