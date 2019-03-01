FROM python:3.7.2-stretch

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app

CMD gunicorn --bind 0.0.0.0:9876 --graceful-timeout 1 --access-logfile - --error-logfile - --log-level debug wsgi:app
