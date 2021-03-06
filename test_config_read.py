import read_config
import unittest
import pydotplus
import classes


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
        graph = classes.GraphObject()
        graph.append(graphs)
        assert graph.len() == 1
