#!/usr/bin/env python3

import os
import json
import time
import logging.config
import logging
import urllib.request

from py_pushover_simple import pushover

import conf.logger_config as lc


if not os.path.isdir('log'):
    os.mkdir('log')

logging.config.dictConfig(lc.LOGGER_CONFIG)

logger = logging.getLogger(__name__)
logger.debug('Logger initialized.')


def read_settings(sf):
    with open(sf) as sf:
        s = json.load(sf)
    return s


class IPPush():
    def __init__(self, settings):
        self.__location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)
        ))
        self.ipv4 = None
        self.old_ip = None
        self.ipv6 = None
        self.old_ipv6 = None
        self.settings = settings
        self.wtfismy_ipv4 = 'https://ipv4.wtfismyip.com/text'
        self.wtfismy_ipv6 = 'https://ipv6.wtfismyip.com/text'

    def get_current_ip(self):
        # note: https://wtfismyip.com doesn't care if you automate requests to
        # their service if it is for non-commercial use as long as you
        # rate-limit to at most one request/min/ip address. Failure to comply
        # may result in blockage.
        try:
            with urllib.request.urlopen(self.wtfismy_ipv4) as r:
                if r.code == 200:
                    logger.info('IPv4 capabilities are True')
                    self.ipv4 = r.read().decode('utf-8').rstrip('\r\n')
        except urllib.error.HTTPError as e:
            logger.error(e)

        ipv6 = False
        try:
            with urllib.request.urlopen(self.wtfismy_ipv6) as r:
                if r.code == 200:
                    ipv6 = True
                    logger.info('IPv6 capabilities are True')
                    self.ipv6 = r.read().decode('utf-8').rstrip('\r\n')
        except urllib.error.HTTPError as e:
            logger.error(e)
        except urllib.error.URLError:
            logger.info('IPv6 capabilities are False')
        logger.debug('IPv6 Status: %s', bool(ipv6))
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

    def send_push(self):
        sloc = self.settings['server_location']
        ip = self.ipv4
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
        self.send_message(message)
        logger.info('Push sent.')

    def write_new_ip(self):
        output = self.ipv4 + '\n'
        with open(os.path.join(self.__location__, 'ip.old'), 'w') as f:
            f.write(output)
        logger.info('New IP Written.')

        output2 = '{}\n'.format(self.ipv6)
        with open(os.path.join(self.__location__, 'ipv6.old'), 'w') as f:
            f.write(output2)

    def update(self):
        self.get_old_ip()
        self.get_current_ip()
        if self.ipv4 != self.old_ip:  # or (self.ipv6 != self.old_ipv6):
            try:
                self.send_push()
            except Exception as e:
                logger.error(
                    'Unable to send push. Exception:\n\n%s\n', e
                )
            self.write_new_ip()
        else:
            logger.info('IP did not change.')

    def send_message(self, message):
        p = pushover.Pushover()
        p.user = self.settings['keys']['user_key']
        p.token = self.settings['keys']['app_token']
        p.send_message(message)


if __name__ == '__main__':
    config = read_settings('settings.json')
    SECRETS = config['keys']

    IPPush(config).update()
