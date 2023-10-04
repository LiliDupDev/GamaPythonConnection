import socket
import os
from _thread import *
from .util_tools import util


class Server:
    # app_id = "ummisco.gama.network.common.CompositeGamaMessage"
    # bytes_to_receive
    # content_path: XML path / "./contents/string"

    def __init__(self, host, server_port, client_host ,client_port, app_id, bytes_to_receive, content_path):
        self.host = host
        self.port = server_port
        self.udp_host = client_host
        self.udp_port = client_port
        self.ThreadCount = 0
        self.ServerSocket = socket.socket()
        self.app_id = app_id
        self.bytes_to_receive=bytes_to_receive
        self.content_path = content_path
        self.tool = util()
        self.create_socket()

    def create_socket(self):
        try:
            self.ServerSocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))


    def threaded_client(self, connection, ):
        while True:
            data = connection.recv(self.bytes_to_receive)
            msg = data.decode('utf-8')

            try:
                if self.app_id in msg:
                    xml_msg = self.tool.clean_xml(msg)
                    content = self.tool.get_contents(xml_msg, self.content_path)
                    print(content)
                    id = self.tool.get_contents(xml_msg, "./receivers/agentReference/attributeValue/index/int")

                    reply = "Hola " + id + ", Soy el servidor"
                    # Response
                    self.tool.send_udp_message( self.udp_host, self.udp_port, reply)
                else:
                    print(msg)
            except:
                print("----------------------------------------------")

            if not data:
                break
        connection.close()


    def run_server(self):
        print('Waiting for a Connection...')
        self.ServerSocket.listen(5)

        while True:
            Client, address = self.ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client,))
            self.ThreadCount += 1
            print('Thread Number: ' + str(self.ThreadCount))
        self.ServerSocket.close()
