import json
from flask import Flask
from flask import send_file
from data import dataInstance

app = Flask(__name__)
dao = dataInstance


def web_start(host, port):
    app.run(host=host, port=port)


@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/all')
def msg_all():
    rows = dao.read_all()
    return json.dumps(rows)


@app.route('/from/<addr>')
def msg_from(addr):
    rows = dao.read_from(addr)
    return json.dumps(rows)


@app.route('/to/<addr>')
def msg_to(addr):
    rows = dao.read_to(addr)
    return json.dumps(rows)
