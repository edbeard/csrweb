# -*- coding: utf-8 -*-
"""
csrweb.models
~~~~~~~~~~~~~

Data models.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from . import db


log = logging.getLogger(__name__)

Base = declarative_base()


class CsrJob(db.Model):
    """An ChemSchematicResolver job."""

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    file = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    result = db.relationship('CsrRecord', backref='csr_job', lazy=True)

    @property
    def status(self):
        from .tasks import celery
        return celery.AsyncResult(self.job_id).status


class CsrRecord(db.Model):
    """ Output from a ChemSchemaitcResolver job"""

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('csr_job.id'), nullable=False)
    smiles = db.Column(db.String, nullable=True)
    labels = db.relationship('CsrLabel', backref='csr_record', lazy=True)


class CsrLabel(db.Model):
    """ Holds a string representing a label"""

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('csr_record.id'), nullable=False)
    value = db.Column(db.String, nullable=True)


class ChemDict(db.Model):
    """A chemical name with associated SMILES."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    smiles = db.Column(db.String, nullable=True)


class User(db.Model):
    """Registered user."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    affiliation = db.Column(db.String, nullable=True)
