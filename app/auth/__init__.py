# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import forms, views

