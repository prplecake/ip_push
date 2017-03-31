import re
import os
import urllib.request
import tweepy
import json
import time

def tweet_ip():
    IPTweet().do_update()
    return

class IPTweet(object):

    def __init__(self):
        self.__location__ = os.path.realpath(os.path.join(
                os.getcwd(), os.path.dirname(__file__)
        ))

    def get_current_ip(self):
        # note: https://wtfismyip.com doesn't care if you automate requests to their service if it is for non-commercial use as long as you rate-limit to at most one request/min/ip address. Failure to comply may result in blockage.
        with urllib.request.urlopen('https://ipv4.wtfismyip.com/text') as url:
            self.ip = url.read().decode('utf8').rstrip('\r\n')
        return self

    def get_old_ip(self):
        try:
            with open(os.path.join(self.__location__, 'ip.old')) as f:
                self.old_ip = f.readline().rstrip('\r\n')
        except:
            self.old_ip = '0.0.0.0'
        return self

    def get_twitter_keys(self):
        try:
            with open(os.path.join(self.__location__, 'settings.json')) as f:
                json_str = f.read()
        except FileNotFoundError:
            print('settings file not found')
        json_data = json.loads(json_str)
        self.c_k = json_data['keys']['consumer_key']
        self.c_s = json_data['keys']['consumer_secret']
        self.a_t = json_data['keys']['access_token']
        self.a_s = json_data['keys']['access_token_secret']
        self.server_location = json_data['server_location']
        self.target_user = json_data['target_user']
        return self

    def get_tweepy_auth(self):
        try:
            self.auth = tweepy.OAuthHandler(self.c_k, self.c_s)
            self.auth.set_access_token(self.a_t, self.a_s)
            self.tweepy_api = tweepy.API(self.auth)
        except Exception:
            self.tweepy_exception = 'there was an error with tweepy auth'
            raise Exception
        return self

    def send_ip_direct_message(self):
        sloc = self.server_location
        ip = self.ip
        target = self.target_user
        t = time.strftime('%c: ')
        message = t + 'New external IP for {} is: {}\n\n Old IP was: {}'.format(sloc, ip, self.old_ip)
        self.tweepy_api.send_direct_message(user=target, text=message)

    def write_new_ip(self):
        output = self.ip + '\n'
        with open(os.path.join(self.__location__, 'ip.old'), 'w') as f:
            f.write(output)

    def do_update(self):
        # get old ip
        self.get_old_ip()
        self.get_current_ip()
        if self.ip != self.old_ip:
            try:
                self.get_twitter_keys()
                self.get_tweepy_auth()
                self.send_ip_direct_message()
            except Exception:
                raise Exception
            self.write_new_ip()


if __name__ == '__main__':
    tweet_ip()
