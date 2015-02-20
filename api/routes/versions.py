# TODO this should probably be per entity type... unless there's
#      a way to make this a module

from flask import Blueprint

versions = Blueprint('versions', __name__, url_prefix='/api/versions')
