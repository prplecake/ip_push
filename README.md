# ip_tweet
Sends a notification via [Pushover][0] if the server's external IP address 
changes. Useful in case you can't use dynamic DNS.

[0]: https://pushover.net

External IP address is found using [WTFismyIP][1], which requests that you 
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
