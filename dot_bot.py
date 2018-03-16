#!/usr/bin/python3
# -*- coding: utf-8 -*-
import read_config
import logging
import pydotplus
import functions
import falcon
import json

# Read config file
error, graphs, tokens, log = read_config.read_config('config.ini')
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
    print('Can not read all dot files')
    exit(1)

# Dict for users
users = dict()

# logging


def dot_algoritm(user_id, user_name, text):
    """
    This is main function. It make answer for user
    :param user_id: unic user id
    :param text: имя пользователя
    :param text: сообщение пользователя
    :return:
    """
    global users
    # Если сказал end, забываем историю
    if text.find('end') >= 0:
        msg = 'Алгоритм прерван по Вашему желанию. Можете начать сначала.'
        err = 1

    # сказал start, начинаем сначала
    elif text.find('start') >= 0:
        # надо найти номер решения, к которому будем обращатся
        answ = text.split()
        if len(answ) == 2:
            try:
                numer = int(answ[1]) - 1
            except:
                numer = -1
            # Проверим, что решение существует
            if numer >= 0 and numer < len(graph_list):
                users[user_id] = [numer, 'Start']
                # Начать опрос
                node, msg, err = functions.dialog(users[user_id][1], 1, graph_object_list[users[user_id][0]])
            else:
                msg = 'Вы ввели неправильный номер, нужно вводить от 1 до %s' % len(graph_list)
                err = 1
        else:
            msg = 'Вы ввели команду start в неправильном формате, нужно /start 1 или /start 2'
            err = 1

    # если пользователя нет в словаре добавим
    elif text.find('/help') >= 0:
        msg = 'Привет %s. Я могу помочь найти решение некоторых проблем используя заранее подготовленные графы' \
              'решений. Вы можете посмотреть все имеющиеся решения командой /list. ' \
              'Чтобы начать работу напишу /start и номер решения, например /start 1. После я задам несколько вопросов, которые' \
              'помогут разобраться с проблемой. Я запоминаю нашу переписку (если меня не перезагрузят) и можно продолжить' \
              'с предыдущего места. Если хочешь закончить, то напиши /end.' % user_name
        err = 1
    # Выдать имеющийся перечень алгоритмов с описанием
    elif text.find('/list') >= 0:
        msg = 'Перечень имеющихся алгоритмов:\n'
        for i in range(0, len(graph_list)):
            msg += '\n%s) %s %s' % (i + 1, graph_list[i][0], graph_list[i][1])
        err = 1

    # Активных разговоров с пользователем нет
    elif not (user_id in users):
        # Мы еще не разговаривали
        msg = 'Привет %s. Я тебя не помню, дававай начнем работу с команды /help' % user_name
        err = 1

    # Пользователь отвечает на вопрос
    else:
        try:
            text = int(text)
        except:
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


class Bot:
    def on_post(self, req, resp):
        """Handles POST requests. Format:
        {
            'token':
            'user_id':
            'user_name':
            'text':
        }
        """
        request = json.loads(req.body)
        response = {'error': 2, 'errorMessage': 'JSON format is not valid'}
        try:
            # Authorization
            if request['token'] in tokens:
                # token is valid, must work
                response = dot_algoritm(user_id = request['user_id'],
                                        user_name = request['user_name'],
                                        text = request['text'])
            else:
                response = {'error': 1, 'errorMessage': 'token is not valid'}
        except KeyError:
            # if has error, response make with error=2
            pass
        resp.body = json.dumps(response)

if __name__ == '__main__':
    api = falcon.API()
    api.add_route('/bot', Bot())






