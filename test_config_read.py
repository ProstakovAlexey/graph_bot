import read_config
import unittest
import pydotplus
import functions


class CaseConfig(unittest.TestCase):
    """This class testing function for read and verification configuration file"""
    def test1_good(self):
        """Read good config file, have not error"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_1.ini')
        self.assertFalse(error)

    def test2_err(self):
        """Config file have bad token files"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_2.ini')
        self.assertEqual(error, 'File with tokens is not found. ')

    def test3_err(self):
        """Config file have not description for dot file"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_3.ini')
        self.assertEqual(error, 'Graph description is empty. ')

    def test4_err(self):
        """Config file have bad dot files"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_4.ini')
        self.assertEqual(error, 'Graph file with name err/1.gv is not found. ')

    def test5_err(self):
        """Config file have not graph name"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_5.ini')
        self.assertEqual(error, 'Graph name is empty. ')


class CaseDot(unittest.TestCase):
    """This class testing function for graph algoritm"""

    def test1_way(self):
        """Load config and checking data"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_6.ini')
        self.assertFalse(error)
        graph_object_list = list()
        for graph in graphs:
            gr = pydotplus.graphviz.graph_from_dot_file(graph['file_name'])
            graph_object_list.append(functions.parse_dot(gr))
        self.assertEqual(len(graph_object_list), 1)
        good = (
            {
                'node': 'node',
                'Start': 'Start',
                'T1': 'Node #1. Only one way.',
                'T2': 'Node #2, have question with choice. What choice you?',
                'T3a': 'Node #3a. You was say YES',
                'T3b': 'Node #3b. You was say NO',
                'T4': 'Finish node #4. One way.',
                'End': 'End'
            },
            [
                ['Start', 'T1', None],
                ['T1', 'T2', None],
                ['T2', 'T3a', 'YES'],
                ['T2', 'T3b', 'NO'],
                ['T3a', 'T4', None],
                ['T3b', 'T4', None],
                ['T4', 'End', None]
            ]
        )
        self.assertEqual(good[0], graph_object_list[0][0],
                         'Error in function for read graph file. Problem with node list.')