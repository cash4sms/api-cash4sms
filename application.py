#!/usr/bin/python3

"""

heroku logs -a api-cash4sms -t --source app

"""

import os
import uuid

from dbconnector import DB

from flask import Flask, request, jsonify, render_template
from random import randint
from datetime import datetime, timedelta
from time import sleep

app = Flask(__name__)

#-----------------------------------------------------------------------

def error(code: int):

    _error = jsonify(
        code = code,
        msg = f'Some problem in {request.path}'
    )

    return (_error, code)

#-----------------------------------------------------------------------

@app.after_request
def after_request(response):

    if request.method == 'POST':
        body = f'\nREQUEST {request.method} {request.path}\nBODY {request.get_json()}\n'
        message = '-'*80+body+'-'*80
        print(message)

    return response

#-----------------------------------------------------------------------

url_login = '/login'
@app.route(url_login, methods=['POST'])
def request_url_login():

    client_id = request.get_json()['username']
    obj = DB().execute_dic('cash4sms_users', ['*'], str(client_id))

    if obj is not None:
        return jsonify(
            access_token = uuid.uuid4().hex
        )

    sleep(0.5)
    return error(403)

#-----------------------------------------------------------------------

url_signup = '/signup'
@app.route(url_signup, methods=['POST'])
def request_url_signup():

    sms_code = request.get_json()['smscode']

    if sms_code == '555555':
        return jsonify(
            msg = f'Success in {request.path}'
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_getcode = '/getcode'
@app.route(url_getcode, methods=['POST'])
def request_url_getcode():

    client_id = request.get_json()['username']
    obj = DB().execute_dic('cash4sms_users', ['*'], str(client_id))

    if obj is not None:
        return jsonify(
            access_token = uuid.uuid4().hex
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_profile = '/profile'
@app.route(url_profile, methods=['POST'])
def request_url_profile():

    client_id = request.get_json()['client_id']
    keys = ['first_name', 'last_name', 'birth', 'country']
    obj = DB().execute_dic('cash4sms_users', keys, str(client_id))

    success = jsonify( obj or dict.fromkeys(keys, None) )

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_profile_change = '/profile/change'
@app.route(url_profile_change, methods=['POST'])
def request_url_profile_change():

    r_json = request.get_json()
    client_id = r_json.get('client_id')
    keys = ['first_name', 'last_name', 'birth', 'country']
    obj = DB().execute_dic('cash4sms_users', keys, str(client_id))

    if obj is not None:
        new_data = [r_json.get(keys[0]), r_json.get(keys[1]), r_json.get(keys[2]), r_json.get(keys[3])]
        DB().save('cash4sms_users', keys, new_data, str(client_id))
        return jsonify(
            msg = f'Success in {request.path}'
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_validated = '/validated'
@app.route(url_validated, methods=['POST'])
def request_url_validated():

    client_id = request.get_json()['client_id']
    keys = ['validated', 'client_id']
    obj = DB().execute_dic('cash4sms_users', keys, str(client_id))

    success = jsonify( obj or dict.fromkeys(keys, None) )

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_password = '/password'
@app.route(url_password, methods=['POST'])
def request_url_password():

    client_id = request.get_json()['client_id']
    password = request.get_json()['password']
    keys = ['client_id', 'password']
    obj = DB().execute_dic('cash4sms_users', keys, str(client_id))

    if obj.get('password') == password:
        return jsonify( 
            msg = f'Success in {request.path}'
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_password_recovery = '/password/recovery'
@app.route(url_password_recovery, methods=['POST'])
def request_url_password_recovery():

    client_id = request.get_json()['username']
    keys = ['client_id', 'password']
    obj = DB().execute_dic('cash4sms_users', keys, str(client_id))

    if obj is not None:
        return jsonify( 
            msg = f'Success in {request.path}'
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_validated_getdata = '/validated/getdata'
@app.route(url_validated_getdata, methods=['POST'])
def request_url_validated_getdata():

    client_id = request.get_json()['client_id']
    
    array = []
    for _ in range(1, randint(1,10)):
        number = randint(10000000000,99999999999)
        item = {
            'number': number,
            'message': f'test from {client_id} to {number}'
        }
        array.append(item)

    success = jsonify(array)
    
    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_stats = '/stats'
@app.route(url_stats, methods=['POST'])
def request_url_stats():

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

    success = jsonify(array)
    
    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_balance = '/balance'
@app.route(url_balance, methods=['POST'])
def request_url_balance():

    client_id = request.get_json()['client_id']
    keys = ['balance_amount', 'balance_currency', 'total_count']
    obj = DB().execute_dic('cash4sms_accounts', keys, str(client_id))

    if obj is not None:
        return jsonify( 
            balance = {
                "amount": obj.get(keys[0]),
                "currency": obj.get(keys[1])
            },
            total = {
                "count": obj.get(keys[2])
            }
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_limits = '/limits'
@app.route(url_limits, methods=['POST'])
def request_url_limits():

    client_id = request.get_json()['client_id']
    keys = ['limit_daily', 'limit_monthly', 'limit_enabled']
    obj = DB().execute_dic('cash4sms_accounts', keys, str(client_id))

    if obj is not None:
        return jsonify( 
            daily = obj.get(keys[0]),
            monthly = obj.get(keys[1]),
            enabled = obj.get(keys[2])
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

# @app.route('/home.html')
# def home():
#     return render_template('home.html')

# @app.route('/about.html')
# def about():
#     return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

#-----------------------------------------------------------------------