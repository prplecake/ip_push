# ip_push

Sends a notification via [Pushover][0] if the server's external IP
address changes. Useful in case you can't use dynamic DNS.

[0]: https://pushover.net

External IP address is found using [WTF is my IP][1], which requests
that you rate-limit yourself to one request per minute. Failure to do so
may result in being blocked.

[1]: https://wtfismyip.com

Settings go in the `settings.json` file. An example is included with the
proper keys, all you have to do is copy `settings.json.example` to
`settings.json` update for your specific needs.

The user\_key, app\_token, key-values come from your Pushover account.

The server\_location key-value is used to distinguish which server sent
the notification, in case you use this from multiple servers that exist
behind different IP addresses.

This was written and tested under Python 3.

Installation instruction are below. Additional information, including
how to obtain a pushover app token, can be found in the project wiki.

## Installation

**Prerequisites:** 

* pip
* [Pushover][0] account

1. Clone the repository:

        git clone https://github.com/mtthwjrgnsn/ip_push.git

2. Change dirs into the repo:

        cd ip_push

3. Install requirements:

        pip install -r requirements.txt

4. Use `setup.py` to configure your secrets:

        python3 setup.py

## Scheduling

This program doesn't include scheduling on its own. I recommend you to
set up a cron job to run as often as you'd like.

Example crontab entry:

    */5 * * * * cd /path/to/ip_push; ./ippush.py >/dev/null 2>&1

This will run ippush.py every 5 minutes.

## License

This project is licensed under the terms of the MIT license.

Inspired by [ip_tweet](https://github.com/p2j/ip_tweet).
