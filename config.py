# -*- coding:utf-8 -*-
# Copyright: HoneycombData
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hcd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'BuildMgmt.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    APP_ADMIN = 'Admin@hcdata.com'
    CELERY_BROKER_URL = 'redis://localhost:6379'
