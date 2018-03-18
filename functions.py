def parse_dot(dot):
    """
    Список всех ребер
    :param dot:
    :return:
    """
    # Сделать список всех узлов
    nodes = dict()
    # Список всех ребер. У ребра 3 свойства - откруда, куда и метка. Пример ребра
    for node in dot.get_node_list():
        key = node.get_name()
        try:
            nodes[key] = node.get_attributes()['label'].replace('"', '')
        except KeyError:
            nodes[key] = key
    edges = list()
    for edge in dot.get_edges():
        try:
            name = edge.get_attributes()['label'].replace('"', '')
        except KeyError:
            name = None
        edges.append([edge.get_source(), edge.get_destination(), name])
    return nodes, edges


def get_edges(one_node, all_edges):
    """
    Выдаем список только ребер, выходящих из этой вершины
    :param one_node: имя вершины
    :param all_edges: все ребра
    :return: result список ребер
    """
    result = list()
    for e in all_edges:
        if e[0] == one_node:
            result.append(e)
    return result


def dialog(node_name, answer, graph):
    """
    :param node_name: текущая вершина
    :param answer: ответ пользователя
    :return: новая текущая вершина и сообщение для пользователя и ошибка
    """
    all_nodes = graph[0]
    all_edges = graph[1]
    msg = ''
    err = 0
    if node_name == 'End':
        # Если это вершина End, то программа закончена
        msg = 'Поздравляю, алгоритм завершен'
        err = 21
    else:
        # Получаем список ребер из этой вершины
        edges = get_edges(node_name, all_edges)
        # Ребер должно быть 1 или больше, иначе это ошибка
        if len(edges) == 1:
            # Ребро одно, поэтому перехоми к следующей вершине
            node_name = edges[0][1]
        elif len(edges) > 1:
            # Вершин несколько, надо анализировать ответ
            if answer == 0 or answer > len(edges):
                # Ответ не правильный, вершину не меняем
                msg += 'Ответ не правильный, надо выбрать из предложенных и ввести его номер. '
            else:
                node_name = edges[answer - 1][1]
        else:
            msg += 'Ошибка! Из вершины с именем %s, комментарий %s нет ребер. ' \
                   'Из всех вершин кроме End должно вести хотя бы одно ребро.' % (node_name, all_nodes[node_name])
            err = 22
        if err == 0:
            # Сейчас у нас выбрана вершина, напечатаем к ней комментарий
            msg += all_nodes[node_name].replace(r'\n', ' ')
            # Получаем список ребер из этой вершины
            edges = get_edges(node_name, all_edges)
            if len(edges) == 1:
                # Если ребро 1, то надо просто нажать ОК и после перейти по ребру 1
                msg += '\nПо готовности напишите ок'
            else:
                # Если ребер более 1, то напечатать вопрос
                for i in range(1, len(edges) + 1):
                    msg += '\n%s) %s' % (i, edges[i - 1][2])
    return node_name, msg, err



