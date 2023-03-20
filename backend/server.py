import hashlib
import hmac
import time

from flask import Flask, request, abort
from flask_cors import CORS

from config import BOT_TOKEN
from database import check_database, check_in_chat, update_database


def verify_data(user):
    received_hash_string = user.get('hash')
    auth_date = user.get('auth_date')

    if received_hash_string is None or auth_date is None:
        return False

    data_check_string = [f"{k}={v}" for k,
                         v in user.items() if k != 'hash']
    data_check_string = '\n'.join(sorted(data_check_string))
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    built_hash = hmac.new(
        secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    current_timestamp = int(time.time())
    auth_timestamp = int(auth_date)
    if current_timestamp - auth_timestamp > 86400:
        return False
    if built_hash != received_hash_string:
        return False
    return True


app = Flask(__name__)
CORS(app)


@app.route('/vote/', methods=['POST'])
def vote():
    data = request.json
    if 'user' not in data or not verify_data(user := data['user']) or not check_in_chat(user):
        abort(401)
    if check_database(user['id']):
        abort(403)
    update_database({
        'id': user['id'],
        'data': data['data']
    })
    return "successful"


if __name__ == '__main__':
    app.run('127.0.0.1', 8080, threaded=False)
