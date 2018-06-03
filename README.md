# ip_tweet
Sends a notification via [Pushover][0] if the server's external IP address 
changes. Useful in case you can't use dynamic DNS.

[0]: https://pushover.net

External IP address is found using [WTF is my IP][1], which requests that you 
rate-limit yourself to one request per minute. Failure to do so may result in 
being blocked.

[1]: https://wtfismyip.com

Settings go in the "settings.json" file. An example is included with the proper
keys, all you have to do is copy "settings.json.example" to "settings.json" 
update for your specific needs.

The user_key, app_token, key-values come from your Pushover account.

The server_location key-value is used to distinguish which server sent the 
notification, in case you use this from multiple servers that exist behind 
different IP addresses.

This was written and tested under Python 3.

## Installation

**Prerequisites:** pip, [pushover][0] account

1. Clone the repository:

    ```
    git clone https://gitlab.com/matthewjorgensen/ip_push.git
    ```

2. Change dirs into the repo:

    ```
    cd ip_push
    ```

3. Install requirements:

    ```
    pip install -r requirements.txt
    ```

4. Copy `settings.json.example` to `settings.json`:

    ```
    cp settings.json.example settings.json
    ```

5. Set your secrets in `settings.json` with your favorite text editor.

## Scheduling

This program doesn't include scheduling on its own. I recommend you to set up a cron job to run as often as you'd like.

Example crontab entry:

    ```
    */5 * * * * cd /path/to/ip_push; ./ippush.py >/dev/null 2>&1
    ```

This will run ippush.py every 5 minutes.

## TODO

* Implement a logger

## Contributors

- Peter Jorgensen [Original Project] - (https://github.com/p2j/ip_tweet)
- Matthew Jorgensen [Pushover Adaptation]

## License

This project is licensed under the terms of the MIT license.