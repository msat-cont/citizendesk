#!/usr/bin/env python
#
# Citizen Desk
#
'''
requests:

GET, DELETE
/feeds/twt/authorized/<doc_id>/

GET
/feeds/twt/authorized/

POST
/feeds/twt/authorized/
/feeds/twt/authorized/<doc_id>/finalize/

'''

import os, sys, datetime, json
from bson import json_util
try:
    from flask import Blueprint, request
except:
    sys.stderr.write('Flask module is not avaliable\n')
    os._exit(1)

from citizendesk.common.utils import get_logger, get_client_ip, get_allowed_ips
from citizendesk.common.dbc import mongo_dbs

bp_feed_twt_authorized = Blueprint('bp_feed_twt_authorized', __name__)

def setup_blueprints(app):
    app.register_blueprint(bp_feed_twt_authorized)
    return

@bp_feed_twt_authorized.route('/feeds/twt/authorized/<doc_id>', defaults={}, methods=['GET'], strict_slashes=False)
def feed_twt_authorized_get_one(doc_id):
    from citizendesk.feeds.twt.authorized import process

    logger = get_logger()
    client_ip = get_client_ip()

    res = process.do_get_one(mongo_dbs.get_db().db, doc_id)

    if not res[0]:
        ret_data = {'_meta': {'schema': process.schema, 'message': res[1]}}
        return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 404, {'Content-Type': 'application/json'})

    ret_data = {'_meta': {'schema': process.schema}, '_data': res[1]}
    return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 200, {'Content-Type': 'application/json'})

@bp_feed_twt_authorized.route('/feeds/twt/authorized/', defaults={}, methods=['GET'], strict_slashes=False)
def feed_twt_authorized_get_list():
    from citizendesk.feeds.twt.authorized import process

    logger = get_logger()
    client_ip = get_client_ip()

    params = {'offset': None, 'limit': None}
    for key in params:
        if key in request.args:
            try:
                params[key] = int(request.args.get(key))
            except:
                params[key] = None

    res = process.do_get_list(mongo_dbs.get_db().db, params['offset'], params['limit'])

    if not res[0]:
        ret_data = {'_meta': {'schema': process.schema, 'message': res[1]}}
        return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 404, {'Content-Type': 'application/json'})

    ret_data = {'_meta': {'schema': process.schema}, '_data': res[1]}
    if 3 >= len(res):
        ret_data['_meta']['list'] = res[2]
    return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 200, {'Content-Type': 'application/json'})

@bp_feed_twt_authorized.route('/feeds/twt/authorized/<doc_id>', defaults={}, methods=['DELETE'], strict_slashes=False)
def feed_twt_authorized_delete_one(doc_id):
    from citizendesk.feeds.twt.authorized import process

    logger = get_logger()
    client_ip = get_client_ip()

    res = process.do_delete_one(mongo_dbs.get_db().db, doc_id)

    if not res[0]:
        ret_data = {'_meta': {'schema': process.schema, 'message': res[1]}}
        return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 404, {'Content-Type': 'application/json'})

    ret_data = {'_meta': {'schema': process.schema}, '_data': res[1]}
    return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 200, {'Content-Type': 'application/json'})

@bp_feed_twt_authorized.route('/feeds/twt/authorized/', defaults={}, methods=['POST'], strict_slashes=False)
def feed_twt_authorized_post_one():
    from citizendesk.feeds.twt.authorized import process
    from citizendesk.feeds.config import get_config

    logger = get_logger()
    client_ip = get_client_ip()

    try:
        data = request.get_json(True, False, False)
        if type(data) is not dict:
            data = None
    except:
        data = None
    if data is None:
        try:
            data = request.json
            if type(data) is not dict:
                data = None
        except:
            data = None
    if data is None:
        return (json.dumps('provided data are not valid json'), 404, {'Content-Type': 'application/json'})

    auther_url = get_config('newstwister_url')

    res = process.do_post_one(mongo_dbs.get_db().db, auther_url, data)

    if not res[0]:
        ret_data = {'_meta': {'schema': process.schema, 'message': res[1]}}
        return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 404, {'Content-Type': 'application/json'})

    ret_data = {'_meta': {'schema': process.schema}, '_data': res[1]}
    return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 200, {'Content-Type': 'application/json'})

@bp_feed_twt_authorized.route('/feeds/twt/authorized/<doc_id>/finalize/', defaults={}, methods=['POST'], strict_slashes=False)
def feed_twt_authorized_finalize_one(doc_id):
    from citizendesk.feeds.twt.authorized import process

    logger = get_logger()
    client_ip = get_client_ip()

    try:
        data = request.get_json(True, False, False)
        if type(data) is not dict:
            data = None
    except:
        data = None
    if data is None:
        try:
            data = request.json
            if type(data) is not dict:
                data = None
        except:
            data = None
    if data is None:
        return (json.dumps('provided data are not valid json'), 404, {'Content-Type': 'application/json'})

    auther_url = get_config('newstwister_url')

    res = process.do_finalize_one(mongo_dbs.get_db().db, auther_url, doc_id, data)

    if not res[0]:
        ret_data = {'_meta': {'schema': process.schema, 'message': res[1]}}
        return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 404, {'Content-Type': 'application/json'})

    ret_data = {'_meta': {'schema': process.schema}, '_data': res[1]}
    return (json.dumps(ret_data, default=json_util.default, sort_keys=True), 200, {'Content-Type': 'application/json'})
