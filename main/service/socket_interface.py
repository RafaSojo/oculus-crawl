#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from multiprocessing import Lock
import zmq

__author__ = 'Iván de Paz Centeno'


class SocketInterface(object):

    def __init__(self, host, port, zmq_context=None):

        self.host = host
        self.port = port
        self.socket = None
        self.lock = Lock()
        self.poll = None
        self.context = zmq_context

    def get_context(self):
        return self.context

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def __get_socket__(self):

        with self.lock:
            socket = self.socket

        return socket

    def __set_socket__(self, socket):

        with self.lock:
            self.socket = socket

    def init_socket(self):

        if not self.context:
            self.context = zmq.Context()
            logging.debug("Socket context intialized.")
        else:
            logging.debug("Socket context injected.")

        socket = self.context.socket(zmq.ROUTER)
        self.__set_socket__(socket)

        socket.RCVTIMEO = 10000

        socket.bind("tcp://{}:{}".format(self.host, self.port))
        #print("Running server on {}:{}".format(self.host, self.port))
        logging.info("Socket opened in port {}".format(self.port))
        self.poll = zmq.Poller()
        self.poll.register(socket, zmq.POLLIN)

    def get_context(self):
        return self.context

    def get_new_request(self):

        received_request = {}
        identity = None
        exit_requested = False

        socket = self.__get_socket__()

        try:

            sockets = dict(self.poll.poll(1000))

            if sockets:
                identity = socket.recv().decode()
                formatted_request = socket.recv_json()
                print(formatted_request)
                if not ('action' in formatted_request):

                    socket.send_string(identity, zmq.SNDMORE)
                    socket.send_json({'error': 'Invalid request'})

                else:

                    received_request = formatted_request

        except KeyboardInterrupt:
            exit_requested = True

        return [received_request, identity, exit_requested]

    def send_response(self, send_to_id, formatted_response):
        socket = self.__get_socket__()
        socket.send_string(send_to_id, zmq.SNDMORE)
        socket.send_json(formatted_response)

    def terminate(self):
        self.__get_socket__().unbind("tcp://{}:{}".format(self.host, self.port))
        self.__get_socket__().setsockopt(zmq.LINGER, 0)
        self.__get_socket__().close()
        logging.info("Socket closed for port {}".format(self.port))
        self.__set_socket__(None)
