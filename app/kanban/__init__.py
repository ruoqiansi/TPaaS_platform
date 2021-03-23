# -*- coding:utf-8 -*-
# Copyright: HoneycombData
from flask import Blueprint

kanban = Blueprint('kanban', __name__)

from . import views
