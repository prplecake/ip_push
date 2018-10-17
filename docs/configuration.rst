Configuration Options
=====================

General Configuration
---------------------

``settings.json`` contains the information needed to contact the Pushover API,
along with an option to specify where your server is located. It should go
without saying, but this file contains secrets and should **never** be uploaded
to the public internet.

The structure is as follows:

* ``keys``
  
  * ``user_key``, *string*, Pushover user key, found at https://pushover.net
  * ``app_token``, *string*, Pushover application token [#f1]_, found at https://pushover.net/apps

* ``server_location``: *string*, the location of your server, sent with the push
  message.


Example ``settings.json``
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    {
        "keys": {
            "user_key":     "PUSHOVER_USER_KEY",
            "app_token":    "PUSHOVER_APP_TOKEN"
        },
        "server_location":  "Server location identifier, e.g.: 'Home'"
    }

Logger Config
-------------

Log configuration is preconfigured in ``conf/logger_config.py``. Based off of
the `template here <https://dev.jrgnsn.net/snippets/1>`_.

.. rubric:: Footnotes

.. [#f1] More help can be found at :doc:`pushover-token`.
