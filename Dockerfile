FROM python:3.8.0

COPY cfg.ini data.py main.py smtpx.py web.py requirements.txt /opt/crazy-email-recv-srv/
COPY static/ /opt/crazy-email-recv-srv/static/

WORKDIR /opt/crazy-email-recv-srv/

RUN pip install -r /opt/crazy-email-recv-srv/requirements.txt
# RUN sed -i "s/changeme/${password}/g" /opt/crazy-email-recv-srv/cfg.ini

EXPOSE 25 14000

ENTRYPOINT ["python", "main.py"]

