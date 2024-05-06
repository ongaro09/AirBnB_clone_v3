#!/usr/bin/python3
"""Flask Blueprint for handling RESTful API actions"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
