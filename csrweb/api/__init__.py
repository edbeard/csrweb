# -*- coding: utf-8 -*-
"""
csrweb.api
~~~~~~~~~~

REST API for ChemSchematicResolver.

:copyright: Copyright 2019 by Ed Beard
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from flask import Blueprint, request
from flask_restplus import Api


log = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)


class CsrApi(Api):
    """Customized subclass of Flask-Restplus/Flask-Restful Api."""

    def make_response(self, data, *args, **kwargs):
        """Wrapper around make_response that uses 'format' querystring parameter as well as 'Accept' header."""
        # If querystring format, use that media type
        mediatypes = {
            'json': 'application/json',
            'xml': 'application/xml'
        }
        mediatype = mediatypes.get(request.args.get('format'))
        if mediatype in self.representations:
            resp = self.representations[mediatype](data, *args, **kwargs)
            resp.headers['Content-Type'] = mediatype
            return resp
        # If text/html (i.e. browser default) make sure we return JSON not XML
        if 'text/html' in request.accept_mimetypes:
            resp = self.representations['application/json'](data, *args, **kwargs)
            resp.headers['Content-Type'] = 'application/json'
            return resp
        # Otherwise do default Flask-RestPlus/Flask-Restful content-negotiation via Accept Header
        return super(CsrApi, self).make_response(data, *args, **kwargs)


api = CsrApi(
    api_bp,
    version='1.0',
    title='ChemSchematicResolver REST API',
    description='A web service for programmatically uploading documents to be processed using ChemSchematicResolver on our servers.\n\n All endpoints are at constructed by appending to http://chemschematicresolver.org/api',
)


from . import resources, representations



