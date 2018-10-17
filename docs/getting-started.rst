Getting Started
===============

Ready to have some fun? 🙂

Prerequisites
-------------

You will need:

#. python 3
#. pip
#. a pushover account

Installation
------------

1. Clone the repository::

    git clone https://dev.jrgnsn.net/matthew/ip_push.git

2. Change dirs into the repo::

    cd ip_push

3. Install requirements::

    pip install -r requirements.txt

4. Copy ``settings.json.example`` to ``settings.json``::
    
    cp setings.json.example settings.json

5. Set your secrets in ``settings.json`` with your favorite text editor.

Scheduling
----------

This program doesn't include scheduling on its own. I recommend you to set up a cronjob to run as often as you'd like. [#f1]_

Example crontab entry::

    */5 * * * * cd /path/to/ip_push; ./ippush.py >/dev/null 2>&1

This would run ``ippush.py`` every 5 minutes.

.. todo:: Verify that crontab entry still logs to file.

.. rubric:: footnotes

.. [#f1] Keep in mind https://wtfismyip.com requests you limit yourself to no more than 1 request per minute.