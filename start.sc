cd /home/robokot/graph_bot
#gunicorn -D -b 0.0.0.0:8443 -p bot.pid -w1 --certfile=sert/bot.pem --keyfile=sert/bot.key app:api
gunicorn -D -b 0.0.0.0:8443 -p bot.pid -w1 app:api

