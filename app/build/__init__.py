# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import Blueprint

build = Blueprint('build', __name__)

from . import views
