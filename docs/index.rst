.. ip_push documentation master file, created by
   sphinx-quickstart on Tue Oct 16 22:23:06 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ip_push's documentation!
===================================

``ip_push`` sends a notification via `Pushover`_ if the server's external IP
address changes. Useful in cases where you can't use Dynamic DNS.

.. _Pushover: https://pushover.net

The external IP address is found using `WTF is my IP?`_, which requests that you
rate limit yourself to one request per minute. Failure to do so may result in
being blocked.

.. _WTF is my IP?: https://wtfismyip.com

Settings go in the ``settings.json`` file. An example is included with the proper
keys, all you have to do is copy `settings.json.example` to `settings.json`, and
update the relevant values. See more in :doc:`getting-started`.

This was written and tested under Python 3.

Contributors
============

* Peter Jorgensen [Original Project] - https://github.com/p2j/ip_tweet
* Matthew Jorgensen [This Puchover adaptation]

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Contents:

    getting-started
    configuration
    pushover-token
