from sanic.response import json
from sanic import Blueprint

index_bp = Blueprint('index')

@index_bp.get('/x')
async def index_route(request):
  return json({'message': 'Welcome to the Sagefy service.'})
