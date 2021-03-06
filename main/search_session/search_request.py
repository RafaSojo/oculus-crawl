#!/usr/bin/env python
# -*- coding: utf-8 -*-
from main.search_engine.google_images import GoogleImages
from main.transport_core.webcore import WebCore
from main.transport_core.transport_cores import TRANSPORT_CORES
from main.search_engine.search_engine import SEARCH_ENGINES

__author__ = "Ivan de Paz Centeno"


class SearchRequest(object):
    def __init__(self, words, options=None, search_engine_proto=GoogleImages, transport_core_proto=WebCore):
        if not options:
            options = {}

        self.words = words
        self.options = options
        self.transport_core_proto = transport_core_proto
        self.search_engine_proto = search_engine_proto
        self.result = []

    def get_search_engine_proto(self):
        return self.search_engine_proto

    def get_transport_core_proto(self):
        return self.transport_core_proto

    def get_words(self):
        return self.words

    def get_options(self):
        return self.options

    def __str__(self):
        return "Words: \"{}\"; options: \"{}\" (search_engine: {}; transport core: {})".format(self.words,
                                                                                               self.options,
                                                                                               self.search_engine_proto,
                                                                                               self.transport_core_proto)

    def associate_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def __hash__(self):
        return hash(self.__str__())

    def serialize(self):
        serial = {
            'words': self.words,
            'options': self.options,
            'transport_core': str(self.transport_core_proto),
            'search_engine': str(self.search_engine_proto),
            'associated_result': self.result
        }

        return serial

    @staticmethod
    def deserialize(serial):
        search_request = SearchRequest(serial['words'], serial['options'], SEARCH_ENGINES[serial['search_engine']],
                                       TRANSPORT_CORES[serial['transport_core']])

        search_request.associate_result(serial['associated_result'])

        return search_request
