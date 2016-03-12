# coding=utf-8
"""
joinall.py - Sopel Join All Channels module
By: susmus
Licensed under the Eiffel Forum License 2.

http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
from os import path
import threading
from time import sleep
from datetime import datetime
import sopel.tools


exclude_channels = ['#example']

def read_logfile(self):
    logfile_path = path.join(self.config.core.homedir, 'logs', 'raw.log')
    with open(logfile_path, 'r') as f:
        contents = f.read()
    return contents

def setup(bot):
    def monitor(bot):
        channel_re = re.compile(r"(#[\w\-_]+)\s")
        sleep(5)
        while True:
            bot.write(['LIST'])

            # TODO: there must be a better way than reading the logfile!
            contents = read_logfile(bot)
            channels = list(set(channel_re.findall(contents)))
            bot_channels = [str(i) for i in bot.channels]
            diff = list(set(channels) - set(bot_channels) - set(exclude_channels))
            print("diff = {}".format(diff))

            for c in diff:
                if c not in exclude_channels:
                    sleep(0.5)
                    bot.join(c)

            sleep(60)

    targs = (bot,)
    t = threading.Thread(target=monitor, args=targs)
    t.start()
