from smtpx import CrazySrvHandler
from web import web_start, app

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
import configparser
import os

if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("cfg.ini")

    smtpd_host = cf.get("smtpd", "host")
    smtpd_port = cf.getint("smtpd", "port")
    domains = cf.get("smtpd", 'domains').split(',')

    rest_host = smtpd_host
    rest_port = cf.getint("rest", "port")

    password = os.environ['password'] if os.environ['password'] else cf.get('auth', 'password')
    user = os.environ['user'] if os.environ['user'] else cf.get('auth', 'user')
    users = {user: password}
    app.config['users'] = users

    handler = CrazySrvHandler(domains)
    controller = Controller(handler, hostname=smtpd_host, port=smtpd_port)
    controller.factory = lambda: SMTP(handler, enable_SMTPUTF8=True)

    try:
        controller.start()
        web_start(rest_host, rest_port)
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        controller.stop()
