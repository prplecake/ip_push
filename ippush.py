#!/usr/bin/env python3

import os
import json
import time
import logging.config
import logging
import subprocess
import urllib.request

from py_pushover_simple import pushover

import conf.logger_config as lc

def startLogger():
    if not os.path.isdir('log'):
        subprocess.call(['mkdir', 'log'])

    logging.config.dictConfig(lc.LOGGER_CONFIG)

    logger = logging.getLogger(__name__)
    logger.debug('Logger initialized.')

    return logger

def readSettings(sf):
    with open(sf) as sf:
        SECRETS = json.load(sf)
    return SECRETS


def sendMessage(message):
    p = pushover.Pushover()
    p.user = SECRETS['user_key']
    p.token = SECRETS['app_token']

    p.sendMessage(message)


class IPPush():
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)
        ))


    def get_current_ip(self):
        # note: https://wtfismyip.com doesn't care if you automate requests to
        # their service if it is for non-commercial use as long as you
        # rate-limit to at most one request/min/ip address. Failure to comply
        # may result in blockage.
        with urllib.request.urlopen('https://ipv4.wtfismyip.com/text') as url:
            self.ip = url.read().decode('utf-8').rstrip('\r\n')
        return self


    def get_old_ip(self):
        try:
            with open(os.path.join(self.__location__, 'ip.old')) as f:
                self.old_ip = f.readline().rstrip('\r\n')
        except:
            self.old_ip = '0.0.0.0'
        return self


    def send_ip_push(self):
        sloc = settings['server_location']
        ip = self.ip
        t = time.strftime('%c\n')
        message = t + 'New external IP for {} is {}\n\n Old IP was: {}'.format(
            sloc, ip, self.old_ip)
        sendMessage(message)
        logger.info('Push sent.')


    def write_new_ip(self):
        output = self.ip + '\n'
        with open(os.path.join(self.__location__, 'ip.old'), 'w') as f:
            f.write(output)
        logger.info('New IP Written.')



    def do_update(self):
        self.get_old_ip()
        self.get_current_ip()
        if self.ip != self.old_ip:
            try:
                self.send_ip_push()
            except:
                logger.error('Unable to send push.')
            self.write_new_ip()
        else:
            logger.info('IP did not change.')


if __name__ == '__main__':
    settings = readSettings('settings.json')
    SECRETS = settings['keys']
    logger = startLogger()

    IPPush().do_update()
