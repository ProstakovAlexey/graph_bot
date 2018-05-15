def parse_dot(dot):
    """
    List all node and edges
    :param dot: dot type
    :return: dict nodes, list edges
    """

    # Dict for node. Node have only label.
    nodes = dict()
    for node in dot.get_node_list():
        key = node.get_name()
        try:
            nodes[key] = node.get_attributes()['label'].replace('"', '')
        except KeyError:
            nodes[key] = key
    edges = list()
    # List all edges. Edge have values: from, to, label
    for edge in dot.get_edges():
        try:
            name = edge.get_attributes()['label'].replace('"', '')
        except KeyError:
            name = None
        edges.append([edge.get_source(), edge.get_destination(), name])
    return nodes, edges


def get_edges(one_node, all_edges):
    """
    List all edges, for one node
    :param one_node: node
    :param all_edges: all edges
    :return: result: edges list
    """
    result = list()
    for e in all_edges:
        if e[0] == one_node:
            result.append(e)
    return sorted(result)


def dialog(node_name, answer, graph):
    """
    :param node_name: current node
    :param answer: user answer
    :return: new current node and message for user
    """
    all_nodes = graph[0]
    all_edges = graph[1]
    msg = ''
    err = 0
    if node_name == 'End':
        msg = 'Поздравляю. Алгоритм завершен'
        # msg = 'Congratulations, the algorithm is complete'
        err = 21
    else:
        # Получаем список ребер из этой вершины
        edges = get_edges(node_name, all_edges)
        # Must be one or more edges else error in dot file
        if len(edges) == 1:
            # Node have one edges, go to next node
            node_name = edges[0][1]
        elif len(edges) > 1:
            # Node have two or more edges, need answer analise
            if answer == 0 or answer > len(edges):
                # The answer is not correct, dot no change
                msg += 'Ответ неправильный. Выберите вариант из предложенных выше и введите его номер'
                # msg += 'The answer is not correct, you must choose from the suggestions and enter its number. '
            else:
                node_name = edges[answer - 1][1]
        else:
            msg += 'ERROR! Node name %s, comment %s have not edge(s). ' \
                   'Any node must hav edge(s), except End, one must lead at least one edge in dot file.' \
                   % (node_name, all_nodes[node_name])
            err = 22
        if err == 0:
            # Add comment for node
            msg += all_nodes[node_name].replace(r'\n', ' ')
            # List edges for this node
            edges = get_edges(node_name, all_edges)
            if len(edges) == 1:
                # Only one edge, don't need choice
                msg += '<br/>Нажмите ENTER'
                # msg += '\nPlease press ENTER'
            else:
                # User must make choice
                for i in range(1, len(edges) + 1):
                    msg += '<br/>%s) %s' % (i, edges[i - 1][2])
    return node_name, msg, err



