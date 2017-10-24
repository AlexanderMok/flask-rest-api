# -*- coding: utf-8 -*-
from flask import jsonify
from flask import request

from api.v1 import api_version
from api.v1.service import urlcountservice


def _url_count_req_params(req_json):
    """
    private method to parse request params
    :param req_json: post request body
    :return: params tuple
    """
    url = req_json.get('url')
    sp = req_json.get('sp_code', 'sdo')
    begin_time = req_json.get('beginTime')
    end_time = req_json.get('endTime')
    page = req_json.get('page')
    size = req_json.get('size')
    return url, sp, begin_time, end_time, page, size


def _resp_header(resp):
    """
    private method to enable Cross Origin Resources Sharing(CORS)
    :param resp: Flask Response instance
    :return: Flask Response instance
    """
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Max-Age'] = 7200
    return resp


def _req_body_illegal():
    resp = jsonify({"error": "Request body is illegal. Is it none? "
                             "Do url, sp, begein_time, end_time, page and size exist?"})
    resp = _resp_header(resp)
    resp.status_code = 400
    return resp


@api_version.route('/url-req-status-count', methods=['POST', 'OPTIONS'])
def find_url_req_num_status():
    resp = jsonify({})
    if request.method == 'POST':
        req_json = request.get_json(silent=True)
        if not req_json or 'page' not in req_json or 'size' not in req_json or 'url' not in req_json \
                or 'beginTime' not in req_json or 'endTime' not in req_json:
            return _req_body_illegal()
        url, sp, begin_time, end_time, page, size = _url_count_req_params(req_json)
        result = urlcountservice.find_url_req_num_status(url, sp, begin_time, end_time, page, size)
        resp = jsonify(result)
    resp = _resp_header(resp)
    return resp


@api_version.route('/url-req-count', methods=['POST', 'OPTIONS'])
def find_url_req_num():
    resp = jsonify({})
    if request.method == 'POST':
        req_json = request.get_json(silent=True)
        if not req_json or 'page' not in req_json or 'size' not in req_json or 'url' not in req_json \
                or 'beginTime' not in req_json or 'endTime' not in req_json:
            return _req_body_illegal()
        req_json = request.get_json()
        url, sp, begin_time, end_time, page, size = _url_count_req_params(req_json)
        result = urlcountservice.find_url_req_num(url, sp, begin_time, end_time, page, size)
        resp = jsonify(result)
    resp = _resp_header(resp)
    return resp


@api_version.route('/url-status', methods=['POST', 'OPTIONS'])
def find_url_status():
    resp = jsonify({})
    if request.method == 'POST':
        req_json = request.get_json(silent=True)
        if not req_json or 'page' not in req_json or 'size' not in req_json or 'url' not in req_json \
                or 'beginTime' not in req_json or 'endTime' not in req_json:
            return _req_body_illegal()
        req_json = request.get_json()
        url, sp, begin_time, end_time, page, size = _url_count_req_params(req_json)
        result = urlcountservice.find_url_status(url, sp, begin_time, end_time, page, size)
        resp = jsonify(result)
    resp = _resp_header(resp)
    return resp
