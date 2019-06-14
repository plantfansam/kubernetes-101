FROM python:3.7.2-stretch

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app

ENV FLASK_APP=app.py

# Notice that the Flask app is configured to serve on port `5678`.
CMD ["flask", "run", "-p", "5678", "-h", "0.0.0.0"]