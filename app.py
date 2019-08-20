#!/usr/bin/python3
# -*- coding: utf-8 -*-
import read_config
import pydotplus
import functions
from tornado import web, escape, ioloop, httpclient, gen
import json
import jsonschema
from http import HTTPStatus
import exceptions
import logging
import sys
import os

# Dict for users
users = dict()
logger = logging.getLogger('bot_logger')


def dot_algorithm(user_id, user_name, text, lang='ru'):
    """
    This is main function. It make answer for user
    :param user_id: unic user id
    :param user_name:
    :param text:
    :param lang:
    :return:
    """
    global users
    node = 0
    # User ask end, history was forget
    if text.find('/end') >= 0:
        if lang == 'ru':
            msg = 'Алгоритм прерван по Вашему желанию. Можете начать сначала, используя команду /start'
        else:
            msg = 'The algorithm is interrupted at your request. You can start again use command /start'
        err = 1

    # User ask start
    elif text.find('/start') >= 0:
        # Must find the number of the solution. Split the line by space
        answ = text.split()
        # If length 2 then process. Example / start 1
        if len(answ) == 2:
            try:
                numer = int(answ[1])
            except ValueError:
                numer = -1
            # Let us verify that the solution exists
            if numer >= 1 and numer <= len(graph_object_list):
                numer -= 1
                users[user_id] = [numer, 'Start']
                node, msg, err = functions.dialog(node_name=users[user_id][1],
                                                  answer=1,
                                                  graph=graph_object_list[users[user_id][0]])
            else:
                if lang == 'ru':
                    msg = 'Вы ввели не правильный номер. Нужно вводить номер от 1 до %s' % len(graphs)
                else:
                    msg = 'You entered the wrong number, you need to enter from 1 to %s' % len(graphs)
                err = 2
        else:
            msg = 'You entered the start command in the wrong format, good format example /start 1'
            err = 3

    # if the user is not in the dictionary add
    elif text.find('/help') >= 0:
        if lang == 'ru':
            msg = 'Привет %s. Я могу помочь найти решение некоторых проблем, используя заранее подготовленные ' \
                  'графы решений. Чтобы посмотреть список решение введите /list. Для начала работы с решением ' \
                  'введите /start и номер решения, например /start 1. После я буду задавать вопросы и предлагать ' \
                  'варианты ответов, вводите номер нужного. Я запоминаю разговор (пока не перезагружен). Если ' \
                  'нужно прекратить наберите /end и вернетесь к выбору решения.' % user_name
        else:
            msg = 'Hi %s. I can help to find a solution to some problems using pre-prepared graphs solutions. ' \
              'You can see all available solutions with the /list command. For starting, you write /start and' \
              ' the solution number, for example /start 1. After I ask some questions that will help to sort' \
              ' out the problem. I remember our correspondence (if I do not restart) and I can continue from ' \
              'the previous place. If you want to finish, then write /end.' % user_name
        err = 4

    # Issue an existing list of algorithms with a description
    elif text.find('/list') >= 0:
        if lang == 'ru':
            msg = 'Список доступных решений (напишите /start и номер решения):<b/>'
        else:
            msg = 'List of available algorithms:<br/>'
        for i in range(0, len(graphs)):
            msg += '<br/>%s) %s %s' % (i + 1, graphs[i]['file_name'], graphs[i]['description'])
        err = 5

    # There are no active conversations with the user
    elif not (user_id in users):
        # We have not talked yet
        if lang == 'ru':
            msg = 'Привет %s. Я Вас не помню, пожалуйста введите команду /help для знакомства' % user_name
        else:
            msg = 'Hi %s. I do not remember you, let is get started with the command /help' % user_name
        err = 6

    # User answers the question
    else:
        try:
            text = int(text)
        except ValueError:
            text = 0
        node, msg, err = functions.dialog(users[user_id][1], text, graph_object_list[users[user_id][0]])

    # Here we get if the error in the graph or it is over
    if err:
        if user_id in users:
            users.pop(user_id, None)
            if lang == 'ru':
                msg += '<br/>История переписки удалена, можно начать сначала.'
            else:
                msg += '<br/>History is reset, you can start again.'
    # We move the user to a new node
    else:
        users[user_id][1] = node
    return msg


class Bot(web.RequestHandler):

    SUPPORTED_METHODS = ("GET", "POST", )
    tokens = set()

    def initialize(self, *args, **kwargs):
        """Get all token from file"""
        with open('tokens.txt') as fp:
            keys = fp.readlines()
            for key in keys:
                self.tokens.add(key.strip())

    def post(self):
        """Handles POST requests."""
        # Cross scripting
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))

        schema = {
            "type": "object",
            "properties": {
                "token": {"type": "string"},
                "user_id": {"type": "string"},
                "user_name": {"type": "string"},
                "text": {"type": "string"},
            },
            "required": ["token", "text", ]
        }

        # JSON schema validations
        try:
            request_data = escape.json_decode(self.request.body)
            jsonschema.validate(request_data, schema)
            logger.debug('Получил сообщение: %s' % request_data)
            """
            response = dot_algorithm(user_id=request_data['user_id'],
                                     user_name=request_data['user_name'],
                                     text=request_data['text'])
                                     """
            self.set_status(HTTPStatus.OK)
            print(request_data)
        except jsonschema.exceptions.ValidationError as err:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({'detail': err.message})
        except exceptions.AuthException:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            self.write({'detail': 'Authorization error for token = %s' % request_data['token']})

    def get(self):
        """Bot work only with POST request"""
        self.write({'error': 3,
                    'errorMessage': 'Bot work only with POST requests. '
                                    'Look - https://github.com/ProstakovAlexey/graph_bot'})


class Application(web.Application):
    def __init__(self, **kwargs):
        handlers = [
            (r"/bot", Bot),
        ]
        super(Application, self).__init__(handlers, **kwargs)


if __name__ == "__main__":
    # Read config file
    error, graphs, tokens, log, lang = read_config.read_config('config.ini')
    if error:
        print(error)
        exit(1)
    """
    на heroku логирование в файл не работает
    # Логирование в файл
    logger.setLevel('DEBUG')
    handler = logging.handlers.TimedRotatingFileHandler(log, when='midnight', interval=1, backupCount=3,
                                                        encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(handler)
    """
    # Логирование на экран
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('Bot %(levelname)s: %(message)s'))
    logger.addHandler(handler)



    logger.info('Программа запущена')

    # Read dot files
    graph_object_list = list()
    for graph in graphs:
        try:
            gr = pydotplus.graphviz.graph_from_dot_file(graph['file_name'])
            graph_object_list.append(functions.parse_dot(gr))
        except:
            logger.error('Can not parse dot file:', graph['file_name'])

    if not graph_object_list:
        logger.critical('Can not read any dot files')
        exit(1)

    logger.debug('Прочитал %s dot файлов' % len(graph_object_list))

    # Start app
    application = Application()
    port = int(os.environ.get('PORT', 5000))
    msg = "Listening at port {0}".format(port)
    logging.info(msg)
    application.listen(port)
    tornado_ioloop = ioloop.IOLoop.instance()
    periodic_callback = ioloop.PeriodicCallback(lambda: None, 500)
    periodic_callback.start()
    tornado_ioloop.start()
