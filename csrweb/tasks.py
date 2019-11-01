# -*- coding: utf-8 -*-
"""
csrweb.tasks
~~~~~~~~~~~~

Celery tasks.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import os
import subprocess
import tempfile
import zipfile

import cirpy


from chemdataextractor import Document
from chemdataextractor.scrape import DocumentEntity, NlmXmlDocument, Selector
from chemdataextractor.text.normalize import chem_normalize
from natsort import natsort
import time

from chemschematicresolver import extract_image

from . import app, db, make_celery
from .models import CsrJob, ChemDict, CsrLabel, CsrRecord
import osra_rgroup
from celery.contrib import rdb


log = logging.getLogger(__name__)

celery = make_celery(app)

#
# def get_ide_output(inf, outf):
#     pass
    # extract_images(inf, outf)
    #
    # filename = inf.split('/')[-1].split('.')[0]
    # filetype = inf.split('.')[-1]
    #
    # # Zip all files together in the output folder
    # paths = [os.path.join(outf, filename, f) for f in os.listdir(os.path.join(outf, filename))]
    # with zipfile.ZipFile(os.path.join(outf, filename, filename + '.zip'), 'w') as zipme:
    #     for file in paths:
    #         zipme.write(file, arcname=os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
    #
    #
    # output = {'path':
    #               {'hist': os.path.join(outf, filename, 'hist_' + filename + '.' + filetype),
    #                'rdf': os.path.join(outf, filename,'rdf_' + filename + '.' + filetype),
    #                'scalebar': os.path.join(outf, filename,'scalebar_' + filename + '.' + filetype),
    #                'det': os.path.join(outf, filename, 'det_' + filename + '.' + filetype),
    #                'meta': os.path.join(outf, filename, filename + '.txt'),
    #                'zip': os.path.join(outf, filename, filename + '.zip')
    #                }
    #           }
    # with open(output['path']['meta'], 'r') as f:
    #     output['meta'] = f.read()
    #
    # return output


def get_result(fname):
    """ Obtains the result from """

    try:
        log.debug('is there any output here?')
        smile = osra_rgroup.read_diagram(fname)
        # rdb.set_trace()
        log.debug('Trying to output to debug after running pybind11 code...')
        log.debug(smile)
        records = [(['1a'], smile)]
        # rdb.set_trace()

    except Exception as e:
        log.debug('An exception occurred while running read_diagram.')
        records = ['fake_smile']

    return records


def get_biblio(f, fname):
    biblio = {'filename': fname}
    try:
        if fname.endswith('.html'):
            biblio.update(DocumentEntity(Selector.from_html_text(f.read())).serialize())
        elif fname.endswith('.xml') or fname.endswith('.nxml'):
            biblio.update(NlmXmlDocument(Selector.from_xml_text(f.read(), namespaces={'xlink': 'http://www.w3.org/1999/xlink'})).serialize())
    except Exception:
        pass
    return biblio


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
                log.debug('Resolved with CIR: %s = %s', result.smiles, name)
                db.session.add(ChemDict(name=name, smiles=result.smiles))
                result.name = name
            except Exception as e:
                log.warning('Couldn\'t resolve smiles: %s' % result.smiles)
                pass
    return result


@celery.task(name='csrweb.tasks.run_csr')
def run_csr(job_id):

    log.debug('Entering the run_csr task...')
    csr_job = CsrJob.query.get(job_id)
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csr_job.file)
    log.debug('Path to input image is %s' % input_filepath)
    log.debug('Detected csr_job is: %s' % csr_job.result)
    results = get_result(input_filepath)
    log.debug('Results are %s' % results)
    for result in results:
        labels, smiles = result[0], result[1].replace('\n', '')
        csr_record = CsrRecord(smiles=smiles, csr_job=csr_job)
        csr_record = add_name(csr_record)
        db.session.add(csr_record)
        for label in labels:
            csr_label = CsrLabel(value=label, csr_record=csr_record)
            db.session.add(csr_label)
        log.debug('Name extracted: %s' % csr_record.name)
    # print('The ouptut result is :' % ide_job.result)
    db.session.commit()

