---
  config:
    irc_channel: "#mqttbot"
    irc_nickname: "mqttbot"
    irc_server: "irc.freenode.net"
    irc_port: 6667

    mqtt_host: "mqtthost.example.com"
    mqtt_port: 1883

  commands:
    lights on:
      topic: "irc/light"
      message: "on"

    lights off:
      topic: "irc/light"
      message: "off"
