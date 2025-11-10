FROM python:3.12-slim

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ircmqtt.py .
COPY LICENSE .

CMD [ "python", "./ircmqtt.py" ]
