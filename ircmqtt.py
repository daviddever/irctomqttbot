#! /usr/bin/env python3

import datetime
import irc.bot
import irc.strings
import paho.mqtt.publish as mqtt
import yaml


class ListenerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, irc_channels, irc_nickname, irc_server, irc_port):
        super().__init__(
            [(irc_server, irc_port)],
            irc_nickname,
            irc_nickname,
            recon="ExponentialBackoff",
        )
        # list of channels to join
        self.irc_channels = irc_channels

    def on_nicknameinuse(self, c, e):
        """Actions to take if nick already in use"""
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        """Actions to take once connected to IRC server"""
        # join all configured channels
        for ch in self.irc_channels:
            c.join(ch)
            print(
                f"{datetime.datetime.now()}: connected to {ch}"
            )

    def on_pubmsg(self, c, e):
        """Actions to take when bot sees public message with its name"""
        # e.arguments[0] is the message text
        # "<botnick>: command text"
        msg = e.arguments[0]
        a = msg.split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            cmd_text = a[1].strip()
            self.do_command(e, cmd_text)

    def do_command(self, e, cmd):
        """Check if command in message is defined in config file and if so send appropriate MQTT message"""
        nick = e.source.nick
        c = self.connection

        # channel the message came from
        channel = e.target

        if cmd in commands:
            cmd_cfg = commands[cmd]

            # if the command has a "channels" list, enforce it
            allowed_channels = cmd_cfg.get("channels")
            if allowed_channels and channel not in allowed_channels:
                # command exists but is not allowed in this channel so ignore
                return

            mqtt_auth = None
            if mqtt_username:
                mqtt_auth = {"username": mqtt_username, "password": mqtt_password}

            mqtt.single(
                cmd_cfg["topic"],
                cmd_cfg["message"],
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
            print(f"{datetime.datetime.now()}: [{channel}] {cmd}")
        else:
            c.notice(nick, "I'm sorry I don't know what a " + cmd + " is")


def read_config(config_file_path):
    """Return a dictionary from yaml config file"""
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
    # support either a single irc_channel (string) or irc_channels (list)
    irc_channels = config.get("irc_channels")

    if irc_channels is None:
        # backwards compatibility with existing config: single-channel mode
        single_channel = config["irc_channel"]
        irc_channels = [single_channel]
    else:
        # Ensure it's a list
        if isinstance(irc_channels, str):
            irc_channels = [irc_channels]

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

    bot = ListenerBot(irc_channels, irc_nickname, irc_server, irc_port)
    bot.start()


if __name__ == "__main__":
    main()
