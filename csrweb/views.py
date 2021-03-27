# -*- coding: utf-8 -*-
"""
csrweb.views
~~~~~~~~~~~~

Main website views.

:copyright: Copyright 2019 by Ed Beard.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import logging
import os
import uuid
import gc

from flask import render_template, request, url_for, redirect, abort, flash, send_from_directory, Response
from flask_basicauth import BasicAuth

import hoedown
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import six

from . import app, tasks, db
from .forms import RegisterForm
from .models import CsrJob, User
from .tasks import celery


log = logging.getLogger(__name__)

basic_auth = BasicAuth(app)


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/about_new')
def about_new():
    return render_template('about.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    registered = request.args.get('registered', False)
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=request.form['email'], name=request.form['name'], affiliation=request.form['affiliation'])
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('download', registered=True))
    return render_template('download.html', form=form, registered=registered)


@app.route('/evaluation')
def evaluation():
    return redirect(url_for('download'))


@app.route('/citing')
def citing():
    return render_template('citing.html')


@app.route('/docs')
def docs_index():
    return redirect(url_for('docs', docfile='intro'))


@app.route('/docs/<docfile>')
def docs(docfile):

    toc = [
        'intro', 'install', 'gettingstarted', 'largescale', 'wildcards', 'contributing'
    ]

    titles = {
        'intro': 'Introduction',
        'install': 'Installation',
        'gettingstarted': 'Getting Started',
        'largescale': 'Large Scale Extraction',
        'wildcards': 'Wildcard Results',
        'contributing': 'Contributing'
    }

    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))
    source_path = os.path.abspath(os.path.join(docs_dir, '%s.md' % docfile))
    # Check just in case somehow a path outside docs dir is constructed
    if not source_path.startswith(docs_dir):
        abort(404)
    try:
        with open(source_path) as mf:
            content = hoedown.html(mf.read())
            prev_i = toc.index(docfile) - 1
            prev = toc[prev_i] if prev_i >= 0 else None
            next_i = toc.index(docfile) + 1
            next = toc[next_i] if next_i < len(toc) else None
            return render_template('docs.html', current=docfile, prev=prev, next=next, content=content, toc=toc, titles=titles)
    except IOError:
        abort(404)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():

    if request.method == 'POST':
        log.info(request.form)
        job_id = six.text_type(uuid.uuid4())
        print('File has been submitted to demo with job_id %s' % job_id)
        if 'input-file' in request.files:
            file = request.files['input-file']
            if '.' not in file.filename:
                abort(400, 'No file extension!')
            extension = file.filename.rsplit('.', 1)[1].lower()
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                abort(400, 'Disallowed file extension!')
            filename = '%s.%s' % (job_id, extension)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            csr_job = CsrJob(file=filename, job_id=job_id)
            db.session.add(csr_job)
            db.session.commit()
            log.debug('Running the task queue.')
            try:
                async_result = tasks.run_csr.apply_async([csr_job.id], task_id=job_id)
                print('Async result is...')
                print(async_result)
            except Exception as e:
                print('Exception thrown in demo')
                print(e)
            print('REached end of demo POST')
            return redirect(url_for('results', result_id=async_result.id))

        # elif 'input-url' in request.form:
        #     url = request.form['input-url']
        #     r = requests.get(url)
        #     extension = None
        #     if 'Content-Type' in r.headers:
        #         t = r.headers['Content-Type']
        #         if 'text/html' in t:
        #             extension = 'html'
        #         elif '/xml' in t:
        #             extension = 'xml'
        #         elif '/pdf' in t:
        #             extension = 'pdf'
        #     elif 'Content-Disposition' in r.headers:
        #         d = r.headers['Content-Disposition']
        #         m = re.search('filename=(.+)\.([^\.]+)', d)
        #         if m:
        #             extension = m.group(2).lower()
        #     else:
        #         m = re.search('\.([a-z]+)$', url)
        #         if m:
        #             extension = m.group(1).lower()
        #     if not extension:
        #         abort(400, 'Could not determine file type!')
        #     if extension not in app.config['ALLOWED_EXTENSIONS']:
        #         abort(400, 'Disallowed file extension!')
        #     filename = '%s.%s' % (job_id, extension)
        #     with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
        #         f.write(r.content)
        #     cde_job = CdeJob(file=filename, job_id=job_id)
        #     db.session.add(cde_job)
        #     db.session.commit()
        #     async_result = tasks.run_cde.apply_async([cde_job.id], task_id=job_id)
        #     return redirect(url_for('results', result_id=async_result.id))
        # elif 'input-text' in request.form:
        #     # save text file from request.form
        #     input_text = request.form['input-text']
        #     filename = '%s.txt' % job_id
        #     with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w') as f:
        #         f.write(input_text.encode('utf-8'))
        #     cde_job = CdeJob(file=filename, job_id=job_id)
        #     db.session.add(cde_job)
        #     db.session.commit()
        #     async_result = tasks.run_cde.apply_async([cde_job.id], task_id=job_id)
        #     return redirect(url_for('results', result_id=async_result.id))

        # Something must have been wrong...
        gc.collect()

    else:
        gc.collect()
        return render_template('demo.html')


@app.route('/results/<result_id>')
def results(result_id):
    task = celery.AsyncResult(result_id)
    job = CsrJob.query.filter_by(job_id=result_id).first_or_404()
    print('job is: %s' % job.job_id)

    prop_keys = {'nmr_spectra', 'ir_spectra', 'uvvis_spectra', 'melting_points', 'electrochemical_potentials', 'quantum_yields', 'fluorescence_lifetimes'}

    has_result = False
    mem_error = False
    none_extracted = False

    if job.result:
        has_result = True
        print('We now have the result...')
        print(job)

        # Detecting case where no results were extracted...
        if len(job.result) == 1 and job.result[0].smiles == 'NA':
            none_extracted = True
        elif len(job.result) == 1 and job.result[0].smiles == 'MEM_ERR':
            mem_error = True

        for result in job.result:
            for label in result.labels:
                print('The label is:')
                print(label.value)
            print('The name is: %s' % result.name)

        # for result in job.result:
        #     for record in result.get('records', []):
        #         has_result = True
        #         if any(k in prop_keys for k in record.keys()):
        #             has_important = True
        #         elif 'labels' in record or 'smiles' in record:
        #             has_other = True
        #         else:
        #             has_important = True


    print('Has result is: %s' % has_result)
    print('job result is %s' % job.result)

    return render_template(
        'results.html',
        task=task,
        job=job,
        has_result=has_result,
        none_extracted=none_extracted,
        mem_error=mem_error
    )


@app.route('/depict/<path:smiles>')
def depict(smiles):
    """Depict structure"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return send_from_directory('static/img', as_attachment=True, filename='failed_resolution.svg')
    print('Molecule loaded: %s' % mol)
    mc = copy.deepcopy(mol)
    print('molecule loaded')
    try:
        print('trying to draw molecule')
        img = Draw.MolToImage(mc, size=(180, 180), kekulize=True, highlightAtoms=[])
        print('molecule drawn')
    except Exception as e:  # <- can happen on a kekulization failure
        print('Error:')
        mc = copy.deepcopy(mol)
        # try:
        print('value error when trying with kekulization')
        img = Draw.MolToImage(mc, size=(180, 180), kekulize=False, highlightAtoms=[])
        print('molcule drawn with kekulization = False')
        # except ValueError:
        #     print('value error when trying without kekulization')
        #     print('Could not resolve SMILES to structure: %s' % smiles)
        #     return send_from_directory('static/img', as_attachment=True, filename='failed_resolution.svg')
    img_io = six.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return Response(response=img_io.getvalue(), status=200, mimetype='image/png')


