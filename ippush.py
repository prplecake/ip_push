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


def start_logger():
    if not os.path.isdir('log'):
        subprocess.call(['mkdir', 'log'])

    logging.config.dictConfig(lc.LOGGER_CONFIG)

    logger = logging.getLogger(__name__)
    logger.debug('Logger initialized.')

    return logger


def read_settings(sf):
    with open(sf) as sf:
        SECRETS = json.load(sf)
    return SECRETS


def send_message(message):
    p = pushover.Pushover()
    p.user = SECRETS['user_key']
    p.token = SECRETS['app_token']

    p.sendMessage(message)


class IPPush():
    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)
        ))
        self.ipv4 = None
        self.ipv6 = None

    def get_current_ip(self):
        # note: https://wtfismyip.com doesn't care if you automate requests to
        # their service if it is for non-commercial use as long as you
        # rate-limit to at most one request/min/ip address. Failure to comply
        # may result in blockage.
        try:
            with urllib.request.urlopen('https://ipv4.wtfismyip.com/text') as r:
                if r.code == 200:
                    logger.info('IPv4 capabilities are True')
                    self.ip = r.read().decode('utf-8').rstrip('\r\n')
        except urllib.error.HTTPError as e:
            logger.error(e)

        ipv6 = False
        try:
            with urllib.request.urlopen('https://ipv6.wtfismyip.com/text') as r:
                if r.code == 200:
                    ipv6 = True
                    logger.info('IPv6 capabilities are True')
                    self.ipv6 = r.read().decode('utf-8').rstrip('\r\n')
        except urllib.error.HTTPError as e:
            logger.error(e)
        except urllib.error.URLError as e:
            logger.info('IPv6 capabilities are False')
            logger.error(e)
        logger.debug('IPv6 Status: {}'.format(bool(ipv6)))
        return self

    def get_old_ip(self):
        try:
            with open(os.path.join(self.__location__, 'ip.old')) as f:
                self.old_ip = f.readline().rstrip('\r\n')
        except FileNotFoundError:
            self.old_ip = '0.0.0.0'

        try:
            with open(os.path.join(self.__location__, 'ipv6.old')) as f:
                self.old_ipv6 = f.readline().rstrip('\r\n')
        except FileNotFoundError:
            self.old_ipv6 = '::'

        return self

    def send_ip_push(self):
        sloc = settings['server_location']
        ip = self.ip
        ipv6 = self.ipv6
        t = time.strftime('%c\n')
        message = '''{}

IPv4:
New external IP for {} is
    {}
Old IP was:
    {}

IPv6:
New external IPv6 address is:
    {}
Old IPv6 address was:
    {}
'''.format(t, sloc, ip, self.old_ip, ipv6, self.old_ipv6)
        send_message(message)
        logger.info('Push sent.')

    def write_new_ip(self):
        output = self.ip + '\n'
        with open(os.path.join(self.__location__, 'ip.old'), 'w') as f:
            f.write(output)
        logger.info('New IP Written.')

        output2 = '{}\n'.format(self.ipv6)
        with open(os.path.join(self.__location__, 'ipv6.old'), 'w') as f:
            f.write(output2)

    def do_update(self):
        self.get_old_ip()
        self.get_current_ip()
        if (self.ip != self.old_ip): #or (self.ipv6 != self.old_ipv6):
            try:
                self.send_ip_push()
            except Exception as e:
                logger.error('Unable to send push. Exception:\n\n{}\n'.format(e))
            self.write_new_ip()
        else:
            logger.info('IP did not change.')


if __name__ == '__main__':
    settings = read_settings('settings.json')
    SECRETS = settings['keys']
    logger = start_logger()

    IPPush().do_update()
