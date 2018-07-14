from sanic import Sanic
from sanic.response import json

from config import config

from routes.index import index_bp

app = Sanic()

app.blueprint(index_bp)

app.run(host='0.0.0.0', port=8654, debug=config['debug'], workers=1)
