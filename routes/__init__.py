from flask import Blueprint

main = Blueprint('main', __name__)

from routes import main as main_routes