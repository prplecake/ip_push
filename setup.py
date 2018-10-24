#!/usr/bin/env python3
import os
import json


def create_config(settings_file='settings.json'):
    if input("Create config now? (Y/n) ") in ['Y', 'y']:
        config = {'keys': {}, 'server_location': ''}
        config['keys']['user_key'] = str(input("Your Pushover User Key: "))
        config['keys']['app_token'] = str(input("Your Pushover App Token: "))
        config['server_location'] = str(input("Server Location: "))
        with open(settings_file, 'w') as cf:
            json.dump(config, cf, indent=4)
    else:
        print("You chose not to create config now.")
        print("Quitting.")
        exit()


def main():
    print("""
Welcome to the `ip_push` setup script! Very simply, this script creates a
configuration file for the `ippush.py` to use.

Find documentation at https://ip-push.rtfd.io
Find the source code at https://github.com/mtthwjrgnsn/ip_push
    """)

    settings_file = 'settings.json'

    if os.path.exists(settings_file):
        if input("""
The settings file already exists. Would you like to overwrite it? (Y/n)
        """) not in ['y', 'Y']:
            print("Exiting.")
            exit()
        else:
            create_config(settings_file)
    else:
        create_config(settings_file)

if __name__ == '__main__':
    main()
