from flask import Blueprint

import config

api_version = Blueprint(config.API_VERSION_V1, __name__)
from errors import *
from endpoint import *
