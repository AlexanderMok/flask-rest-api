# -*- coding: utf-8 -*-
from flask import jsonify

from api.v1 import api_version
from app import app_flask


@api_version.errorhandler(405)
def handle_method_not_allowed_error(error):
    app_flask.logger.exception(error)
    resp = jsonify({'error': 'The request method is not allowed for the requested URL.'})
    resp.status_code = error.status_code
    return resp
