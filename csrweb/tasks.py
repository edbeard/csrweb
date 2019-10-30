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

from . import app, db, make_celery
from .models import CsrJob, ChemDict, CsrLabel, CsrRecord

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
        print('is there any output hre?')
        # records = extract_image(fname)
        import osra_rgroup
        var = osra_rgroup.read_diagram('osra_temp.gif')
        print('Was anything extracted?: %s' % var)
        records = var
    except:
        print('An exception occurred while running extract_image.')
        return 'Exception in get_result function'
    print('records are : %s' % records)

    return [(['1a'], 'C1CCCCC1')]


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


def add_structures(result):
    # Run OPSIN
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        for record in result['records']:
            for name in record.get('names', []):
                tf.write(('%s\n' % name).encode('utf-8'))
    subprocess.call([app.config['OPSIN_PATH'], '--allowRadicals', '--wildcardRadicals', '--allowAcidsWithoutAcid', '--allowUninterpretableStereo', tf.name, '%s.result' % tf.name])
    with open('%s.result' % tf.name) as res:
        structures = [line.strip() for line in res]
        i = 0
        for record in result['records']:
            for name in record.get('names', []):
                if 'smiles' not in record and structures[i]:
                    log.debug('Resolved with OPSIN: %s = %s', name, structures[i])
                    record['smiles'] = structures[i]
                i += 1
    os.remove(tf.name)
    os.remove('%s.result' % tf.name)
    # For failures, use NCI CIR (with local cache of results)
    for record in result['records']:
        for name in record.get('names', []):
            if 'smiles' not in record:
                local_entry = ChemDict.query.filter_by(name=name).first()
                if local_entry:
                    log.debug('Resolved with local dict: %s = %s', name, local_entry.smiles)
                    if local_entry.smiles:
                        record['smiles'] = local_entry.smiles
                else:
                    smiles = cirpy.resolve(chem_normalize(name).encode('utf-8'), 'smiles')
                    log.debug('Resolved with CIR: %s = %s', name, smiles)
                    db.session.add(ChemDict(name=name, smiles=smiles))
                    if smiles:
                        record['smiles'] = smiles
    return result


@celery.task()
def run_csr(job_id):

    print('Entering the run_csr task...')
    csr_job = CsrJob.query.get(job_id)
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csr_job.file)
    print('Path to input image is %s' % input_filepath)
    results = get_result(input_filepath)
    print('Results are %s' % results)
    for result in results:
        labels, smiles = result[0], result[1]
        csr_record = CsrRecord(smiles=smiles, csr_job=csr_job)
        for label in labels:
            csr_label = CsrLabel(value=label, csr_record=csr_record)
            db.session.add(csr_label)
        db.session.add(csr_record)
    # print('The ouptut result is :' % ide_job.result)
    db.session.commit()