@app.route('/mol/<path:smiles>')
def mol(smiles):
    """Return MOL for SMILES."""

    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return render_template('unresolved_mol.html', smiles=smiles)
    AllChem.Compute2DCoords(mol)
    mb = Chem.MolToMolBlock(mol)
    return Response(response=mb, status=200, mimetype='chemical/x-mdl-molfile', headers={'Content-Disposition': 'attachment;filename=structure.mol'})


@app.route('/imgs/<job_id>/<type>', methods=['GET','POST'])
def send_image(job_id, type):
    job = CsrJob.query.filter_by(job_id=job_id).first_or_404()
    fail_path = 'static/img'

    if 'path' in job.result.keys():
        full_path = job.result['path'][type]
    else:
        full_path = None
        return None

    print('Image full path is... %s' % full_path)

    # Check that file was produced
    if os.path.isfile(full_path) and full_path is not None:
        dir_path = os.path.join(app.config['OUTPUT_FOLDER'], full_path.split('/')[-2])
        img_file = full_path.split('/')[-1]
        return send_from_directory(dir_path, as_attachment=True, filename=img_file)
    elif type == 'rdf':
        return send_from_directory(fail_path, as_attachment=True, filename='minRDF_fail.png')
    elif type == 'hist':
        return send_from_directory(fail_path, as_attachment=True, filename='hist_fail.png')



