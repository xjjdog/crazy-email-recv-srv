import json
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import send_file
from data import dataInstance

app = Flask(__name__)
auth = HTTPBasicAuth()
dao = dataInstance


def web_start(host, port):
    app.run(host=host, port=port)


@auth.get_password
def get_pw(username):
    users = app.config['users'] 
    if username in users:
        return users.get(username)
    return None


@app.route('/')
@auth.login_required
def index():
    return send_file('static/index.html')


@app.route('/all')
@auth.login_required
def msg_all():
    rows = dao.read_all()
    return json.dumps(rows)


@app.route('/from/<addr>')
@auth.login_required
def msg_from(addr):
    rows = dao.read_from(addr)
    return json.dumps(rows)


@app.route('/to/<addr>')
@auth.login_required
def msg_to(addr):
    rows = dao.read_to(addr)
    return json.dumps(rows)


@app.route('/clear')
@auth.login_required
def msg_to():
    rows = dao.clear()
    return json.dumps(rows)
