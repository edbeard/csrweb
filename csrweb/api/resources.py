# -*- coding: utf-8 -*-
"""
csrweb.api.resources
~~~~~~~~~~~~~~~~~~~~

API resources.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import os
import uuid

import six
from flask import current_app, make_response
from flask_restplus import Resource, abort, fields
import werkzeug

from .. import db
from ..models import CsrJob
from ..tasks import run_csr
from . import api


log = logging.getLogger(__name__)


jobs = api.namespace('Jobs', path='/job', description='Submit jobs and retrieve results')


csrjob_schema = api.model('CsrJob', {
    'job_id': fields.String(required=True, description='Unique job ID'),
    'created_at': fields.DateTime(required=True, description='Job creation timestamp'),
    'status': fields.String(required=True, description='Current job status'),
})

labels = dict()
labels['value'] = fields.String

result = dict()
result['smiles'] = fields.String
result['name'] = fields.String
result['labels'] = fields.Nested(labels)

csrjob_schema['result'] = fields.Nested(result)

submit_parser = api.parser()
submit_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, required=True, help='The input file.', location='files')

result_parser = api.parser()
result_parser.add_argument('output', help='Response format', location='query', choices=['json', 'xml'])


@jobs.route('/')
# @api.doc(responses={400: 'Disallowed file type'})
class CsrJobSubmitResource(Resource):
    """Submit a new ChemSchematicResolver job and get the job ID."""

    @api.doc(description='Submit a new ChemSchematicResolver job.', parser=submit_parser)
    @api.marshal_with(csrjob_schema, code=201)
    def post(self):
        """Submit a new job."""
        args = submit_parser.parse_args()
        file = args['file']
        job_id = six.text_type(uuid.uuid4())
        if '.' not in file.filename:
            abort(400, b'No file extension!')
        extension = file.filename.rsplit('.', 1)[1]
        if extension not in current_app.config['ALLOWED_EXTENSIONS']:
            abort(400, b'Disallowed file extension!')
        filename = '%s.%s' % (job_id, extension)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        csr_job = CsrJob(file=filename, job_id=job_id)
        db.session.add(csr_job)
        db.session.commit()
        run_csr.apply_async([csr_job.id], task_id=job_id)
        return csr_job, 201


@jobs.route('/<string:job_id>')
@api.doc(params={'job_id': 'The job ID'})  # responses={404: 'Job not found'},
class CsrJobResource(Resource):
    """View the status and results of a specific ChemSchematicResolver job."""

    @api.doc(description='View the status and results of a specific ChemSchematicResolver job.', parser=result_parser)
    @api.marshal_with(csrjob_schema)
    def get(self, job_id):
        """Get the results of a job."""
        return CsrJob.query.filter_by(job_id=job_id).first_or_404()
