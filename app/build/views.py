# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import render_template, flash, redirect, url_for, request
from . import build
from app.models import BuildBranch, BuildPlatform, BuildHistory, BuildServer, db



@build.route('/build_index/')
def build_index():
    return render_template('build_index.html',
                           build_history=db.session.query(BuildHistory).all(),
                           build_branch=db.session.query(BuildBranch.branch_name).all(),
                           build_platform=db.session.query(BuildPlatform.os_type, BuildPlatform.cpu_type).all())


@build.route('/build_new/')
def build_new():
    return render_template('build_new.html',
                           build_branch=db.session.query(BuildBranch.branch_name).all(),
                           build_platform=db.session.query(BuildPlatform.os_type, BuildPlatform.cpu_type).all())


@build.route('/build_query/', methods=['POST'])
def build_query():
    error = None
    if request.method == 'POST':
        data = request.get_json()
        criteria = dict(d.split('=') for d in data.split('&'))
#        criteria_filter =
        branch = criteria.get('branch_select', None)
        platform = criteria.get('platform_select', None)
    else:
        error = 'Invalid branch name'
    build_query = db.session.query(BuildHistory).filter(BuildHistory.build_branch == branch, BuildHistory.build_platform == platform).all()
    return render_template('build_query.html', error=error, build_query=build_query)

