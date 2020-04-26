#! /usr/bin/env python3

import irc.bot
import irc.strings
import paho.mqtt.client as mqtt
import time
import yaml


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, irc_channel, irc_nickname, irc_server, irc_port, publisher):
        self.publisher = publisher
        irc.bot.SingleServerIRCBot.__init__(
            self, [(irc_server, irc_port)], irc_nickname, irc_nickname
        )
        self.irc_channel = irc_channel

    def on_nicknameinuse(self, irc_channel, irc_nickname, irc_server, irc_port):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.irc_channel)
        print("connected to " + self.irc_channel)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())

    def do_command(self, e, cmd):
        print(cmd)
        nick = e.source.nick
        c = self.connection

        if cmd in full_config["commands"]:
            self.publisher.send_message(
                full_config["commands"][cmd]["topic"],
                full_config["commands"][cmd]["message"],
            )
            time.sleep(5)
            self.publisher.send_message(full_config["commands"][cmd]["topic"], "")
        else:
            c.notice(nick, "I'm sorry I don't know what a " + cmd + " is")


class Publisher:
    def __init__(self, mqtt_host, mqtt_port):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port

        self.client = mqtt.Client("sender")
        self.client.connect(mqtt_host, port=mqtt_port, keepalive=60, bind_address="")
        print("connected to " + mqtt_host)

    def send_message(self, topic, message):
        self.client.publish(topic, message)


def read_config(config_file_path):
    with open(config_file_path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

        return config


def main():
    # Read in configuration
    global full_config
    full_config = read_config("./config.yaml")

    # IRC settings
    irc_channel = full_config["config"]["irc_channel"]
    irc_nickname = full_config["config"]["irc_nickname"]
    irc_server = full_config["config"]["irc_server"]
    irc_port = full_config["config"]["irc_port"]

    # MQTT settings
    mqtt_host = full_config["config"]["mqtt_host"]
    mqtt_port = full_config["config"]["mqtt_port"]

    publisher = Publisher(mqtt_host, mqtt_port)
    bot = ListenerBot(irc_channel, irc_nickname, irc_server, irc_port, publisher)
    bot.start()


if __name__ == "__main__":
    main()
