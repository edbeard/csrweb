# -*- coding: utf-8 -*-
"""
csrweb.tasks
~~~~~~~~~~~~

Celery tasks.

:copyright: Copyright 2019 by Ed Beard.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import os
import traceback

import cirpy

from chemschematicresolver import extract_image

from . import app, db, make_celery
from .models import CsrJob, ChemDict, CsrLabel, CsrRecord


log = logging.getLogger(__name__)

celery = make_celery(app)


def get_result(fname):
    """ Obtains the results from the extracted image."""

    try:
        records = extract_image(fname, allow_wildcards=True)

    except MemoryError as e:
        log.error('Memory error:')
        log.error(e)
        memory_error = True
        return [], memory_error
    except Exception as e:
        log.warning('An exception occurred while running extract_image!...')
        log.warning(e)
        traceback.print_exc()
        records = []
    memory_error = False
    return records, memory_error


def add_name(result):
    # Run NCI CIR to get chemical names
    print('Have entered the add_name function')
    if result.smiles:
        local_entry = ChemDict.query.filter_by(smiles=result.smiles).first()
        print('Local entry: %s' % local_entry)
        if local_entry:
            log.debug('Resolved with local dict: %s = %s', result.smiles, local_entry.name)
            result.name = local_entry.name
        else:
            try:
                name = cirpy.resolve(result.smiles, 'iupac_name')
                if name:
                    log.debug('Resolved with CIR: %s = %s', result.smiles, name)
                    db.session.add(ChemDict(name=name, smiles=result.smiles))
                    result.name = name
            except Exception as e:
                log.warning('Couldn\'t resolve smiles: %s' % result.smiles)
                pass
    return result


def canonicalize_smiles(result):
    # Run NCI CIR to get chemical names

    print('SMILES before cirpy: %s' % result.smiles)
    if result.smiles:
        canon_smiles = cirpy.resolve(result.smiles, 'smiles')
        if canon_smiles:
            result.smiles = canon_smiles

    print('SMILES after cirpy: %s' % result.smiles)
    return result


@celery.task(name='csrweb.tasks.run_csr')
def run_csr(job_id):

    log.debug('Entering the run_csr task...')
    csr_job = CsrJob.query.get(job_id)
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csr_job.file)
    log.debug('Path to input image is %s' % input_filepath)
    log.debug('Detected csr_job is: %s' % csr_job.result)
    results, memory_error = get_result(input_filepath)

    if memory_error:
        csr_record = CsrRecord(smiles='MEM_ERR', name='MEM_ERR', csr_job=csr_job)
        db.session.add(csr_record)

    elif not results:
        log.debug('No results extracted.')
        csr_record = CsrRecord(smiles='NA', name='NA', csr_job=csr_job)
        db.session.add(csr_record)

    else:
        log.debug('Results extracted successfully.')
        for result in results:
            labels, smiles = result[0], result[1].replace('\n', '')
            log.debug('Smiles: %s , Labels : %s ' % (smiles, labels))
            csr_record = CsrRecord(smiles=smiles, csr_job=csr_job)
            csr_record = canonicalize_smiles(csr_record)
            csr_record = add_name(csr_record)
            db.session.add(csr_record)
            for label in labels:
                csr_label = CsrLabel(value=label, csr_record=csr_record)
                db.session.add(csr_label)
            log.debug('Name extracted: %s' % csr_record.name)
    db.session.commit()

