#!/usr/bin/python3

"""

heroku logs -a api-cash4sms -t --source app

"""

import os
import uuid

from dbconnector import DB

from flask import Flask, request, jsonify, render_template
from random import randint, choice
from datetime import datetime, timedelta
from time import sleep

app = Flask(__name__)

#-----------------------------------------------------------------------

def error(code: int):

    _error = jsonify(
        code = code,
        msg = f'Some problem in {request.path}'
    )

    return (_error, 401)

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
    obj = DB().execute_dic('cash4sms_users', where=('client_id', client_id))

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

    client_id = request.get_json()['username']
    sms_code = request.get_json()['smscode']
    obj = DB().execute_dic('cash4sms_users', where=('client_id', client_id))

    if obj.get('sms_code') == int(sms_code):
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
    obj = DB().execute_dic('cash4sms_users', where=('client_id', client_id))
    updated_at = datetime.now().replace(microsecond=0).isoformat()
    update_keys = ['sms_code', 'updated_at']
    update_values = [str(randint(100_000, 999_999)), updated_at]
    DB().save('cash4sms_users', update_keys, update_values, where=('client_id', client_id))

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
    obj = DB().execute_dic('cash4sms_users', keys, where=('client_id', client_id))

    success = jsonify( obj or dict.fromkeys(keys, None) )

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_profile_change = '/profile/change'
@app.route(url_profile_change, methods=['POST'])
def request_url_profile_change():

    r_json = request.get_json()
    client_id = r_json.get('client_id')
    keys = ['first_name', 'last_name', 'birth', 'country', 'updated_at']
    obj = DB().execute_dic('cash4sms_users', keys, where=('client_id', client_id))

    if obj is not None:
        updated_at = datetime.now().replace(microsecond=0).isoformat()
        new_data = [r_json.get(keys[0]), r_json.get(keys[1]), r_json.get(keys[2]), r_json.get(keys[3]), updated_at]
        DB().save('cash4sms_users', keys, new_data, where=('client_id', client_id))
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
    obj = DB().execute_dic('cash4sms_users', keys, where=('client_id', client_id))

    success = jsonify( obj or dict.fromkeys(keys, None) )

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_password = '/password'
@app.route(url_password, methods=['POST'])
def request_url_password():

    client_id = request.get_json()['client_id']
    password = request.get_json()['password']
    updated_keys = ['password', 'updated_at']
    updated_values = [str(password), datetime.now().replace(microsecond=0).isoformat()]
    DB().save('cash4sms_users', updated_keys, updated_values, where=('client_id', client_id))

    success = jsonify( 
            msg = f'Success in {request.path}'
        )

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_password_recovery = '/password/recovery'
@app.route(url_password_recovery, methods=['POST'])
def request_url_password_recovery():

    client_id = request.get_json()['username']
    keys = ['client_id', 'password']
    obj = DB().execute_dic('cash4sms_users', keys, where=('client_id', client_id))

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

    client_id = request.get_json()['client_id']
    keys = ['balance_currency']
    obj = DB().execute_dic('cash4sms_accounts', keys, where=('client_id', client_id))

    array = []
    for i in range(randint(0, int(delta.days*0.7*0.4))):
        date = to_date - timedelta(days=31*i)
        item = {
            "date": int(date.timestamp()),
            "count": randint(1,999),
            "tariff": 4,
            "currency": obj.get(keys[0]) if obj is not None else 'EUR',
            "amount": randint(10,999)
        }
        array.append(item)

    success = jsonify(array)
    
    sleep(1)
    return success if randint(0,10) != 5 else error(404)

