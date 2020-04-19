#! /usr/bin/env python3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import paho.mqtt.client as mqtt


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, irc_channel, irc_nickname, irc_server, irc_port, publisher):
        self.publisher = publisher
        irc.bot.SingleServerIRCBot.__init__(self, [(irc_server, irc_port)], irc_nickname, irc_nickname)
        self.irc_channel = irc_channel

    def on_nicknameinuse(self, irc_channel, irc_nickname, irc_server, irc_port):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        c.join(self.irc_channel)
        print('connected to irc!')

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == 'say':
            # TODO: split string and send text after say as a mqtt message
            pass
        if 'light' in cmd:
            message = cmd.split('=')[1]
            print(message)
            self.publisher.send_message('irc/light', message)
        else:
            c.notice(nick, 'Sorry I don\'t know what a ' + cmd + ' is')


class Publisher:
    def __init__(self, mqtt_host, mqtt_port):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port

        self.client = mqtt.Client('sender')
        self.client.connect(mqtt_host, port=mqtt_port, keepalive=60, bind_address='')
        print('connected to ' + mqtt_host)

    def send_message(self, topic, message):
        self.client.publish(topic, message)


def main():
    # IRC settings
    irc_channel = '#mqttbot'
    irc_nickname = 'mqttbot'
    irc_server = 'irc.freenode.net'
    irc_port = 6667

    # MQTT settings
    mqtt_host = '192.168.86.5'
    mqtt_port = 1883

    publisher = Publisher(mqtt_host, mqtt_port)
    bot = ListenerBot(irc_channel, irc_nickname, irc_server, irc_port, publisher)
    bot.start()


if __name__ == '__main__':
    main()
