#! /usr/bin/env python3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import paho.mqtt.client as mqtt


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, channel, nickname, server, port):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        c.join(self.channel)

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
        else:
            c.notice(nick, 'Sorry I don\'t know what a ' + cmd + ' is')


class Publisher:
    def __init___(self, message, host, port, topic, target):
        self.message = message
        self.host = host
        self.port = port
        self.topic = topic
        self.target = target

    def send_message(self, message, host, port, topic, target):
        client = mqtt.Client('sender')
        client.connect(host, port=port, keepalive=60, bind_address='')
        client.publish(topic + '/' + target, message)


def main():
    # IRC settings
    channel = '#mqttbot'
    nickname = 'mqttbot'
    server = 'irc.freenode.net'
    irc_port = 6667

    # MQTT settings
    host = '192.168.86.5'
    port = '1883'
    topic = 'irc'
    target = 'say'

    bot = ListenerBot(channel, nickname, server, irc_port)
    bot.start()


if __name__ == '__main__':
    main()
