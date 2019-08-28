#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import configparser


def read_config(file_name="config.ini"):
    """
    Read and verify config file
    :param file_name: file name
    :return error: errors descriptions
    :return graphs: with graph dict
    :return tokens: list with tokens
    :return log: - file name for logging
    """
    error = ""
    graphs = list()
    log = None
    lang = 'eng'

    if os.access(file_name, os.F_OK):
        with open(file_name, encoding='utf-8', mode='r') as f:
            config_str = f.read()
        # delete utf-8 BOM
        config_str = config_str.replace(u'\ufeff', '')
        # read config file
        conf = configparser.ConfigParser()
        conf.read_string(config_str)
        sections = conf.sections()
        for section in sections:
            i = conf[section]
            # section with tokens and logs setup
            if section.count('settings'):
                tokens_file_name = i.get('tokens', fallback="tokens.txt")
                log = i.get('log', fallback="log.txt")
                lang = i.get('lang', fallback="eng")
            # sections with graph description
            if section.count('graph'):
                graph = dict()
                graph['file_name'] = i.get('file_name', fallback=None)
                graph['graph_name'] = i.get('graph_name', fallback=None)
                graph['description'] = i.get('description', fallback=None)
                graphs.append(graph)

        # graph section verify
        if graphs:
            for gr in graphs:
                if gr['file_name']:
                    if not os.access(gr['file_name'], os.F_OK):
                        error += 'Graph file with name %s is not found. ' % gr['file_name']
                else:
                    error += 'Graph file name is emtpy. '
                if not gr['graph_name']:
                    error += 'Graph name is empty. '
                if not gr['description']:
                    error += 'Graph description is empty. '
        else:
            error += 'Graphs list is emtpy. '
    else:
        error = "Configuration file is not found."
    return error, graphs, log, lang
