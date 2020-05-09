#! /usr/bin/env python3

import datetime
import irc.bot
import irc.strings
import paho.mqtt.publish as mqtt
import yaml


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(
        self, irc_channel, irc_nickname, irc_server, irc_port,
    ):
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [(irc_server, irc_port)],
            irc_nickname,
            irc_nickname,
            recon="ExponentialBackoff",
        )
        self.irc_channel = irc_channel

    def on_nicknameinuse(self, irc_channel, irc_nickname, irc_server, irc_port):
        "Actions to take if nick already in use"
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        "Actions to take once connected to IRC server"
        c.join(self.irc_channel)
        print(str(datetime.datetime.now()) + ": " + "connected to " + self.irc_channel)

    def on_pubmsg(self, c, e):
        "Actions to take when bot sees public message with its name"
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())

    def do_command(self, e, cmd):
        "Check if command in message is defined in config file and if so send appropriate MQTT message"
        nick = e.source.nick
        c = self.connection

        if cmd in commands:
            mqtt_auth = None
            if mqtt_username:
                mqtt_auth = {"username": mqtt_username, "password": mqtt_password}

            mqtt.single(
                commands[cmd]["topic"],
                commands[cmd]["message"],
                qos=0,
                retain=False,
                hostname=mqtt_host,
                port=mqtt_port,
                client_id=mqtt_client_id,
                keepalive=60,
                will=None,
                auth=mqtt_auth,
                tls=None,
            )
            print(str(datetime.datetime.now()) + ": " + cmd)
        else:
            c.notice(nick, "I'm sorry I don't know what a " + cmd + " is")


def read_config(config_file_path):
    "Return a dictionary from yaml config file"
    with open(config_file_path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

        return config


def main():
    # Read in configuration
    full_config = read_config("./config/config.yaml")
    global commands
    commands = full_config["commands"]
    config = full_config["config"]

    # IRC settings
    irc_channel = config["irc_channel"]
    irc_nickname = config["irc_nickname"]
    irc_server = config["irc_server"]
    irc_port = config["irc_port"]

    # MQTT settings
    global mqtt_host
    global mqtt_port
    global mqtt_client_id
    global mqtt_username
    global mqtt_password
    mqtt_host = config["mqtt_host"]
    mqtt_port = config["mqtt_port"]
    mqtt_client_id = config["mqtt_client_id"]
    mqtt_username = config["mqtt_username"]
    mqtt_password = config["mqtt_password"]

    bot = ListenerBot(irc_channel, irc_nickname, irc_server, irc_port,)
    bot.start()


if __name__ == "__main__":
    main()
