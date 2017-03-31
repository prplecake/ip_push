# ip_tweet
Sends a DM to a specified user if the server's external IP address changes

The idea is to notify you of an IP address change in lieu of using a dynamic-DNS service.

External IP address is found using wtfismyip.com, which requests that you rate-limit yourself to one request per minute. Failure to do so may result in being blocked.

Settings go in the "settings.json" file. An example is included with the proper keys, all you have to do is copy "settings.json.example" to "settings.json" update for your specific needs.

The consumer_key, consumer_secret, access_token, and access_token_secret key-values come from your Twitter app, available at https://apps.twitter.com

The server_location key-value is used to distinguish which server sent the notification, in case you use this from multiple servers that exist behind different IP addresses.

The target_user key-value is the Twitter handle of the person to notify, which should probably be yourself.

This was written and tested under Python 3.
