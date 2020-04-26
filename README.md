# irctomqttbot

IRC bot that relays MQTT commands

#### Warning: This is probabally a bad idea
If you do want to use it be sure to understand the possible effects of allowing random interneters to send requests to your MQTT server.
There are no restrictions on who this bot will accept commands from, and most likely any in place wouldn't be enough to really be secure.


## Overview
Looks for settings on startup in `./config.yaml` (You can copy the `example_config.yaml` to get started.


The `config` section is for the information for the IRC and MQTT settings


The `command` section is for setting up the terms the bot looks for in IRC and the MQTT response that will be sent.
`example_config.yaml` has two example commands.


```
  commands:
    lights on:
      topic: "irc/light"
      message: "on"
```

The first element key is the string the IRC bot will watch for (in this case `lights on`)
The `topic` and `message` key value pairs are used to build the MQTT request.

An example of a [Home Assistant](home-assistant.io) automation based on the above example.


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
