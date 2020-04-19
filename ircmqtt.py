#! /usr/bin/env python3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import paho.mqtt.client as mqtt


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, irc_channel, irc_nickname, irc_server, irc_port):
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
            Publisher.send_message('irc/light', message)
        else:
            c.notice(nick, 'Sorry I don\'t know what a ' + cmd + ' is')


class Publisher:
    def __init___(self, topic, message):
        self.message = message
        self.topic = topic

        client = mqtt.Client('sender')
        client.connect(mqtt_host, port=mqtt_port, keepalive=60, bind_address='')
        print(mqtt_host)

    def send_message(self, topic, message):
        client.publish(topic, message)


def main():
    # IRC settings
    irc_channel = '#mqttbot'
    irc_nickname = 'mqttbot'
    irc_server = 'irc.freenode.net'
    irc_port = 6667

    # MQTT settings
    global mqtt_host
    global mqtt_port
    mqtt_host = '192.168.86.5'
    mqtt_port = '1883'

    bot = ListenerBot(irc_channel, irc_nickname, irc_server, irc_port)
    bot.start()


if __name__ == '__main__':
    main()
