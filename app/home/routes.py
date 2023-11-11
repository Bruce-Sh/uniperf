# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager, db
from jinja2 import TemplateNotFound
from sqlalchemy import desc
from app.base.models import Sfssum, ArrayMetric,Suffix


@blueprint.route('/')
# @login_required
def index():

    return render_template('index.html')

# def gen():
#   for i in range(100):
#      yield i

# prog = gen()

# @blueprint.route('/oom')
# def start_oom_triage():
#     global prog
#     try: 
#         p = next(prog)
#     except StopIteration:
#         prog = gen()
#         p = next(prog)

#     return jsonify(
#         progress = p,
#         nfsthread = 1234
#     )

@blueprint.route('/cpu')
def get_array_metrics_cpu():
    suffix = request.args.get('suffix', '', type=str)
    metrics = ArrayMetric.query.filter_by(suffix=suffix).order_by(ArrayMetric.Timestamp).all()
    res = []
    spacpu = []
    spbcpu = []
    timestamp = []

    for m in metrics:
        spacpu.append(m.SpaCpu)
        spbcpu.append(m.SpbCpu)
        timestamp.append(m.Timestamp)
    entry = {}
    entry['legend'] = "spa cpu"
    entry['labels'] = timestamp
    entry['data'] = spacpu
    res.append(entry)

    entry['legend'] = "spb cpu"
    entry['labels'] = timestamp
    entry['data'] = spbcpu
    res.append(entry)
    return jsonify(res)
    
@blueprint.route('/iops')
def get_array_metrics_iops():
    suffix = request.args.get('suffix', '', type=str)
    metrics = ArrayMetric.query.filter_by(suffix=suffix).order_by(ArrayMetric.Timestamp).all()
    res = []
    spaavgiops = []
    spbavgiops = []
    totavgiops = []
    timestamp = []

    for m in metrics:
        spaavgiops.append(m.SpaAvgIOPS)
        spbavgiops.append(m.SpbAvgIOPS)
        timestamp.append(m.Timestamp)
    entry = {}
    entry['legend'] = "Spa Avg IOPS"
    entry['labels'] = timestamp
    entry['data'] = spaavgiops
    res.append(entry)

    entry['legend'] = "Spb Avg IOPS"
    entry['labels'] = timestamp
    entry['data'] = spbavgiops
    res.append(entry)

    entry['legend'] = "Total Avg IOPS"
    entry['labels'] = timestamp
    entry['data'] = list(map(add, spaavgiops, spbavgiops))
    res.append(entry)

    return jsonify(res)

@blueprint.route('/kbps')
def get_array_metrics_kbps():
    suffix = request.args.get('suffix', '', type=str)
    metrics = ArrayMetric.query.filter_by(suffix=suffix).order_by(ArrayMetric.Timestamp).all()
    res = []
    spareadkbps = []
    spbreadkbps = []
    spawritekbps = []
    spbwritekbps = []
    timestamp = []

    for m in metrics:
        spareadkbps.append(m.SpaRdKBPS)
        spbreadkbps.append(m.SpbRdKBPS)
        spawritekbps.append(m.SpaWrtKBPS)
        spbwritekbps.append(m.SpaWrtKBPS)        
        timestamp.append(m.Timestamp)
    entry = {}
    entry['legend'] = "Spa Read KBPS"
    entry['labels'] = timestamp
    entry['data'] = spareadkbps
    res.append(entry)

    entry['legend'] = "Spb Read KBPS"
    entry['labels'] = timestamp
    entry['data'] = spbreadkbps
    res.append(entry)
    
    entry['legend'] = "Spa Write KBPS"
    entry['labels'] = timestamp
    entry['data'] = spawritekbps
    res.append(entry)

    entry['legend'] = "Spb Write KBPS"
    entry['labels'] = timestamp
    entry['data'] = spbwritekbps
    res.append(entry)

    return jsonify(res)