url_income = '/income'
@app.route(url_income, methods=['POST'])
def request_url_income():

    from_date = datetime.fromtimestamp(int(request.get_json()['from_date']))
    to_date = datetime.fromtimestamp(int(request.get_json()['to_date']))
    delta = to_date - from_date

    client_id = request.get_json()['client_id']
    keys = ['balance_currency']
    obj = DB().execute_dic('cash4sms_accounts', keys, where=('client_id', client_id))

    array = []
    for i in range(randint(0, int(delta.days*0.7*0.4))):
        date = to_date - timedelta(days=31*i)
        item = {
            "date_create": int(date.timestamp()),
            "date_transfer": int(date.timestamp()),
            "number": randint(1,9999),
            "status": choice(["unpaid", "paid", "rejected"]),
            "currency": obj.get(keys[0]) if obj is not None else 'EUR',
            "amount": randint(10,999)
        }
        array.append(item)

    success = jsonify(array)

    sleep(1)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_balance = '/balance'
@app.route(url_balance, methods=['POST'])
def request_url_balance():

    client_id = request.get_json()['client_id']
    keys = ['balance_amount', 'balance_currency', 'total_count']
    obj = DB().execute_dic('cash4sms_accounts', keys, where=('client_id', client_id))

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
    obj = DB().execute_dic('cash4sms_accounts', keys, where=('client_id', client_id))

    if obj is not None:
        return jsonify( 
            daily = obj.get(keys[0]),
            monthly = obj.get(keys[1]),
            enabled = obj.get(keys[2])
        )

    sleep(0.5)
    return error(404)

#-----------------------------------------------------------------------

url_notifications = '/notifications/<option>'
@app.route(url_notifications, methods=['POST'])
def request_url_notifications(option):

    rdata = request.get_json()
    updated_at = datetime.now().replace(microsecond=0).isoformat()

    if option == 'subscribe':
        client_id = rdata.get('client_id')
        push_token = rdata.get('push_token')
        update_keys = ['push_token', 'updated_at']
        update_values = [f'{push_token}', updated_at]
        DB().save('cash4sms_users', update_keys, update_values, where=('client_id', client_id))

    if option == 'status':
        client_id = rdata.get('client_id')
        push_id = rdata.get('push_id')
        push_status = rdata.get('status')
        update_keys = ['client_id', 'push_status', 'updated_at']
        update_values = [str(client_id), str(push_status), updated_at]
        DB().save_or_create('cash4sms_pushs', update_keys, update_values, where=('push_id', push_id))

    success = jsonify( 
        msg = f'Success in {request.path}'
    )
    
    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_messages = '/messages/getdata'
@app.route(url_messages, methods=['POST'])
def request_url_messages():

    client_id = request.get_json()['client_id']
    daily = request.get_json()['daily']

    array = list()
    for _ in range(randint(0,20)):
        item = {
            "number": randint(int('1' * len(client_id)),int('9' * len(client_id))),
            "message": f'{client_id} %RAND8%',
            "daily": randint(1,int(daily))
        }
        array.append(item)
    
    success = jsonify(array)

    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_chat = '/chat'
@app.route(url_chat, methods=['POST'])
def request_url_chat():

    count = int( request.get_json()['count'] )
    start = int( request.get_json()['start'] )

    array = list()
    for i in range(randint(0,count)):
        date = datetime.now() - timedelta(hours=(i+start))
        item = {
            "index": i + int(start),
            "message": {
                "from": choice(["user", "support"]),
                "msg": choice(["except you wont to sleep me", 
                                "please explain how work you fucking system", 
                                "i dont understand anything there"]),
                "timestamp": int(date.timestamp())
            }
        }
        array.append(item)
    
    success = jsonify( {"messages": array} )
    
    sleep(1)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

url_msg = '/chat/msg'
@app.route(url_msg, methods=['POST'])
def request_url_msg():

    success = jsonify( 
        msg = f'Success in {request.path}'
    )
    
    sleep(0.5)
    return success if randint(0,10) != 5 else error(404)

#-----------------------------------------------------------------------

@app.route('/')
@app.route('/user.html')
def user():

    keys = ['client_id', 'password', 'first_name', 'last_name', 'validated', 'sms_code', 'push_token']
    objs = DB().execute_dic('cash4sms_users', keys=keys, order='updated_at')
    return render_template('user.html', objs=objs)

@app.route('/push.html')
def push():

    objs = DB().execute_dic('cash4sms_pushs', order='updated_at')
    return render_template('push.html', objs=objs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

#-----------------------------------------------------------------------