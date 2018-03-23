Installing
==========

Modules install
---------------
Bot was write by python3, you need install it. I try this program in Ubuntu 14.04 and Ubuntu 16.04, and have python 3
in my system.

After python need install pip3 (packet manager), Ubuntu 14.04 have not it "from packet". Run command in
terminal::

   sudo apt-get -y install python3-pip


After install pip3 add modules::

    sudo pip3 install falcon gunicorn


Bot is publication in github, for get last version I recommend install git-client::

    sudo apt-get install git

Bot install
-----------
Download program in your machine::

    git clone https://github.com/ProstakovAlexey/graph_bot.git

After it command will be create directory `graph_bot`, please go to in it::

    cd graph_bot/

Bot running
-----------
Bot user https connection, because you need generation key and sertificate and place it in `sert`::

    cd sert\
    openssl req -newkey rsa:2048 -sha256 -nodes -keyout bot.key -x509 -days 365 -out bot.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=bot.EXAMPLE"

After it run script `start.sc`.

Check installing
----------------
You can check installing (bot must be running).

1. Check file `log.txt`, must have not error, example::

    [2018-03-23 10:29:39 +0300] [15595] [INFO] Starting gunicorn 19.7.1
    [2018-03-23 10:29:39 +0300] [15595] [INFO] Listening at: https://0.0.0.0:8443 (15595)
    [2018-03-23 10:29:39 +0300] [15595] [INFO] Using worker: sync
    [2018-03-23 10:29:39 +0300] [15598] [INFO] Booting worker with pid: 15598

2. Check file `bot.pid`, must have gunicorn process pid, for my example 15595

3. Run tests. Open file `tests.py`` and correct `port` and `addr` for your system. Save and run tests::

    python3 -m unittest tests.py

Have not errors, all tests ok. If you have problem, check `addr` and `port`.