@blueprint.route('/size')
def get_array_metrics_size():
    suffix = request.args.get('suffix', '', type=str)

@blueprint.route('/nfs4')
def get_sfssum_nfs4():
    nlimit = request.args.get('limit', 10, type=int)
    noffset = request.args.get('offset', 0, type=int)
    benchmark =  request.args.get('benchmark', 'swbuild', type=str) 
    res = []
    sfscount = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%4_'+ benchmark +'%')).count()
    sfxs = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%4_'+ benchmark +'%')).order_by(desc(Suffix.Timestamp)).offset(noffset).limit(nlimit).all()
    for sfx in sfxs:
        entry = {}
        # print(sfx.suffix)
        sfssums = Sfssum.query.filter_by(suffix=sfx.suffix).order_by(Sfssum.BizMetric).all()
        opratelist = []
        avglatlist = []
        for sfs in sfssums:
            opratelist.append(sfs.AchiOpRate)
            avglatlist.append(sfs.AvgLat)
        entry['legend'] = sfx.suffix
        entry['labels'] = opratelist
        entry['data'] = avglatlist
        res.append(entry) 
    return render_template('page-nfs4.html', 
                            perfdata=res,
                            offset=noffset,
                            limit=nlimit,
                            count=sfscount,
                            benchmark=benchmark)

@blueprint.route('/smb')
def get_sfssum_smb():
    return

@blueprint.route('/nfs3api')
def get_sfssum_nfs3api():
    nlimit = request.args.get('limit', 10, type=int)
    noffset = request.args.get('offset', 0, type=int)
    benchmark =  request.args.get('benchmark', 'swbuild', type=str)
    perf = {}
    res = []
    sfscount = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%3_' + benchmark + '%')).count()
    sfxs = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%3_' + benchmark + '%')).order_by(desc(Suffix.Timestamp)).offset(noffset).limit(nlimit).all()
    for sfx in sfxs:
        entry = {}
        # print(sfx.suffix)
        sfssums = Sfssum.query.filter_by(suffix=sfx.suffix).order_by(Sfssum.BizMetric).all()
        opratelist = []
        avglatlist = []
        for sfs in sfssums:
            opratelist.append(sfs.AchiOpRate)
            avglatlist.append(sfs.AvgLat)
        entry['legend'] = sfx.suffix
        entry['Timestamp'] = sfx.Timestamp
        entry['labels'] = opratelist
        entry['data'] = avglatlist
        entry['build'] = sfx.build
        entry['desc'] = sfx.desc
        res.append(entry) 
    
    perf['res'] = res
    perf['count'] = sfscount
    perf['benchmark'] = benchmark

    return jsonify(perf)

@blueprint.route('/nfs3')
def get_sfssum_nfs3():
    nlimit = request.args.get('limit', 10, type=int)
    noffset = request.args.get('offset', 0, type=int)
    benchmark =  request.args.get('benchmark', 'swbuild', type=str)
    res = []
    sfscount = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%3_' + benchmark + '%')).count()
    sfxs = db.session.query(Suffix).filter(Suffix.suffix.like('%nfs%3_' + benchmark + '%')).order_by(desc(Suffix.Timestamp)).offset(noffset).limit(nlimit).all()
    for sfx in sfxs:
        entry = {}
        # print(sfx.suffix)
        sfssums = Sfssum.query.filter_by(suffix=sfx.suffix).order_by(Sfssum.BizMetric).all()
        opratelist = []
        avglatlist = []
        for sfs in sfssums:
            opratelist.append(sfs.AchiOpRate)
            avglatlist.append(sfs.AvgLat)
        entry['legend'] = sfx.suffix
        entry['labels'] = opratelist
        entry['data'] = avglatlist
        res.append(entry) 
    return render_template('page-nfs3.html', 
                            perfdata=res,
                            offset=noffset,
                            limit=nlimit,
                            count=sfscount,
                            benchmark=benchmark)

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
