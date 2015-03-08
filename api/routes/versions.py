# TODO@ this should probably be per entity type... unless there's
#      a way to make this a module

from flask import Blueprint

versions_routes = Blueprint('versions', __name__, url_prefix='/api/versions')
