# irctomqttbot

IRC bot that relays MQTT commands

#### Warning: This is probabally a bad idea
If you do want to use it be sure to understand the possible effects of allowing random interneters to send requests to your MQTT server.
There are no restrictions on who this bot will accept commands from, and most likely any in place wouldn't be enough to really be secure.


## Overview

This bot will connect to an IRC channel and send MQTT messages as defined in the config based on command in channel. The format for messaging the bot is `<Bot Username>:<Command Name>`.

## Install

### Docker

Docker container is availible on [Dockerhub](https://hub.docker.com/r/daviddever/irctomqttbot)

With Docker

```
docker run -d -v /docker_files/config:/home/appuser/config \
                 daviddever/irctomqttbot:latest
```

or with Docker Compose

```
services:

  linkgrabber:
    image: daviddever/irctomqttbot:latest
    container_name: irctomqttbot
    volumes:
      - /docker_files/config:/home/appuser/config
    restart: unless-stopped
```

Then copy `config_example.yaml` to the `/docker_files/config/config.yaml` and configure the settings.


### Manually

Assuming Ubuntu 20.04

#### Install pip

```
sudo apt-get install python3-pip
```

#### Setup virtualenv

```
pip3 install virtualenv
source venv/bin/activate
pip install -r requirements.txt
```

#### Create config directory and configure

```
mkdir config
cp config_example.yaml ./config/configure
vim ./config/configure
```

#### Set execute permisisons

```
chmod +x ircmqtt.py
```

#### Start the application

```
./ircmqtt.py
```


## Config
Looks for settings on startup in `.config/config.yaml` (You can copy the `example_config.yaml` to get started.)


The `config` section is for the information for the IRC and MQTT settings


The `command` section is for setting up the terms the bot looks for in IRC and the MQTT response that will be sent.
`example_config.yaml` has three example commands.


```
  commands:
    lights on:
      topic: "irc/light"
      message: "on"
      channels:
        - "#mqttbot"
```

The first element key is the string the IRC bot will watch for (in this case `lights on`)
The `topic` and `message` key value pairs are used to build the MQTT request.
If `channels` is used the bot will ignore the command unless it is in the defined channels.

An example of a [Home Assistant](https://home-assistant.io) automation based on the above example.


```
alias: IRC Turn On Light
trigger:
  - platform: mqtt
    topic: irc/light
    payload: 'on'

action:
  - service: light.turn_on
    data:
      entity_id:
        - light.bed_left_lamp
        - light.bed_right_lamp
```
