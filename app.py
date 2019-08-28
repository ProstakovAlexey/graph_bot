#!/usr/bin/python3
# -*- coding: utf-8 -*-
import read_config
from tornado import web, escape, ioloop, httpclient, gen
import logging
import sys
import os
import errors_code
import classes
import traceback

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

thread_pool_executor = ThreadPoolExecutor()

# Dict for users
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

users_dict = dict()


class AsyncBot(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST",)
    _thread_pool_executor = thread_pool_executor

    def initialize(self, *args, **kwargs):
        pass

    @gen.coroutine
    def post(self):
        """Handles POST requests."""
        try:
            request_data = escape.json_decode(self.request.body)['message']
            logger.debug('Получил сообщение: %s' % request_data)
            response = yield self.dot_algorithm(user_id=request_data['from']['id'],
                                     user_name=request_data['from']['username'],
                                     text=request_data['text'],
                                     lang=request_data['from']['language_code'])
        except:
            mtype, value, trace = sys.exc_info()
            logging.error("type=%s, value=%s, trace=%s" % (mtype, value, traceback.format_exc()))
            self.set_status(200)
        else:
            self.write({'method': 'sendMessage', 'chat_id': request_data['chat']['id'], 'text': response})

    def get(self):
        """Bot work only with POST request"""
        # // TODO написать тут страницу со справкой
        self.write('errorMessage')


    def command(self, user, text):
        c_graph = classes.GraphObject()
        result = errors_code.get_error(25, user.get_lang())
        # User ask end, history was forget
        if text.find('/end') >= 0:
            user.clear()
            result = errors_code.get_error(1, user.get_lang())
        # User ask start
        elif text.find('/start') >= 0:
            # Must find the number of the solution. Split the line by space
            # If length 2 then process. Example / start 1
            try:
                numer = int(text.split()[1])
            except:
                result = errors_code.get_error(4, user.get_lang())
            else:
                # Let us verify that the solution exists
                if 1 <= numer <= c_graph.len():
                    numer -= 1
                    user.start(schema=c_graph.get_by_id(numer))
                    result = user.next_dialog("any")
                else:
                    result = errors_code.get_error(2, user.get_lang())

        # if the user is not in the dictionary add
        elif text.find('/help') >= 0:
            result = errors_code.get_error(5, user.get_lang()) % user.get_name()

        # Issue an existing list of algorithms with a description
        elif text.find('/list') >= 0:
            result = errors_code.get_error(6, user.get_lang())
            for i in range(0, len(graphs)):
                result += '\n%s) %s %s' % (i + 1, graphs[i]['file_name'], graphs[i]['description'])
        return result

    @run_on_executor(executor="_thread_pool_executor")
    def dot_algorithm(self, user_id, user_name, text, lang):
        """
        This is main function. It make answer for user
        :param user_id: unic user id
        :param user_name:
        :param text:
        :param lang:
        :return:
        """

        # We have not talked yet
        if user_id not in users_dict:
            result = errors_code.get_error(7, lang) % user_name
            users_dict[user_id] = classes.User(user_id, user_name, lang)
            return result
        user = users_dict[user_id]
        if text[0] == '/':
            # command
            result = self.command(user, text)
        else:
            # answer
            result = user.next_dialog(text)
        return result


class Application(web.Application):
    def __init__(self, **kwargs):
        handlers = [
            (r"/bot", AsyncBot),
        ]
        super(Application, self).__init__(handlers, **kwargs)


if __name__ == "__main__":
    # Read config file
    error, graphs, log, _ = read_config.read_config('config.ini')
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
    logger.info('Program is run')

    # Read dot files
    graph = classes.GraphObject()
    graph.append(graphs)
    if graph.len() < 1:
        logger.critical('Can not read any dot files')
        exit(1)
    logger.debug('Read %s dot file(s)' % graph.len())

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
