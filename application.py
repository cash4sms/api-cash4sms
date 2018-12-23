#!/usr/bin/python3

"""

heroku logs -a api-cash4sms -t --source app

"""

import os
import uuid
import logging

from dbconnector import DB_Cash4SMS

from flask import Flask, request, jsonify
from random import choice, random, randint
from datetime import datetime, timedelta
from time import sleep

app = Flask(__name__)

#-----------------------------------------------------------------------

def request_logger(url, request):

    jb = request.get_json()
    body = f'\nREQUEST {url}\nBODY {jb}\n'
    message = '-'*80+body+'-'*80
    logging.info(message)

def request_error(code: str):

    error = {
        "code": 404,
        "msg": "Invalid credentials"
    }

    return (jsonify(error), 404)

#-----------------------------------------------------------------------

url_login = '/login'
@app.route(url_login, methods=['POST'])
def request_url_login():

    request_logger(url_login, request)

    success = {
        "access_token": uuid.uuid4().hex
    }

    sleep(0.5)
    return (jsonify(success), 200) if randint(0,10) != 5 else request_error(404)

#-----------------------------------------------------------------------

url_profile = '/profile'
@app.route(url_profile, methods=['POST'])
def request_url_profile():

    request_logger(url_profile, request)
    client_id = request.get_json()['client_id']
    
    sql = """
        SELECT first_name, last_name, birth, country, client_id
        FROM cash4sms_users
        WHERE client_id LIKE '{}'
    """.format(client_id)
    db = DB_Cash4SMS().execute(sql)

    success = {
        "first_name": db[0][0] if len(db) > 0 else None,
        "last_name": db[0][1] if len(db) > 0 else None,
        "birth": db[0][2] if len(db) > 0 else None,
        "country": db[0][3] if len(db) > 0 else None
    }

    sleep(0.5)
    return (jsonify(success), 200) if randint(0,10) != 5 else request_error(404)

#-----------------------------------------------------------------------

url_validated = '/validated'
@app.route(url_validated, methods=['POST'])
def request_url_validated():

    request_logger(url_validated, request)
    client_id = request.get_json()['client_id']
    
    sql = """
        SELECT validated, client_id
        FROM cash4sms_users
        WHERE client_id LIKE '{}'
    """.format(client_id)
    db = DB_Cash4SMS().execute(sql)

    sleep(0.5)
    if len(db) > 0:
        success = {
            "validated": db[0][0],
            "client_id": db[0][1]
        }
        return jsonify(success), 200
    
    return request_error(404)

#-----------------------------------------------------------------------

url_validated_getdata = '/validated/getdata'
@app.route(url_validated_getdata, methods=['POST'])
def request_url_validated_getdata():

    request_logger(url_validated_getdata, request)
    client_id = request.get_json()['client_id']
    
    array = []
    for _ in range(1, randint(1,10)):
        number = randint(10000000000,99999999999)
        item = {
            "number": number,
            "message": f'test from {client_id} to {number}'
        }
        array.append(item)

    success = array
    
    sleep(0.5)
    return (jsonify(success), 200) if randint(0,10) != 5 else request_error(404)

#-----------------------------------------------------------------------

url_stats = '/stats'
@app.route(url_stats, methods=['POST'])
def request_url_stats():

    request_logger(url_stats, request)

    from_date = datetime.fromtimestamp(int(request.get_json()['from_date']))
    to_date = datetime.fromtimestamp(int(request.get_json()['to_date']))
    delta = to_date - from_date

    array = []
    for i in range(randint(0, int(delta.days*0.7*0.4))):
        date = to_date - timedelta(days=31*i)
        item = {
            "date": int(date.timestamp()),
            "count": randint(1,999),
            "tariff": 4,
            "currency": "EUR",
            "amount": randint(10,999)
        }
        array.append(item)

    success = array
    
    sleep(0.5)
    return (jsonify(success), 200) if randint(0,10) != 5 else request_error(404)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

#-----------------------------------------------------------------------