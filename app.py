#!/usr/bin/python3
# -*- coding: utf-8 -*-
import read_config
import pydotplus
import functions
import falcon
import json

# Read config file
error, graphs, tokens, log = read_config.read_config('for_tests/config_6.ini')
if error:
    print(error)
    exit(1)

# Read dot files
graph_object_list = list()
for graph in graphs:
    try:
        gr = pydotplus.graphviz.graph_from_dot_file(graph['file_name'])
        graph_object_list.append(functions.parse_dot(gr))
    except:
        print('Can not parse dot file:', graph['file_name'])

if len(graph_object_list) < 1:
    print('Can not read any dot files')
    exit(1)

# Dict for users
users = dict()


def dot_algoritm(user_id, user_name, text):
    """
    This is main function. It make answer for user
    :param user_id: unic user id
    :param user_name: имя пользователя
    :param text: сообщение пользователя
    :return:
    """
    global users
    node = 0
    # Если сказал end, забываем историю
    if text.find('/end') >= 0:
        msg = 'Алгоритм прерван по Вашему желанию. Можете начать сначала.'
        err = 1

    # сказал start, начинаем сначала
    elif text.find('/start') >= 0:
        # надо найти номер решения, к которому будем обращатся. Разбиваем строку по пробелу
        answ = text.split()
        # Если длина 2 то обрабатываем. Пример /start 1
        if len(answ) == 2:
            try:
                numer = int(answ[1])
            except ValueError:
                numer = -1
            # Проверим, что решение существует
            if numer >= 1 and numer <= len(graph_object_list):
                numer -= 1
                users[user_id] = [numer, 'Start']
                # Начать опрос
                print(users)
                print(user_id)
                print(numer)
                node, msg, err = functions.dialog(node_name=users[user_id][1],
                                                  answer=1,
                                                  graph=graph_object_list[users[user_id][0]])
            else:
                msg = 'Вы ввели неправильный номер, нужно вводить от 1 до %s' % len(graphs)
                err = 2
        else:
            msg = 'Вы ввели команду start в неправильном формате, нужно /start 1 или /start 2'
            err = 3

    # если пользователя нет в словаре добавим
    elif text.find('/help') >= 0:
        msg = 'Привет %s. Я могу помочь найти решение некоторых проблем используя заранее подготовленные графы' \
              'решений. Вы можете посмотреть все имеющиеся решения командой /list. ' \
              'Чтобы начать работу напишу /start и номер решения, например /start 1. После я задам несколько вопросов, которые' \
              'помогут разобраться с проблемой. Я запоминаю нашу переписку (если меня не перезагрузят) и можно продолжить' \
              'с предыдущего места. Если хочешь закончить, то напиши /end.' % user_name
        err = 4

    # Выдать имеющийся перечень алгоритмов с описанием
    elif text.find('/list') >= 0:
        msg = 'Перечень имеющихся алгоритмов:\n'
        for i in range(0, len(graphs)):
            msg += '\n%s) %s %s' % (i + 1, graphs[i]['file_name'], graphs[i]['description'])
        err = 5

    # Активных разговоров с пользователем нет
    elif not (user_id in users):
        # Мы еще не разговаривали
        msg = 'Привет %s. Я тебя не помню, дававай начнем работу с команды /help' % user_name
        err = 6

    # Пользователь отвечает на вопрос
    else:
        try:
            text = int(text)
        except ValueError:
            text = 0
        node, msg, err = functions.dialog(users[user_id][1], text, graph_object_list[users[user_id][0]])

    # Сюда попадаем если ошибка в графе или он окончен
    if err:
        if user_id in users:
            users.pop(user_id, None)
            msg += '\n История сброшена, можно начать снова.'
    # Перемещаем пользователя на новый узел
    else:
        users[user_id][1] = node
    return msg, err


class Bot:
    @staticmethod
    def on_post(req, resp):
        """Handles POST requests. Format:
        {
            'token':
            'user_id':
            'user_name':
            'text':
        }
        """
        body = req.stream.read().decode('utf-8')
        request = json.loads(body)

        response = ('JSON format is not valid.'+body, 'ERROR')
        #try:
            # Authorization
        if request['token'] in tokens:
                # token is valid, must work
                response = dot_algoritm(user_id=request['user_id'],
                                        user_name=request['user_name'],
                                        text=request['text'])
        else:
                response = ('token is not valid', 'ERROR')
        #except KeyError:
            # if has error, response make with error=2
        #    pass
        resp.body = json.dumps({'status': response[1], 'text': response[0]})

    @staticmethod
    def on_get(req, resp):
        """Bot work only with POST request"""
        response = {'error': 3,
                    'errorMessage': 'Bot work only with POST requests. '
                                    'Look - https://github.com/ProstakovAlexey/graph_bot'}
        resp.body = json.dumps(response)

api = falcon.API()
api.add_route('/bot', Bot())






