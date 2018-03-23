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
    :param user_name:
    :param text:
    :return:
    """
    global users
    node = 0
    # User ask end, history was forget
    if text.find('/end') >= 0:
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
                msg = 'You entered the wrong number, you need to enter from 1 to %s' % len(graphs)
                err = 2
        else:
            msg = 'You entered the start command in the wrong format, good format example /start 1'
            err = 3

    # if the user is not in the dictionary add
    elif text.find('/help') >= 0:
        msg = 'Hi% s. I can help to find a solution to some problems using pre-prepared graphs solutions. ' \
              'You can see all available solutions with the / list command. For starting, you write /start and' \
              ' the solution number, for example /start 1. After I ask some questions that will help to sort' \
              ' out the problem. I remember our correspondence (if I do not restart) and I can continue from ' \
              'the previous place. If you want to finish, then write /end.' % user_name
        err = 4

    # Issue an existing list of algorithms with a description
    elif text.find('/list') >= 0:
        msg = 'List of available algorithms:\n'
        for i in range(0, len(graphs)):
            msg += '\n%s) %s %s' % (i + 1, graphs[i]['file_name'], graphs[i]['description'])
        err = 5

    # There are no active conversations with the user
    elif not (user_id in users):
        # We have not talked yet
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
            msg += '\n History is reset, you can start again.'
    # We move the user to a new node
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
        try:
            # Authorization
            if request['token'] in tokens:
                # token is valid, must work
                response = dot_algoritm(user_id=request['user_id'],
                                        user_name=request['user_name'],
                                        text=request['text'])
            else:
                response = ('Token is not valid', 'ERROR')
        except KeyError:
            # if has error, response make with error=2
            response = ('JSON format is not valid', 'ERROR')
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





