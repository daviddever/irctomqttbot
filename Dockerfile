FROM python:slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ircmqtt.py .
COPY LICENSE .

CMD [ "python", "./ircmqtt.py" ]
