from flask import Blueprint

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

from .import routes, models