---
  config:
    irc_channel: "#mqtt"
    irc_nickname: "mqttbot"
    irc_server: "irc.freenode.net"
    irc_port: 6667

    mqtt_host: "mqtthost.some.domain"
    mqtt_port: 1883

  commands:
    turn_on_lights:
      name: "Turn on Lights"
      trigger: "light on"
      topic: "irc/light"
      message: "on"

    turn_off_lights:
      name: "Turn off Lights"
      trigger: "light off"
      topic: "irc/light"
      message: "off"
