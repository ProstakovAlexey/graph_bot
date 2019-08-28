import pydotplus
import logging
import errors_code as msg_code

logger = logging.getLogger()


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class GraphObject:
    """
    Главный класс, хранит информацию о всех доступных схемах
    """
    graph_object_list = list()

    def append(self, graphs):
        for graph in graphs:
            try:
                self.graph_object_list.append(GraphSchema(file_name=graph['file_name'],
                                                          graph_name=graph['graph_name'],
                                                          description=graph['description']))
            except:
                logger.error('Can not parse dot file: ' + graph['file_name'])

    def len(self):
        return len(self.graph_object_list)

    def get_by_id(self, schema_id):
        return self.graph_object_list[schema_id]


class User:
    """
    Information about users and his activity
    """
    # Schema object for user
    schema = None

    def __init__(self, user_id, name, lang):
        self.__user_id = user_id
        self.__name = name
        self.__lang = lang

    def start(self, schema):
        self.schema = schema

    def get_lang(self):
        return self.__lang

    def get_name(self):
        return self.__name

    def clear(self):
        self.schema = None

    def next_dialog(self, answer):
        """
        :param answer: user answer
        :return: message for user
        """
        if self.schema is None:
            return msg_code.get_error(1, self.__lang)
        all_nodes = self.schema.nodes
        all_edges = self.schema.edges
        # Получаем список ребер из этой вершины
        edges = self.schema.get_edges(self.schema.current_node_id)
        # Must be one or more edges else error in dot file
        if len(edges) == 1:
            # Node have one edges, go to next node
            self.schema.current_node_id = edges[0][1]
        elif len(edges) > 1:
            # Node have two or more edges, need answer analise
            # //TODO answer переделать в цифру и именьшить на 1
            if not answer.isdigit():
                return msg_code.get_error(22, self.__lang)
            answer = int(answer)
            self.schema.current_node_id = edges[answer - 1][1]
        else:
            if self.schema.current_node_id != 'End':
                msg = msg_code.get_error(20, self.__lang) \
                      % (self.schema.current_node_id, all_nodes[self.schema.current_node_id])
                return msg

        msg = all_nodes[self.schema.current_node_id].replace(r'\n', ' ')
        # List edges for this node
        edges = self.schema.get_edges(self.schema.current_node_id)
        if len(edges) == 1:
            # Only one edge, don't need choice
            msg += "\n" + msg_code.get_error(19, self.__lang)
        else:
            # User must make choice
            for i in range(1, len(edges) + 1):
                msg += '\n%s) %s' % (i, edges[i - 1][2])
        # For end return special message and clear current dot-schema
        if self.schema.current_node_id == 'End':
            msg = msg_code.get_error(21, lang=self.__lang)
            self.schema = None
        return msg


class GraphSchema:
    """
    Information about graph schema
    """
    file_name = None
    graph_name = None
    description = None
    current_node_id = None
    # All nodes. key = unic_node_id, value= node label
    nodes = dict()
    # All edges for graph. Value is [node_source, node_destination, name]
    edges = list()

    def __init__(self, file_name, graph_name, description):
        self.file_name = file_name
        self.graph_name = graph_name
        self.description = description
        self.nodes, self.edges = self.__parse()
        # All times, any scheme will be begin fot Start node
        self.current_node_id = 'Start'

    def __parse(self):
        """
        Return all node and edges
        :return: dict nodes, list edges
        """
        dot = pydotplus.graphviz.graph_from_dot_file(self.file_name)
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

    def get_edges(self, one_node):
        """
        List all edges, for one node
        :param one_node: node
        :return: result: edges list
        """
        result = list()
        for e in self.edges:
            if e[0] == one_node:
                result.append(e)
        return sorted(result)
